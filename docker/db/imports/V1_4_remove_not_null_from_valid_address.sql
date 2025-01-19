alter table osint_web_v2.web_found_address
    alter column valid_address drop not null;

alter table osint_web_v2.web_found_address
    alter column valid_address set default null;