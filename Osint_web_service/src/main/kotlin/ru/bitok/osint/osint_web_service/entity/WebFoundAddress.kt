package ru.bitok.osint.osint_web_service.entity

import jakarta.persistence.Column
import jakarta.persistence.Entity
import jakarta.persistence.Id
import jakarta.persistence.Table
import org.hibernate.annotations.ColumnDefault
import ru.bitok.osint.osint_web_service.util.AddressParser
import java.time.Instant

@Entity
@Table(name = "web_found_address", schema = "osint_web_v2")
class WebFoundAddress {
    @Id
    @Column(name = "address", nullable = false, length = Integer.MAX_VALUE)
    var address: String = ""

    @Column(name = "search_type", length = Integer.MAX_VALUE)
    var searchType: String = "WEB"

    @Column(name = "crypto_name", nullable = false, length = Integer.MAX_VALUE)
    var cryptoName: String = AddressParser.CryptoName.UNIVERSAL.name

    @Column(name = "pattern_name", nullable = false, length = Integer.MAX_VALUE)
    var patternName: String = "NOT_STATED"

    @Column(name = "valid_address", nullable = false)
    var validAddress: Boolean = false

    @Column(name = "create_time")
    var createTime: Instant = Instant.now()
}