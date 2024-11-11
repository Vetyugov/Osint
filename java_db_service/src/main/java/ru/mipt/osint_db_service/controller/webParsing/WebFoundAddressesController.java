package ru.mipt.osint_db_service.controller.webParsing;

import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.data.domain.Page;
import org.springframework.web.bind.annotation.*;
import ru.mipt.osint_db_service.model.webParsing.WebFoundAddress;
import ru.mipt.osint_db_service.model.webParsing.WebFoundAddress1;
import ru.mipt.osint_db_service.service.webParsing.WebFoundAddressService;

import java.util.Optional;

@RestController
@RequestMapping("/api/v1/found_addresses")
@RequiredArgsConstructor
@Slf4j
public class WebFoundAddressesController {

    private final WebFoundAddressService webFoundAddressService;

    @GetMapping
    public Page<WebFoundAddress> getAllFoundAddresses(
            @RequestParam(name = "p", defaultValue = "1") Integer page,
            @RequestParam(name = "address", defaultValue = "") String address
    ) {
        log.info("Запрос на получение списка адресов с параметрами: p = {}, address = {}", page, address );
        if (page < 1) {
            page = 1;
        }
        Page<WebFoundAddress> all = webFoundAddressService.findAllWithFilter(page, address);
        log.info("Найдено записей: " + all.getTotalElements());
        return all;
    }

    @GetMapping("/aboutOne/{address}")
    public WebFoundAddress1 getAllInfoAboutAddress(
            @RequestParam(name = "p", defaultValue = "1") Integer page,
            @PathVariable String address) {
        log.info("Запрос на получение информации по конкретному адресу {}", address);
        if (page < 1) {
            page = 1;
        }
        Page<WebFoundAddress> all = webFoundAddressService.getInfo(page, address);
        log.info("Найдено записей для адреса {} {}: ", address, all.getTotalElements());
        Optional<WebFoundAddress> first = all.stream().findFirst();
        if(first.isPresent()){
            return WebFoundAddress1.builder().address(address).found(true).state("not confirmed").links_count(all.getTotalElements()).build();
        } else return WebFoundAddress1.builder().address(address).found(false).state("---").links_count(0L).build();
    }
}
