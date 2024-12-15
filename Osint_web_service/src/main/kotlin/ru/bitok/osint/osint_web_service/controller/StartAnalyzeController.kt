package ru.bitok.osint.osint_web_service.controller

import lombok.AllArgsConstructor
import org.slf4j.Logger
import org.slf4j.LoggerFactory
import org.springframework.web.bind.annotation.PostMapping
import org.springframework.web.bind.annotation.RequestMapping
import org.springframework.web.bind.annotation.RequestParam
import org.springframework.web.bind.annotation.RestController
import ru.bitok.osint.osint_web_service.service.AddressSearcher
import ru.bitok.osint.osint_web_service.service.CircleSearchService

@RestController
@AllArgsConstructor
@RequestMapping("/api/v1/analyze")
class StartAnalyzeController(
    val addressSearcher: AddressSearcher,
    val circleSearchService: CircleSearchService
) {

    @PostMapping("/start")
    fun startAnalyzeUrl(
        @RequestParam("url") url: String,
        @RequestParam("startCircleThread") startCircleThread: Boolean?
    ) {
        logger.info("Получен запрос на запуск анализа: startCircleThread = $startCircleThread, url = $url")
        if (startCircleThread == null || startCircleThread == false) {
            addressSearcher.startSearch(url)
        } else {
            circleSearchService.threadStatus = CircleSearchService.ThreadStatus.RUN
            circleSearchService.analyzingWebSourcesLink = url
            circleSearchService.start()
        }
        logger.info("Запрос на запуск анализа отработал успешно")
    }

    @PostMapping("/stop")
    fun stopAnalyze() {
        logger.info("Получен запрос на остановку анализа")
        circleSearchService.stopAnalyze()
    }

    companion object {
        private val logger: Logger = LoggerFactory.getLogger(this::class.java)
    }

}