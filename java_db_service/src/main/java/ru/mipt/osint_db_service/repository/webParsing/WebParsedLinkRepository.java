package ru.mipt.osint_db_service.repository.webParsing;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;
import ru.mipt.osint_db_service.model.webParsing.WebParsedLink;

@Repository
public interface WebParsedLinkRepository extends JpaRepository<WebParsedLink, Long> {
}
