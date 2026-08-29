"""Small shared translation table for Telegram alarm notifications."""

from __future__ import annotations

from typing import Any

_TEXT = {
    "en": {
        "event_activated": "ACTIVATED", "event_cleared": "CLEARED",
        "event_acknowledged": "ACKNOWLEDGED", "event_shelved": "SHELVED",
        "event_unshelved": "UNSHELVED", "event_disabled": "DISABLED",
        "event_enabled": "ENABLED", "priority_critical": "CRITICAL",
        "priority_high": "HIGH", "priority_medium": "MEDIUM",
        "priority_low": "LOW", "priority_info": "INFO", "priority_status": "STATUS",
        "field_priority": "Priority", "field_area": "Area", "field_system": "System",
        "field_tag": "Tag", "field_state": "State", "field_value": "Value",
        "field_operator": "Operator", "field_reason": "Reason", "field_time": "Time",
        "alarm": "Alarm", "ack": "Acknowledge", "shelve": "Suspend",
        "disable": "Disable", "enable": "Enable", "unshelve": "Unshelve now",
        "confirm": "Confirm", "cancel": "Cancel", "cancelled": "Cancelled",
        "ack_ok": "Alarm acknowledged", "shelve_ok": "Alarm suspended",
        "shelve_until": "Alarm suspended until {time}", "disable_ok": "Alarm disabled",
        "enable_ok": "Alarm enabled", "unshelve_ok": "Alarm unshelved",
        "expired": "Action expired", "unavailable": "Action no longer available",
        "choose": "Suspend for:", "disable_q": "Disable this alarm?",
        "duration_15": "15 min", "duration_60": "1 hour", "duration_240": "4 hours",
        "duration_480": "8 hours", "duration_1440": "1 day",
        "duration_4320": "3 days", "duration_10080": "7 days",
    },
    "it": {
        "event_activated": "ALLARME ATTIVO", "event_cleared": "RIENTRATO",
        "event_acknowledged": "RICONOSCIUTO", "event_shelved": "SOSPESO",
        "event_unshelved": "RIATTIVATO", "event_disabled": "DISABILITATO",
        "event_enabled": "ABILITATO", "priority_critical": "CRITICA",
        "priority_high": "ALTA", "priority_medium": "MEDIA", "priority_low": "BASSA",
        "priority_info": "INFO", "priority_status": "STATO",
        "field_priority": "Priorità", "field_area": "Area", "field_system": "Sistema",
        "field_tag": "Tag", "field_state": "Stato", "field_value": "Valore",
        "field_operator": "Operatore", "field_reason": "Motivo", "field_time": "Ora",
        "alarm": "Allarme", "ack": "Riconosci", "shelve": "Sospendi",
        "disable": "Disabilita", "enable": "Abilita", "unshelve": "Riattiva ora",
        "confirm": "Conferma", "cancel": "Annulla", "cancelled": "Annullato",
        "ack_ok": "Allarme riconosciuto", "shelve_ok": "Allarme sospeso",
        "shelve_until": "Allarme sospeso fino alle {time}",
        "disable_ok": "Allarme disabilitato", "enable_ok": "Allarme abilitato",
        "unshelve_ok": "Allarme riattivato", "expired": "Azione scaduta",
        "unavailable": "Azione non più disponibile", "choose": "Sospendi per:",
        "disable_q": "Disabilitare questo allarme?", "duration_15": "15 min",
        "duration_60": "1 ora", "duration_240": "4 ore", "duration_480": "8 ore",
        "duration_1440": "1 giorno", "duration_4320": "3 giorni",
        "duration_10080": "7 giorni",
    },
}


def telegram_language(hass: Any) -> str:
    """Return a supported language from Home Assistant configuration."""
    return normalize_telegram_language(getattr(hass.config, "language", "en"))


def normalize_telegram_language(language: str | None) -> str:
    """Normalize supported locale variants and fall back to English."""
    return "it" if str(language or "en").lower().startswith("it") else "en"


def telegram_text(language: str, key: str) -> str:
    """Translate one Telegram UI key with an English fallback."""
    language = normalize_telegram_language(language)
    return _TEXT[language].get(key, _TEXT["en"].get(key, key))
