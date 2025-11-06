import keyboard
import pyautogui
import datetime
from tkinter import Tk
from abc import ABC, abstractmethod

class ScenarioRecorder(ABC):
    def __init__(self, parentWindow : Tk):
        self.parentWindow = parentWindow
        self.scenario = []

    def clear_scenario(self):
        self.scenario.clear()

    def show_scenario(self):
        for command in self.scenario:
            print(command, sep=" ")

    @abstractmethod
    def get_scenario(self):
        pass

    @abstractmethod
    def start_scenario_record(self):
        pass

class MouseScenarioRecorder(ScenarioRecorder):
    def __init__(self, parentWindow : Tk):
        self.parentWindow = parentWindow
        self.scenario = []

    def get_scenario(self):
        self.scenario.sort(key = lambda row: row[0])
        return [el[1] for el in self.scenario]

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
            self.scenario.append([datetime.datetime.now().time(), pyautogui.position()])
            print(pyautogui.position())
            pyautogui.sleep(0.05)
        keyboard.remove_hotkey(stop_record_hotkey)
        self.parentWindow.deiconify()
        pyautogui.moveTo(self.startPosition)

    def finish_record(self):
        self.record_finished = True
