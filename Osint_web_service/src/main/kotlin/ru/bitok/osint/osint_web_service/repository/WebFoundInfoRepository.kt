package ru.bitok.osint.osint_web_service.repository

import org.springframework.data.jpa.repository.JpaRepository
import ru.bitok.osint.osint_web_service.entity.WebFoundInfo

interface WebFoundInfoRepository:JpaRepository<WebFoundInfo, String> {
}