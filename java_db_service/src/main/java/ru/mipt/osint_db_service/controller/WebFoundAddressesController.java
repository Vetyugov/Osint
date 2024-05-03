package ru.mipt.osint_db_service.controller;

import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.data.domain.Page;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import ru.mipt.osint_db_service.model.webParsing.WebFoundAddress;
import ru.mipt.osint_db_service.service.webParsing.WebFoundAddressService;

@RestController
@RequestMapping("/api/v1/found_addresses")
@RequiredArgsConstructor
@Slf4j
public class WebFoundAddressesController {

    private final WebFoundAddressService webFoundAddressService;

    @GetMapping
    public Page<WebFoundAddress> getAllFoundAddresses(
            @RequestParam(name = "p", defaultValue = "1") Integer page
    ) {
        log.info("Запрос на получение списка адресов");
        if (page < 1) {
            page = 1;
        }
        Page<WebFoundAddress> all = webFoundAddressService.findAll(page);
        log.info("Найдено записей: " + all.getTotalElements());
        return all;
    }
}
