package ru.bitok.osint.osint_web_service.service

import org.junit.jupiter.params.ParameterizedTest
import org.junit.jupiter.params.provider.ValueSource
import ru.bitok.osint.osint_web_service.service.addressValidator.AddressBitcoinValidator
import kotlin.test.assertTrue

class AddressBitcoinValidatorTest {


    /**
     * "BTC Legacy address"
     */
    @ParameterizedTest(name = "Validation should return true for {0}")
    @ValueSource(
        strings = [
            "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa",
            "1BQ9qza7fn9snSCyJQB3ZcN46biBtkt4ee",
            "1BFGurtJoM8vM813yoWrRE2YNtJymjyYNn",
            "1HQ2ZmTRmVetEsuJT8KfenMuYPetqGNDAp",
            "1ExBPRJLeYqiJAmZ134ncTwyfFztsXtr8s"
        ]
    )
    fun checkBitCoin1Validation(candidate: String) {
        val addressValidator = AddressBitcoinValidator()
        assertTrue { addressValidator.isValidAddress(candidate) }
    }

    /**
     * "BTC P2SH address"
     */
    @ParameterizedTest(name = "Validation should return true for {0}")
    @ValueSource(
        strings = [
            "36mwXuH4FVaeLuMUsmyU7YvVXKCcuZyP5N"
        ]
    )
    fun checkBitCoin3Validation(candidate: String) {
        val addressValidator = AddressBitcoinValidator()
        assertTrue { addressValidator.isValidAddress(candidate) }
    }

    /**
     * "BTC P2SH address"
     */
    @ParameterizedTest(name = "Validation should return true for {0}")
    @ValueSource(
        strings = [
            "bc1qw508d6qejxtdg4y5r3zarvary0c5xw7kv8f3t4"
        ]
    )
    fun checkBitCoinBc1Validation(candidate: String) {
        val addressValidator = AddressBitcoinValidator()
        assertTrue { addressValidator.isValidAddress(candidate) }
    }

}