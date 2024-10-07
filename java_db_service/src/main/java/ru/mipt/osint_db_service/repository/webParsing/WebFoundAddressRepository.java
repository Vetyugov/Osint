package ru.mipt.osint_db_service.repository.webParsing;

import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.stereotype.Repository;
import ru.mipt.osint_db_service.model.webParsing.WebFoundAddress;

@Repository
public interface WebFoundAddressRepository extends JpaRepository<WebFoundAddress, Long> {
    @Query("select wfa from WebFoundAddress wfa order by wfa.foundTime desc")
    Page<WebFoundAddress> getAllOrderByFoundTimeDesc(Pageable pageable);
}
