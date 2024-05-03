package ru.mipt.osint_db_service.model;

public interface FoundAddressDto {
    String getId();
    String getSearchType();
    String getCryptoName();
    String getPatternName();
    String getAddress();
    String getContext();
    String getSource();
    String getFoundTime();
    Boolean getApproved();
}
