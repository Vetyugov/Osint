package ru.bitok.osint.osint_web_service.service.addressValidator

import org.slf4j.Logger
import org.slf4j.LoggerFactory
import org.springframework.stereotype.Component
import java.security.MessageDigest

/**
 * https://rosettacode.org/wiki/Bitcoin/address_validation#Kotlin
 */
@Component
class AddressBitcoinValidator : AddressValidator {

    private val ALPHABET = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"

    override fun patternName(): String {
        return "BTC Legacy address"
    }

    override fun isValidAddress(address: String): Boolean {
        try {
            if (address.length !in 26..35) return false
            val decoded = decodeBase58(address)
            if (decoded == null) return false
            val hash = sha256(decoded, 0, 21, 2)
            return hash.sliceArray(0..3).contentEquals(decoded.sliceArray(21..24))
        } catch (e: Exception) {
            logger.error("Не удалось провалидировать адрес: $address",e)
            return false
        }

    }

    private fun ByteArray.contentEquals(other: ByteArray): Boolean {
        if (this.size != other.size) return false
        return (0 until this.size).none { this[it] != other[it] }
    }

    private fun decodeBase58(input: String): ByteArray? {
        val output = ByteArray(25)
        for (c in input) {
            var p = ALPHABET.indexOf(c)
            if (p == -1) return null
            for (j in 24 downTo 1) {
                p += 58 * (output[j].toInt() and 0xff)
                output[j] = (p % 256).toByte()
                p = p shr 8
            }
            if (p != 0) return null
        }
        return output
    }

    private fun sha256(data: ByteArray, start: Int, len: Int, recursion: Int): ByteArray {
        if (recursion == 0) return data
        val md = MessageDigest.getInstance("SHA-256")
        md.update(data.sliceArray(start until start + len))
        return sha256(md.digest(), 0, 32, recursion - 1)
    }

    companion object {
        private val logger: Logger = LoggerFactory.getLogger(this::class.java)
    }
}