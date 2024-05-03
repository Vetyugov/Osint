package ru.mipt.osint_db_service.service.webParsing;

import org.springframework.data.domain.Page;
import ru.mipt.osint_db_service.model.webParsing.WebFoundAddress;

public interface WebFoundAddressService {
    Page<WebFoundAddress> findAll(Integer page);
}
