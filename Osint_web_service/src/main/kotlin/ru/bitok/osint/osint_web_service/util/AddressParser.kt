package ru.bitok.osint.osint_web_service.util

import org.slf4j.Logger
import org.slf4j.LoggerFactory
import org.springframework.stereotype.Component

@Component
class AddressParser {
    data class AddressParserResult(
        val address: String,
        val text: String,
        val cryptoName: CryptoName,
        val patternName: String
    )

    enum class CryptoName(value: Int) {
        BTC(0),
        ETH(1),
        DASH(2),
        XMR(3),
        ADA(4),
        ATOM(5),
        DOGE(6),
        MIOTA(7),
        LSK(8),
        LTC(9),
        XEM(10),
        NEO(11),
        ONT(12),
        DOT(13),
        XRP(14),
        XLM(15),
        TRC_20(16),
        TRX(17),
        UNIVERSAL(18),
    }


    private final val BTC_ADDRESSES_REGEX_PATTERNS = mapOf(
        "BTC Legacy address" to Regex("(?<![a-z0-9A-Z/])1[a-z0-9A-Z]{25,33}(?![a-z0-9A-Z])"),
        "BTC P2SH address" to Regex("(?<![a-z0-9A-Z/])3[a-z0-9A-Z]{25,33}(?![a-z0-9A-Z])"),
        "BTC Segwit address" to Regex("(?<![a-z0-9A-Z/])bc1[a-z0-9A-Z]{23,42}(?![a-z0-9A-Z])"),
        "BTC Taproot address" to Regex("(?<![a-z0-9A-Z/])bc1p[a-z0-9A-Z]{23,42}(?![a-z0-9A-Z])"),

        // Слово целиком
        "BTC Legacy address full" to Regex("^1[a-z0-9A-Z]{25,33}$"),
        "BTC P2SH address full" to Regex("^3[a-z0-9A-Z]{25,33}$"),
        "BTC Segwit address full" to Regex("^bc1[a-z0-9A-Z]{23,42}$"),
        "BTC Taproot address full" to Regex("^bc1p[a-z0-9A-Z]{23,42}$")
    )
    private final val ETH_ADDRESSES_REGEX_PATTERNS = mapOf(
        "ETH address" to Regex("(?<![^a-z0-9A-Z/]0x[0-9A-Fa-f]{40}[^a-z0-9A-Z])"),
        "ETH address full" to Regex("^0x[0-9A-Fa-f]{40}$"),
    )

    val patterns = mapOf(
        CryptoName.BTC to BTC_ADDRESSES_REGEX_PATTERNS,
        CryptoName.ETH to ETH_ADDRESSES_REGEX_PATTERNS
    )

    fun foundInText(text: String): List<AddressParserResult> {
        val result = ArrayList<AddressParserResult>()
        try {
            for ((cryptoName, pattern) in patterns) {
                for ((patternName, regex) in pattern) {
                    for (matchResult in regex.findAll(text)) {
                        matchResult.value.takeIf { it.isNotBlank() }?.let {
                            result.add(AddressParserResult(it, text, cryptoName, patternName))
                        }
                    }
                }
            }
            logger.debug("Найдены адреса: {}", result)
        } catch (e: Exception) {
            logger.error("Ошибка при поиске адресов в тексте", e)
        }
        return result
    }

    companion object {
        private val logger: Logger = LoggerFactory.getLogger(this::class.java)
    }
}

