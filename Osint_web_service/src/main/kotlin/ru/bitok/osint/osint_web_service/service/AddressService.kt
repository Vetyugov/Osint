package ru.bitok.osint.osint_web_service.service

import org.slf4j.Logger
import org.slf4j.LoggerFactory
import org.springframework.stereotype.Service
import org.springframework.transaction.annotation.Transactional
import ru.bitok.osint.osint_web_service.entity.WebFoundAddress
import ru.bitok.osint.osint_web_service.entity.WebFoundInfo
import ru.bitok.osint.osint_web_service.entity.WebQueueLink
import ru.bitok.osint.osint_web_service.entity.WebSourcesLink
import ru.bitok.osint.osint_web_service.exception.SourceLinkNotFoundException
import ru.bitok.osint.osint_web_service.repository.WebFoundAddressRepository
import ru.bitok.osint.osint_web_service.repository.WebFoundInfoRepository
import ru.bitok.osint.osint_web_service.repository.WebQueueLinkRepository
import ru.bitok.osint.osint_web_service.service.addressValidator.AddressValidatorStrategy
import ru.bitok.osint.osint_web_service.util.AddressParser
import ru.bitok.osint.osint_web_service.util.StaticWebParser
import java.time.Instant

@Service
class AddressService(
    val webFoundAddressRepository: WebFoundAddressRepository,
    val webFoundInfoRepository: WebFoundInfoRepository,
    val webQueueLinkRepository: WebQueueLinkRepository,
    val addressParser: AddressParser,
    val webParser: StaticWebParser,
    val addressValidatorStrategy: AddressValidatorStrategy
) {
    @Transactional
    fun saveParserResult(link: WebQueueLink, onlyWithSameHost: Boolean) {
        //Анализируем ссылку
        val webParserResult = webParser.extractLinks(
            link.link,
            link.sourceLink?.link?:throw SourceLinkNotFoundException(link.link),
            onlyWithSameHost
        )
        webParserResult?.also { webResult ->
            //Ищем адрес в тексте
            val addressParserResults = addressParser.foundInText(webResult.onlyText)
            logger.info("Найдено ${addressParserResults.size} адресов: $addressParserResults")
            addressParserResults.forEach { parserResult ->
                //Сохраняем результат поиска
                val webFoundAddress =
                    webFoundAddressRepository.findByAddress(parserResult.address) ?: WebFoundAddress().apply {
                        address = parserResult.address
                        cryptoName = parserResult.cryptoName.name
                        patternName = parserResult.patternName
                        validAddress = addressValidatorStrategy.validate(parserResult.address, parserResult.patternName)
                    }
                webFoundAddressRepository.save(webFoundAddress).let { savedWebFoundAddress ->
                    webFoundInfoRepository.save(WebFoundInfo().apply {
                        address = savedWebFoundAddress
                        context = webParser.getContextForString(webResult.html, savedWebFoundAddress.address)
                        source = link.link
                        foundTime = Instant.now()
                    })
                }
            }
            //Сохраняем новые найденные ссылки
            val webSourcesLink = link.sourceLink ?: WebSourcesLink().apply {
                this.link = link.link
                analyzedTime = Instant.now()
            }

            webQueueLinkRepository.saveAll(
                webParserResult.links.subtract(webQueueLinkRepository.findAllInList(webParserResult.links).toSet())
                    .map {
                        WebQueueLink().apply {
                            this.link = it
                            sourceLink = webSourcesLink
                            isAnalyzed = false
                        }
                    })
            logger.info("Новых ссылок сохранено: ${webParserResult.links.size}")
        }
        //Сохраняем ссылку
        link.isAnalyzed = true
        link.lastMonitoringTime = Instant.now()
        webQueueLinkRepository.save(link)
    }

    companion object {
        private val logger: Logger = LoggerFactory.getLogger(this::class.java)
    }
}