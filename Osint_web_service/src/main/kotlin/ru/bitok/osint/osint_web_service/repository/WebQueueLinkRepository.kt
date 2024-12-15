package ru.bitok.osint.osint_web_service.repository

import org.springframework.data.domain.Pageable
import org.springframework.data.jpa.repository.JpaRepository
import org.springframework.data.jpa.repository.Query
import org.springframework.stereotype.Repository
import ru.bitok.osint.osint_web_service.entity.WebQueueLink

@Repository
interface WebQueueLinkRepository:JpaRepository<WebQueueLink, String> {
    @Query("select queue from WebQueueLink queue join fetch WebSourcesLink source on queue.sourceLink = source where queue.isAnalyzed = false and source.link=:link")
    fun findNotAnalyzedListOfLink(link:String, pageable: Pageable):List<WebQueueLink>

    @Query("select queue.link from WebQueueLink queue where queue.link in (:links)")
    fun findAllInList(links: Set<String>): List<String>
}