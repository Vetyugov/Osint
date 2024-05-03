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
@Table(name = "web_parsed_link", schema = "osint_web")
public class WebParsedLink {
    @Id
    @Column(name = "id", nullable = false)
    private String id;

    @Column(name = "link", nullable = false, length = Integer.MAX_VALUE)
    private String link;

    @Column(name = "link_from", length = Integer.MAX_VALUE)
    private String linkFrom;

    @Column(name = "last_monitoring_time", length = Integer.MAX_VALUE)
    private String lastMonitoringTime;

}