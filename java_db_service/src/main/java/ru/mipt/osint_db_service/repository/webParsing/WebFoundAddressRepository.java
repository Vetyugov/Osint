package ru.mipt.osint_db_service.repository.webParsing;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;
import ru.mipt.osint_db_service.model.webParsing.WebFoundAddress;

@Repository
public interface WebFoundAddressRepository extends JpaRepository<WebFoundAddress, Long> {
}
