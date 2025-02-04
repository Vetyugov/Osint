package ru.bitok.osint.osint_web_service.util

import org.openqa.selenium.WebDriver
import org.openqa.selenium.chrome.ChromeDriver
import org.openqa.selenium.chrome.ChromeOptions
import org.slf4j.Logger
import org.slf4j.LoggerFactory
import org.springframework.stereotype.Component
import java.util.concurrent.TimeUnit

@Component
class DynamicWebParser {
    data class WebParserResult(
        val onlyTest: String,
        val html: String,
        val links: Set<String>,
    )

    //    val PATH_TO_CHROME_DRIVER = "C:\\Users\\Admin\\AppData\\Local\\Google\\Chrome\\Application\\chrome.exe"
    val PATH_TO_CHROME_DRIVER = "chrome_driver/chromedriver.exe"
//    val PATH_TO_CHROME_DRIVER = "C:\\ownProjects\\PycharmProjects\\Osint\\Osint_web_service\\chrome_driver\\chromedriver.exe"

    fun fetchDynamicPageContent(url: String): String {
        // Укажите путь к вашему драйверу Chrome
        System.setProperty("webdriver.chrome.driver", PATH_TO_CHROME_DRIVER)
        System.getProperty("webdriver.chrome.driver")?.let { println(it) }

        // Настраиваем опции браузера
        val options = ChromeOptions()
        options.addArguments("--headless") // Запуск в фоновом режиме
        options.addArguments("--no-sandbox")
        options.addArguments("--disable-dev-shm-usage")
        options.setBinary("chrome_driver/chrome-win32/chrome.exe")

        // Создаем экземпляр драйвера
        val driver: WebDriver = ChromeDriver(options)
        driver.manage().timeouts().implicitlyWait(10, TimeUnit.SECONDS)

        return try {
            // Открываем URL
            driver.get(url)

            // Получаем полное содержимое страницы
            driver.pageSource
        } finally {
            // Закрываем драйвер
            driver.quit()
        }
    }

    companion object {
        private val logger: Logger = LoggerFactory.getLogger(this::class.java)
    }
}