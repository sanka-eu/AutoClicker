import keyboard
from pynput import mouse
import pyautogui
import datetime
from abc import ABC, abstractmethod
import copy

class MouseScenarioRecorder(ABC):
    def __init__(self):
        self.scenario = []

    def clear_scenario(self):
        self.scenario.clear()

    def show_scenario(self):
        for command in self.scenario:
            print(command, sep=" ")

    def start_scenario_record(self):
        self.prepare_for_record()
        self.record()

    def prepare_for_record(self):
        self.clear_scenario()
        self.record_finished = False

    @abstractmethod
    def record(self):
        pass

    def finish_record(self):
        self.record_finished = True

    def get_scenario(self):
        self.scenario.sort(key = lambda row: row[0])
        return copy.deepcopy(self.scenario)

class MouseMoveScenarioRecorder(MouseScenarioRecorder):
    def __init__(self):
        super().__init__()

    def record(self):
        stop_record_hotkey = keyboard.add_hotkey("ctrl+p", self.finish_record)
        while not self.record_finished:
            self.append_scenario_element()
            print(pyautogui.position())
            pyautogui.sleep(0.05)
        keyboard.remove_hotkey(stop_record_hotkey)

    def append_scenario_element(self):
        self.scenario.append([datetime.datetime.now().time(), pyautogui.position()])

class MouseClickScenarioRecorder(MouseScenarioRecorder):
    def __init__(self):
        super().__init__()

    def record(self):
        stop_record_hotkey = keyboard.add_hotkey("ctrl+p", self.finish_record)
        listener = mouse.Listener(on_click=self.on_click_handler)
        listener.start()
        while not self.record_finished:
            pyautogui.sleep(0.05)
        listener.stop()
        listener.join()

    def on_click_handler(self, x, y, button, pressed):
        self.scenario.append([datetime.datetime.now().time(), pyautogui.Point(x, y)])

import threading
import event_types

class RecorderController():
    def __init__(self):
        self.mouseMoveScenarioRecorder = MouseMoveScenarioRecorder()
        self.mouseClickScenarioRecorder = MouseClickScenarioRecorder()

    def start_record(self):
        self.start_recorders_threads()

    def start_recorders_threads(self):
        self.mouseMoveScenarioRecorderThread = threading.Thread(target=self.mouseMoveScenarioRecorder.start_scenario_record, daemon=True)
        self.mouseMoveScenarioRecorderThread.start()
        self.mouseClickScenarioRecorderThread = threading.Thread(target=self.mouseClickScenarioRecorder.start_scenario_record, daemon=True)
        self.mouseClickScenarioRecorderThread.start()

    def is_threads_alive(self):
        return self.mouseMoveScenarioRecorderThread.is_alive() or self.mouseClickScenarioRecorderThread.is_alive()

    def calculate_general_scenario(self):
        mouseMoveScenario = self.mouseMoveScenarioRecorder.get_scenario()
        for el in mouseMoveScenario:
            el.insert(0, event_types.MouseEvent.MouseMove)
        mouseClickScenario = self.mouseClickScenarioRecorder.get_scenario()
        for el in mouseClickScenario:
            el.insert(0, event_types.MouseEvent.MouseLeftClick)

        general_scenario = mouseMoveScenario + mouseClickScenario
        general_scenario.sort(key=lambda row: row[1])
        return general_scenario
