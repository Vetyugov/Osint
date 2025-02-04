package ru.bitok.osint.osint_web_service.exception

class AnalyzeAlreadyStartedException() : Exception("Анализ был уже ранее запущен")
class SourceLinkNotFoundException(link:String): Exception("Не найдена родительская ссылка в бд для WebQueueLink = $link")