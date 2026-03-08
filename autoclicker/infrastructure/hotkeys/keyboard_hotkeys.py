"""keyboard library implementation for hotkey management."""

import keyboard

from autoclicker.application.ports import HotkeyManagerPort


class KeyboardHotkeyManager(HotkeyManagerPort):
    def register(self, combination, callback):
        return keyboard.add_hotkey(combination, callback)

    def unregister(self, hotkey_id):
        if callable(hotkey_id):
            hotkey_id()
            return
        keyboard.remove_hotkey(hotkey_id)

    def capture_hotkey(self) -> str:
        return keyboard.read_hotkey(suppress=False)
