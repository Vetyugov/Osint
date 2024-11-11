package ru.mipt.osint_db_service.api;

import lombok.Builder;
import lombok.Getter;
import lombok.Setter;

@Getter
@Setter
@Builder
public class WebFoundAddressDTO {

    private String address;

    private Boolean found;

    private Long links_count;

    private String state;

}