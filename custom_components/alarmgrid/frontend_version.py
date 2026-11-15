"""Content-based versioning for the shared card and panel JavaScript bundle."""

from __future__ import annotations

from hashlib import sha256
from pathlib import Path
from typing import TYPE_CHECKING

from .const import FRONTEND_MODULE, VERSION

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant

FRONTEND_DIST = Path(__file__).parent / "frontend" / "dist"


def _frontend_module_url() -> str:
    """Fingerprint the installed bundle, including unreleased frontend fixes."""

    build = sha256((FRONTEND_DIST / "alarmgrid.js").read_bytes()).hexdigest()[:16]
    return f"{FRONTEND_MODULE}?v={VERSION}&build={build}"


async def async_get_frontend_module_url(hass: HomeAssistant) -> str:
    """Read the bundle outside the event loop; recalculate on integration setup."""

    return await hass.async_add_executor_job(_frontend_module_url)
