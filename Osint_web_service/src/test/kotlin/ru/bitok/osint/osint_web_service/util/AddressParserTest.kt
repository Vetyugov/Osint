package ru.bitok.osint.osint_web_service.util

import org.junit.jupiter.api.Test
import ru.bitok.osint.osint_web_service.util.AddressParser
import kotlin.test.assertTrue

class AddressParserTest {
    @Test
    fun `address found in text`(){
        val parser = AddressParser()
        val found = parser.foundInText("0sz; alt. Digital Currency Address - XBT bc1qa2xr7dmz5lztplp9yfp7k382nf4ma8gwrl7zgg; alt. Digital Currency Address ")
        assertTrue { found.size == 1 }
        assertTrue { found.get(0).address == "bc1qa2xr7dmz5lztplp9yfp7k382nf4ma8gwrl7zgg" }
    }


    @Test
    fun `address found in text 2`(){
        val parser = AddressParser()
        val found = parser.foundInText("    Адрес для добровольных пожертвований на развитие - 1BQ9qza7fn9snSCyJQB3ZcN46biBtkt4ee (QR)\n" +
                "    ---------------------------------------\n")
        assertTrue { found.size == 1 }
        assertTrue { found.get(0).address == "1BQ9qza7fn9snSCyJQB3ZcN46biBtkt4ee" }
    }
}