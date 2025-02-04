package ru.bitok.osint.osint_web_service.util

import org.jsoup.Jsoup
import org.jsoup.nodes.Document
import org.jsoup.nodes.Element
import org.slf4j.Logger
import org.slf4j.LoggerFactory
import org.springframework.stereotype.Component

@Component
class StaticWebParser {
    data class WebParserResult(
        val onlyText:String,
        val html: String,
        val links: Set<String>,
    )

    // Функция для извлечения списка ссылок со страницы
    fun extractLinks(url: String, mainLink:String, onlyWithSameHost: Boolean): WebParserResult? {
        return try {
            val document: Document = Jsoup.connect(url).get()
            val body = document.body()
            val indexThirdSlash = findThirdSlashIndex(mainLink)
            // Извлечение всех ссылок (href атрибутов) из тега <a>
            val urls = document.select("a[href]").map { it.attr("abs:href") }.filter { it ->
                if (onlyWithSameHost and (indexThirdSlash > 0)){
                    return@filter it.startsWith(mainLink.substring(0, indexThirdSlash))
                }
                return@filter true
            }.toList()
            WebParserResult(body.text(), body.html(), urls.toSet())
        } catch (e: Exception) {
            logger.error("Ошибка при извлечении содердимого url <$url> : ${e.message}")
            null
        }
    }

    fun getContextForString(htmlText: String, targetString:String): String {
        // Парсинг HTML текста
        val document: Document = Jsoup.parse(htmlText)

        // Поиск всех элементов <p>
        val paragraphs: List<Element> = document.select("p")
        // Проход по всем параграфам для поиска выбранного слова
        var result = paragraphs.map { it.text() }
            .filter { it.contains(targetString, ignoreCase = true) }
            .map { it.replace(Regex(" +"), " ").replace(Regex("\n+"), "\n") }
            .joinToString("\n-----------------------------------------------------------------\n") { it }
            .takeIf { it.isNotBlank() }
        result = result?.let { "Найден в тэге <p>\n$result" }
        //Если не нашелся в <p>
        if(result == null){
            // Поиск всех элементов <div>
            val divs: List<Element> = document.select("div")
            // Проход по всем параграфам для поиска выбранного слова
            result = divs.map { it.text() }
                .filter { it.contains(targetString, ignoreCase = true) }
                .map { it.replace(Regex(" +"), " ").replace(Regex("\n+"), "\n") }
                .first()
                .takeIf { it.isNotBlank() }

            result = result?.let {"Найден в тэге <div>\n$result"}
        }
        return result?:document.text()
    }


    private fun findThirdSlashIndex(input: String): Int {
        var slashCount = 0

        for (i in input.indices) {
            if (input[i] == '/') {
                slashCount++
                if (slashCount == 3) {
                    return i // Возвращаем индекс третьего слэша
                }
            }
        }

        return -1 // Если третьего слэша нет, возвращаем -1
    }

    companion object {
        private val logger: Logger = LoggerFactory.getLogger(this::class.java)
    }
}