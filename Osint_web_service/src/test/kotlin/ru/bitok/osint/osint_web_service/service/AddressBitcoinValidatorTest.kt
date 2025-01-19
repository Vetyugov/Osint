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
    fun checkBitCoinValidation(candidate: String) {
        val addressValidator = AddressBitcoinValidator()
        assertTrue { addressValidator.isValidAddress(candidate) }
    }


}