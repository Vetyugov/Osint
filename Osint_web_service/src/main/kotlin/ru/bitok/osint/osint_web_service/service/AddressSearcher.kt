package ru.bitok.osint.osint_web_service.service

import org.slf4j.Logger
import org.slf4j.LoggerFactory
import org.springframework.data.domain.PageRequest
import org.springframework.stereotype.Service
import ru.bitok.osint.osint_web_service.entity.WebQueueLink
import ru.bitok.osint.osint_web_service.entity.WebSourcesLink
import ru.bitok.osint.osint_web_service.repository.WebQueueLinkRepository
import ru.bitok.osint.osint_web_service.repository.WebSourcesLinkRepository
import java.time.Instant

@Service
class AddressSearcher(
    val webQueueLinkRepository: WebQueueLinkRepository,
    val webSourcesLinkRepository: WebSourcesLinkRepository,
    val addressService: AddressService
) {


    fun startSearch(url: String) {
        val notAnalyzedListOfLink = webQueueLinkRepository.findNotAnalyzedListOfLink(url, PageRequest.of(0, 20))
        if (notAnalyzedListOfLink.isNotEmpty()) {
            logger.info("Корневая ссылка $url найдена - продолжаем анализ ${notAnalyzedListOfLink.size} ссылок")
            continueSearch(notAnalyzedListOfLink)
        } else {
            logger.info("Корневая ссылка $url ещё не анализировалась - запускаем анализ ")
            val webQueueLink = webQueueLinkRepository.save(WebQueueLink().apply {
                link = url
                sourceLink = webSourcesLinkRepository.save(WebSourcesLink().apply {
                    this.link = url
                    analyzedTime = Instant.now()
                })
                isAnalyzed = false
            })
            continueSearch(listOf(webQueueLink))
        }
    }

    private fun continueSearch(links: List<WebQueueLink>) {
        links.forEach { link ->
            try {
                addressService.saveParserResult(link)
            } catch (e: Exception) {
                logger.error("Не удалось произвести анализ ссылки $link", e)
            }
        }
    }

    companion object {
        private val logger: Logger = LoggerFactory.getLogger(this::class.java)
    }

}