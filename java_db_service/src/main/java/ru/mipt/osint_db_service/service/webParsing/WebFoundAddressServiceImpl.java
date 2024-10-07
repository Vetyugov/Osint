package ru.mipt.osint_db_service.service.webParsing;

import lombok.RequiredArgsConstructor;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.stereotype.Service;
import ru.mipt.osint_db_service.model.webParsing.WebFoundAddress;
import ru.mipt.osint_db_service.repository.webParsing.WebFoundAddressRepository;

@Service
@RequiredArgsConstructor
public class WebFoundAddressServiceImpl implements WebFoundAddressService {

    private final WebFoundAddressRepository webFoundAddressRepository;
    @Override
    public Page<WebFoundAddress> findAll(Integer page) {
        return webFoundAddressRepository.getAllOrderByFoundTimeDesc(PageRequest.of(page - 1, 30));
    }
}
