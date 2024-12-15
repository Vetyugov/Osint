package ru.bitok.osint.osint_web_service.entity

import jakarta.persistence.Column
import jakarta.persistence.Entity
import jakarta.persistence.Id
import jakarta.persistence.Table
import org.hibernate.annotations.ColumnDefault
import java.time.Instant

@Entity
@Table(name = "web_sources_links", schema = "osint_web_v2")
class WebSourcesLink {
    @Id
    @Column(name = "link", nullable = false, length = Integer.MAX_VALUE)
    var link: String = ""

    @ColumnDefault("CURRENT_TIMESTAMP")
    @Column(name = "analyzed_time")
    var analyzedTime: Instant = Instant.now()

    @Column(name = "active", nullable = false)
    var active: Boolean = true

    @ColumnDefault("NULL::character varying")
    @Column(name = "user_comment")
    var userComment: String? = null
}