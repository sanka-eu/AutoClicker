import keyboard
from pynput import mouse
import pyautogui
import datetime
from tkinter import Tk
from abc import ABC, abstractmethod
import copy

class MouseScenarioRecorder(ABC):

    def show_scenario(self):
        for command in self.scenario:
            print(command, sep=" ")

    @abstractmethod
    def start_scenario_record(self):
        pass

class MouseMoveScenarioRecorder(MouseScenarioRecorder):

    def __init__(self, parentWindow : Tk):
        self.parentWindow = parentWindow
        self.scenario = []

    def start_scenario_record(self, startPosition: pyautogui.Point):
        self.startPosition = startPosition
        self.prepare_for_record()
        self.record()

    def prepare_for_record(self):
        self.scenario.append(pyautogui.position())
        self.parentWindow.iconify()
        if self.scenario:
            self.clear_scenario()
        self.record_finished = False

    def record(self):
        stop_record_hotkey = keyboard.add_hotkey("ctrl+p", self.finish_record)
        while not self.record_finished:
            self.append_scenario_element()
            print(pyautogui.position())
            pyautogui.sleep(0.05)
        keyboard.remove_hotkey(stop_record_hotkey)
        self.parentWindow.deiconify()
        pyautogui.moveTo(self.startPosition)

    def append_scenario_element(self):
        self.scenario.append([datetime.datetime.now().time(), pyautogui.position()])

    def clear_scenario(self):
        self.scenario.clear()

    def get_scenario(self):
        self.scenario.sort(key = lambda row: row[0])
        return copy.deepcopy(self.scenario)
        #return [el[1] for el in self.scenario]

    def finish_record(self):
        self.record_finished = True

class MouseClickScenarioRecorder(MouseScenarioRecorder):

    def __init__(self, parentWindow : Tk):
        self.parentWindow = parentWindow
        self.scenario = []

    def start_scenario_record(self):
        self.record_finished = False
        stop_record_hotkey = keyboard.add_hotkey("ctrl+p", self.finish_record)
        listener = mouse.Listener(on_click=self.on_click_handler)
        listener.start()
        while not self.record_finished:
            pyautogui.sleep(0.05)
        listener.join()
        keyboard.remove_hotkey(stop_record_hotkey)

    def on_click_handler(self, x, y, button, pressed):
        self.scenario.append([datetime.datetime.now().time(), pyautogui.Point(x, y)])

    def get_scenario(self):
        self.scenario.sort(key = lambda row: row[0])
        return copy.deepcopy(self.scenario)
        #return [el[1] for el in self.scenario]

    def clear_scenario(self):
        self.scenario.clear()

    def finish_record(self):
        self.record_finished = True