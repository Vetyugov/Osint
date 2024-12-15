package ru.bitok.osint.osint_web_service.repository

import org.springframework.data.jpa.repository.JpaRepository
import org.springframework.stereotype.Repository
import ru.bitok.osint.osint_web_service.entity.WebSourcesLink

@Repository
interface WebSourcesLinkRepository: JpaRepository<WebSourcesLink, String> {
    fun findByLink(link:String):WebSourcesLink?
}