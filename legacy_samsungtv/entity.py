"""Entity Base for Legacy Samsung TV."""

from __future__ import annotations

from homeassistant.const import (
    ATTR_CONNECTIONS,
    ATTR_IDENTIFIERS,
    CONF_HOST,
    CONF_MAC,
    CONF_MODEL,
    CONF_NAME,
)
from homeassistant.helpers import device_registry as dr
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.trigger import PluggableAction
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import CONF_MANUFACTURER, DOMAIN
from .coordinator import SamsungTVDataUpdateCoordinator


class SamsungTVEntity(CoordinatorEntity[SamsungTVDataUpdateCoordinator], Entity):
    """Defines a base SamsungTV entity."""

    _attr_has_entity_name = True

    def __init__(self, *, coordinator: SamsungTVDataUpdateCoordinator) -> None:
        """Initialize the SamsungTV entity."""
        super().__init__(coordinator)
        self._bridge = coordinator.bridge
        config_entry = coordinator.config_entry
        self._mac: str | None = config_entry.data.get(CONF_MAC)
        self._host: str | None = config_entry.data.get(CONF_HOST)
        # Fallback for legacy models that doesn't have a API to retrieve MAC or SerialNumber
        self._attr_unique_id = config_entry.unique_id or config_entry.entry_id
        self._attr_device_info = DeviceInfo(
            name=config_entry.data.get(CONF_NAME),
            manufacturer=config_entry.data.get(CONF_MANUFACTURER),
            model=config_entry.data.get(CONF_MODEL),
            model_id=config_entry.data.get(CONF_MODEL),
        )
        if self.unique_id:
            self._attr_device_info[ATTR_IDENTIFIERS] = {(DOMAIN, self.unique_id)}
        if self._mac:
            self._attr_device_info[ATTR_CONNECTIONS] = {
                (dr.CONNECTION_NETWORK_MAC, self._mac)
            }
        self._turn_on_action = PluggableAction(self.async_write_ha_state)

    @property
    def available(self) -> bool:
        """Return the availability of the device."""
        if self._bridge.auth_failed:
            return False
        return (
            self.coordinator.is_on
            or bool(self._turn_on_action)
            or self._mac is not None
            or self._bridge.power_off_in_progress
        )

    #    async def async_added_to_hass(self) -> None:
    #        """Connect and subscribe to dispatcher signals and state updates."""
    #        await super().async_added_to_hass()

    async def _async_turn_off(self) -> None:
        """Turn the device off."""
        await self._bridge.async_power_off()
        await self.coordinator.async_refresh()
