package ru.bitok.osint.osint_web_service.service

import org.slf4j.Logger
import org.slf4j.LoggerFactory
import org.springframework.stereotype.Service
import ru.bitok.osint.osint_web_service.repository.WebFoundAddressRepository
import ru.bitok.osint.osint_web_service.service.addressValidator.AddressValidatorStrategy

@Service
class AddressValidatorService(
    private val addressValidatorStrategy: AddressValidatorStrategy,
    private val webFoundAddressRepository: WebFoundAddressRepository
    ) {


    fun validateAllHistoricalAddressesInDB(){
        logger.info("Запущен процесс анализа исторических адресов...")
        val findAllNotValidatedInPatternList =
            webFoundAddressRepository.findAllNotValidatedInPatternList(addressValidatorStrategy.getAllPatterns())
        logger.info("Для анализа найдено ${findAllNotValidatedInPatternList.size} адресов")
        findAllNotValidatedInPatternList.forEach{
            webFoundAddressRepository.save(it.apply { validAddress = addressValidatorStrategy.validate(it.address, it.patternName) })
        }
        logger.info("Процесс анализа исторических адресов Успешно завершен...")

    }

    companion object {
        private val logger: Logger = LoggerFactory.getLogger(this::class.java)
    }
}