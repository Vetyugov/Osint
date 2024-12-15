package ru.bitok.osint.osint_web_service.entity

import jakarta.persistence.*
import org.hibernate.annotations.ColumnDefault
import java.time.Instant

@Entity
@Table(name = "web_queue_link", schema = "osint_web_v2")
class WebQueueLink {
    @Id
    @Column(name = "link", nullable = false, length = Integer.MAX_VALUE)
    var link: String = ""

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "source_link")
    var sourceLink: WebSourcesLink? = null

    @Column(name = "is_analyzed")
    var isAnalyzed: Boolean = false

    @Column(name = "last_monitoring_time")
    var lastMonitoringTime: Instant? = null

    @Column(name = "create_time")
    var createTime: Instant = Instant.now()
}