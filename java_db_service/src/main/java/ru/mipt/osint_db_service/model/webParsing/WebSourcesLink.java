package ru.mipt.osint_db_service.model.webParsing;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import jakarta.persistence.Table;
import lombok.Getter;
import lombok.Setter;

@Getter
@Setter
@Entity
@Table(name = "web_sources_links", schema = "osint_web")
public class WebSourcesLink {
    @Id
    @Column(name = "id", nullable = false)
    private String id;

    @Column(name = "link", nullable = false, length = Integer.MAX_VALUE)
    private String link;

    @Column(name = "analyzed_time", length = Integer.MAX_VALUE)
    private String analyzedTime;

}