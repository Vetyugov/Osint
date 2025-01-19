package ru.bitok.osint.osint_web_service.service.addressValidator

interface AddressValidator {
    fun patternName():String
    fun isValidAddress(address: String): Boolean
}