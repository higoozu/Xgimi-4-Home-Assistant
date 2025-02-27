import logging
from homeassistant.components.media_player import MediaPlayerEntity, DEVICE_CLASS_TV
from homeassistant.const import STATE_OFF, STATE_ON

from .pyxgimi import XgimiApi

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up the Xgimi media player from a config entry."""
    ip = config_entry.data["host"]
    token = config_entry.data["token"]
    api = XgimiApi(ip=ip, command_port=16735, advance_port=16750, alive_port=554, manufacturer_data=token)
    
    async_add_entities([XgimiMediaPlayer(api, config_entry.entry_id)])

class XgimiMediaPlayer(MediaPlayerEntity):
    """Representation of an Xgimi media player."""

    def __init__(self, api: XgimiApi, entry_id):
        """Initialize the media player."""
        self._api = api
        self._entry_id = entry_id
        self._state = STATE_OFF
        self._name = "Xgimi Projector"

    @property
    def unique_id(self):
        """Return a unique ID."""
        return f"xgimi_{self._entry_id}"

    @property
    def name(self):
        """Return the name of the device."""
        return self._name

    @property
    def state(self):
        """Return the state of the device."""
        return self._state

    @property
    def device_class(self):
        """Return the device class of the media player."""
        return DEVICE_CLASS_TV

    @property
    def supported_features(self):
        """Flag media player features that are supported."""
        from homeassistant.components.media_player.const import (
            SUPPORT_TURN_ON,
            SUPPORT_TURN_OFF,
            SUPPORT_PLAY,
            SUPPORT_PAUSE,
            SUPPORT_VOLUME_STEP,
            SUPPORT_VOLUME_MUTE,
            SUPPORT_PREVIOUS_TRACK,
            SUPPORT_NEXT_TRACK,
        )
        return (
            SUPPORT_TURN_ON
            | SUPPORT_TURN_OFF
            | SUPPORT_PLAY
            | SUPPORT_PAUSE
            | SUPPORT_VOLUME_STEP
            | SUPPORT_VOLUME_MUTE
            | SUPPORT_PREVIOUS_TRACK
            | SUPPORT_NEXT_TRACK
        )

    async def async_update(self):
        """Fetch new state data for this media player."""
        await self._api.async_fetch_data()
        self._state = STATE_ON if self._api.is_on else STATE_OFF

    async def async_turn_on(self):
        """Turn the media player on."""
        await self._api.async_send_command("poweron")
        self._state = STATE_ON

    async def async_turn_off(self):
        """Turn the media player off."""
        await self._api.async_send_command("poweroff")
        self._state = STATE_OFF

    async def async_play_media(self, media_type, media_id, **kwargs):
        """Play media."""
        await self._api.async_send_command("play")
        self._state = STATE_ON

    async def async_media_play(self):
        """Play the media player."""
        await self._api.async_send_command("play")
        self._state = STATE_ON

    async def async_media_pause(self):
        """Pause the media player."""
        await self._api.async_send_command("pause")
        self._state = STATE_ON

    async def async_volume_up(self):
        """Increase the volume."""
        await self._api.async_send_command("volumeup")

    async def async_volume_down(self):
        """Decrease the volume."""
        await self._api.async_send_command("volumedown")

    async def async_mute_volume(self, mute):
        """Mute the volume."""
        await self._api.async_send_command("volumemute")

    async def async_media_previous_track(self):
        """Send back command."""
        await self._api.async_send_command("left")

    async def async_media_next_track(self):
        """Send next command."""
        await self._api.async_send_command("right")