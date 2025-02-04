package ru.bitok.osint.osint_web_service.util

import org.junit.jupiter.api.Test
import java.io.File

class WebParserTest {
    @Test
    fun findContextInHtml() {
        val staticWebParser = StaticWebParser()
        // Создаем объект файла
        val file = File("C:\\ownProjects\\PycharmProjects\\Osint\\Osint_web_service\\src\\test\\kotlin\\ru\\bitok\\osint\\osint_web_service\\util\\text_html.html")
        // Читаем все содержимое файла и возвращаем его

        val contextForString = staticWebParser.getContextForString(
            file.readText(),
            "14znnCq91DDYqJJJhUBqjGeii3pGEPQdks"
        )
        println("Контекст: $contextForString")
        assert(contextForString != "Не найден")
    }

    @Test
    fun checkRedditComments(){
        val staticWebParser = StaticWebParser()
        val extractLinks =
            staticWebParser.extractLinks("https://www.reddit.com/r/Bitcoin/comments/1i520qg/what_does_he_mean_by_that/")
        println(extractLinks?.onlyText)
    }

    @Test
    fun checkDynamicRedditComments(){
        val staticWebParser = DynamicWebParser()
        val extractLinks =
            staticWebParser.fetchDynamicPageContent("https://www.reddit.com/r/Bitcoin/comments/1i520qg/what_does_he_mean_by_that/")
        println(extractLinks)
    }


}