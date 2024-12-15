alter table osint_web_v2.web_queue_link
    add create_time timestamp default now();

alter table osint_web_v2.web_found_address
    add create_time timestamp default now();