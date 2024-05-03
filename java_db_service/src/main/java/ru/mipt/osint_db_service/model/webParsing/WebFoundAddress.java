package ru.mipt.osint_db_service.model.webParsing;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import jakarta.persistence.Table;
import lombok.Getter;
import lombok.Setter;
import ru.mipt.osint_db_service.model.FoundAddressDto;

@Getter
@Setter
@Entity
@Table(name = "web_found_address", schema = "osint_web")
public class WebFoundAddress implements FoundAddressDto {
    @Id
    @Column(name = "id", nullable = false)
    private String id;

    @Column(name = "search_type", nullable = false, length = Integer.MAX_VALUE)
    private String searchType;

    @Column(name = "crypto_name", nullable = false, length = Integer.MAX_VALUE)
    private String cryptoName;

    @Column(name = "pattern_name", nullable = false, length = Integer.MAX_VALUE)
    private String patternName;

    @Column(name = "address", nullable = false, length = Integer.MAX_VALUE)
    private String address;

    @Column(name = "context", length = Integer.MAX_VALUE)
    private String context;

    @Column(name = "source", length = Integer.MAX_VALUE)
    private String source;

    @Column(name = "found_time", length = Integer.MAX_VALUE)
    private String foundTime;

    @Column(name = "is_approved")
    private Boolean approved;
}