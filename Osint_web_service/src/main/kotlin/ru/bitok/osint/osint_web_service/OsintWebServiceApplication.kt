package ru.bitok.osint.osint_web_service

import org.springframework.boot.autoconfigure.SpringBootApplication
import org.springframework.boot.runApplication

@SpringBootApplication
class OsintWebServiceApplication

fun main(args: Array<String>) {
    runApplication<OsintWebServiceApplication>(*args)
}
