package ru.bitok.osint.osint_web_service.service

import org.slf4j.Logger
import org.slf4j.LoggerFactory
import org.springframework.beans.factory.config.ConfigurableBeanFactory
import org.springframework.context.annotation.Scope
import org.springframework.stereotype.Service
import ru.bitok.osint.osint_web_service.exception.AnalyzeAlreadyStartedException

@Service
@Scope(value = ConfigurableBeanFactory.SCOPE_SINGLETON)
class CircleSearchService(
    val addressSearcher: AddressSearcher
) : Thread() {

    enum class ThreadStatus {
        RUN,
        STOP
    }

    var analyzingWebSourcesLink: String? = null
    var onlyWithSameHost: Boolean = true
    private var threadStatus: ThreadStatus = ThreadStatus.STOP


    override fun run() {
        if(threadStatus == ThreadStatus.RUN) {
            logger.info("Поток уже был запущен")
            throw AnalyzeAlreadyStartedException()
        }
        threadStatus = CircleSearchService.ThreadStatus.RUN
        logger.info("Поток запущен...")
        while (threadStatus == ThreadStatus.RUN) {
            try {
                analyzingWebSourcesLink?.also { it ->
                    addressSearcher.startSearch(it, onlyWithSameHost)
                } ?: also {
                    threadStatus = ThreadStatus.STOP
                }
                sleep(100)
            } catch (exception: Exception) {
                logger.error("Непредвиденная ошибка ", exception)
            }
        }
        logger.info("Поток остановлен")
    }

    fun stopAnalyze() {
        threadStatus = ThreadStatus.STOP
        analyzingWebSourcesLink?.also {
            addressSearcher.stopSearch(it)
        }
    }

    companion object {
        private val logger: Logger = LoggerFactory.getLogger(this::class.java)
    }
}