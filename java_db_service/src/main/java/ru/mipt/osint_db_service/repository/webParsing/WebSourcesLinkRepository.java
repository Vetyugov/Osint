package ru.mipt.osint_db_service.repository.webParsing;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;
import ru.mipt.osint_db_service.model.webParsing.WebSourcesLink;

@Repository
public interface WebSourcesLinkRepository extends JpaRepository<WebSourcesLink, Long> {
}
