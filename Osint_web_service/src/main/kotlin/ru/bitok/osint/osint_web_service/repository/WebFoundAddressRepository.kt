package ru.bitok.osint.osint_web_service.repository

import org.springframework.data.jpa.repository.JpaRepository
import org.springframework.data.jpa.repository.Query
import org.springframework.stereotype.Repository
import ru.bitok.osint.osint_web_service.entity.WebFoundAddress

@Repository
interface WebFoundAddressRepository : JpaRepository<WebFoundAddress, String>{
    fun findByAddress(address: String): WebFoundAddress?

    @Query("""
        select a from WebFoundAddress a
        where a.patternName in (:patternNames) and a.validAddress is null
    """)
    fun findAllNotValidatedInPatternList(patternNames:List<String>): List<WebFoundAddress>
}