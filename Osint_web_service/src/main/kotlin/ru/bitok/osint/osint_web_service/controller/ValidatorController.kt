package ru.bitok.osint.osint_web_service.controller

import lombok.AllArgsConstructor
import org.springframework.web.bind.annotation.PostMapping
import org.springframework.web.bind.annotation.RequestMapping
import org.springframework.web.bind.annotation.RestController
import ru.bitok.osint.osint_web_service.service.AddressValidatorService

@RestController
@AllArgsConstructor
@RequestMapping("/api/v1/validate")
class ValidatorController(
    val addressValidatorService: AddressValidatorService
) {

    @PostMapping("/historic")
    fun validateAllHistoricAddresses(){
        addressValidatorService.validateAllHistoricalAddressesInDB()
    }
}