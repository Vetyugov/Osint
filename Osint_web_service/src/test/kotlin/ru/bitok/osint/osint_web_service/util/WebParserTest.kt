package ru.bitok.osint.osint_web_service.util

import org.junit.jupiter.api.Test
import java.io.File

class WebParserTest {
    @Test
    fun findContextInHtml() {
        val webParser = WebParser()
        // Создаем объект файла
        val file = File("C:\\ownProjects\\PycharmProjects\\Osint\\Osint_web_service\\src\\test\\kotlin\\ru\\bitok\\osint\\osint_web_service\\util\\text_html.html")
        // Читаем все содержимое файла и возвращаем его

        val contextForString = webParser.getContextForString(
            file.readText(),
            "14znnCq91DDYqJJJhUBqjGeii3pGEPQdks"
        )
        println("Контекст: $contextForString")
        assert(contextForString != "Не найден")
    }
}