package ru.bitok.osint.osint_web_service.service.addressValidator

import org.springframework.stereotype.Component

@Component
class AddressValidatorStrategy(validators: List<AddressValidator>) {
    private val validatorsMap = validators.associateBy({ it.patternName() }, { it })
    fun validate(address: String, patternName: String): Boolean? {
        return validatorsMap[patternName]?.isValidAddress(address)
    }

    fun getAllPatterns(): List<String> = validatorsMap.keys.toList()
}