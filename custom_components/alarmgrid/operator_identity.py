"""Snapshot the authenticated Home Assistant actor for history and notifications."""

from __future__ import annotations

import logging
from typing import Any

_LOGGER = logging.getLogger(__name__)
SYSTEM_OPERATOR = "Home Assistant (system/automation)"


def user_operator(user: Any) -> str:
    """Use the authenticated user's display name, never client-supplied text."""
    name = getattr(user, "name", None)
    if isinstance(name, str) and name.strip():
        return f"{name.strip()} (Home Assistant)"
    return f"Home Assistant (ID {user.id})"


async def async_context_operator(hass: Any, context: Any) -> str:
    """Resolve the action context without attributing automatic work to a user."""
    user_id = getattr(context, "user_id", None)
    if not user_id:
        return SYSTEM_OPERATOR
    try:
        user = await hass.auth.async_get_user(user_id)
    except Exception as err:
        # An auth lookup failure must not prevent acknowledging/shelving an alarm.
        _LOGGER.warning("Cannot resolve alarm operator: error=%s", type(err).__name__)
        user = None
    return user_operator(user) if user is not None else f"Home Assistant (ID {user_id})"
