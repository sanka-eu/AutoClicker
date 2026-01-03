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
