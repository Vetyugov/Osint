create table osint_web_v2.web_found_address
(
    address       varchar              not null
        constraint web_found_address_pk
            primary key,
    search_type   varchar default 'WEB'::character varying,
    crypto_name   varchar              not null,
    pattern_name  varchar              not null,
    valid_address boolean default true not null
);

alter table osint_web_v2.web_found_address
    owner to osint_admin;

create table osint_web_v2.web_found_info
(
    address     varchar not null
        constraint web_found_info_web_found_address_address_fk
            references osint_web_v2.web_found_address,
    context     varchar,
    source      varchar,
    found_time  timestamp default CURRENT_TIMESTAMP,
    is_approved boolean   default false,
    id          uuid    not null
        constraint web_found_info_pk
            primary key
);

alter table osint_web_v2.web_found_info
    owner to osint_admin;

create table osint_web_v2.web_sources_links
(
    link          varchar                   not null
        constraint web_sources_links_pk
            primary key,
    analyzed_time timestamp    default CURRENT_TIMESTAMP,
    active        boolean      default true not null,
    user_comment  varchar(255) default NULL::character varying
);

alter table osint_web_v2.web_sources_links
    owner to osint_admin;

create table osint_web_v2.web_queue_link
(
    link                 varchar not null
        constraint web_queue_link_pk
            primary key,
    source_link          varchar
        constraint web_queue_link_web_sources_links_link_fk
            references osint_web_v2.web_sources_links,
    is_analyzed          boolean default false,
    last_monitoring_time timestamp
);

alter table osint_web_v2.web_queue_link
    owner to osint_admin;

