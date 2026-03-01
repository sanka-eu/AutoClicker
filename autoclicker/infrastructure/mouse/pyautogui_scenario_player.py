"""Scenario playback through PyAutoGUI."""

import time

import pyautogui

from autoclicker.application.ports import ScenarioPlayerPort
from autoclicker.domain import MouseEventType, Scenario


class PyAutoGuiScenarioPlayer(ScenarioPlayerPort):
    def __init__(self, speed_multiplier: float = 1.0, loop_playback: bool = False) -> None:
        if speed_multiplier <= 0:
            raise ValueError("speed_multiplier must be > 0")
        self._speed_multiplier = speed_multiplier
        self._loop_playback = loop_playback

    def play(self, scenario: Scenario, should_stop=None) -> None:
        if not scenario:
            return

        events = sorted(scenario, key=lambda event: event.timestamp)
        while True:
            if self._should_stop(should_stop):
                return
            self._play_once(events, should_stop)
            if self._should_stop(should_stop) or not self._loop_playback:
                return

    def _play_once(self, events, should_stop) -> None:
        base_timestamp = events[0].timestamp
        started_at = time.perf_counter()

        offsets = [
            (event.timestamp - base_timestamp) / self._speed_multiplier for event in events
        ]

        for index, event in enumerate(events):
            if self._should_stop(should_stop):
                return
            if not self._sleep_until(started_at, offsets[index], should_stop):
                return

            if event.event_type == MouseEventType.MOVE:
                pyautogui.moveTo(event.x, event.y)
            elif event.event_type == MouseEventType.LEFT_CLICK:
                pyautogui.click(event.x, event.y, button="left")

    @staticmethod
    def _sleep_until(started_at: float, target_offset: float, should_stop) -> bool:
        while True:
            if PyAutoGuiScenarioPlayer._should_stop(should_stop):
                return False
            elapsed = time.perf_counter() - started_at
            wait_time = target_offset - elapsed
            if wait_time <= 0:
                return True
            time.sleep(min(wait_time, 0.01))

    @staticmethod
    def _should_stop(should_stop) -> bool:
        return bool(should_stop and should_stop())
