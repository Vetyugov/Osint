package ru.bitok.osint.osint_web_service.entity

import jakarta.persistence.*
import org.hibernate.annotations.ColumnDefault
import java.time.Instant
import java.util.UUID

@Entity
@Table(name = "web_found_info", schema = "osint_web_v2")
class WebFoundInfo {
    @Id
    @Column(name = "id")
    var id: UUID = UUID.randomUUID()

    @ManyToOne(fetch = FetchType.LAZY, optional = false)
    @JoinColumn(name = "address", nullable = false)
    var address: WebFoundAddress = WebFoundAddress()

    @Column(name = "context", length = Integer.MAX_VALUE)
    var context: String? = null

    @Column(name = "source", length = Integer.MAX_VALUE)
    var source: String? = null

    @ColumnDefault("CURRENT_TIMESTAMP")
    @Column(name = "found_time")
    var foundTime: Instant = Instant.now()

    @Column(name = "is_approved")
    var isApproved: Boolean = false
}