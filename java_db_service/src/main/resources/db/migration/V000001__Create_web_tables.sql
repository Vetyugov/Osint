-- DROP SCHEMA osint_web;

CREATE SCHEMA osint_web AUTHORIZATION osint_admin;

CREATE TABLE osint_web.web_parsed_link (
                                            id int8 NOT NULL GENERATED ALWAYS AS IDENTITY,
                                            link varchar NOT NULL,
                                            link_from varchar NULL DEFAULT '',
                                            last_monitoring_time timestamp NULL DEFAULT CURRENT_TIMESTAMP
);



CREATE TABLE osint_web.web_found_address (
                                              id int8 NOT NULL GENERATED ALWAYS AS IDENTITY,
                                              search_type varchar NULL DEFAULT 'WEB',
                                              crypto_name varchar NOT NULL,
                                              pattern_name varchar NOT NULL,
                                              address varchar NOT NULL,
                                              context varchar NULL,
                                              "source" varchar NULL,
                                              found_time timestamp NULL DEFAULT CURRENT_TIMESTAMP,
                                              is_approved bool NULL DEFAULT false
);


CREATE TABLE osint_web.web_sources_links (
                                              id int8 NOT NULL GENERATED ALWAYS AS IDENTITY,
                                              link varchar NOT NULL,
                                              analyzed_time timestamp NULL DEFAULT CURRENT_TIMESTAMP
);