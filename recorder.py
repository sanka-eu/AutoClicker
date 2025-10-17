import keyboard
import pyautogui
from tkinter import Tk

class MouseScenarioRecorder:
    def __init__(self, parentWindow : Tk):
        self.parentWindow = parentWindow
        self.scenario = []

    def get_scenario(self):
        return self.scenario

    def start_scenario_record(self):
        self.scenario.append(pyautogui.position())
        self.parentWindow.iconify()
        self.record()

    def record(self):
        self.record_finished = False
        stop_record_hotkey = keyboard.add_hotkey("ctrl+p", self.finish_record)
        while not self.record_finished:
            self.scenario.append(pyautogui.position())
            print(pyautogui.position())
            pyautogui.sleep(0.05)
        keyboard.remove_hotkey(stop_record_hotkey)
        self.parentWindow.deiconify()

    def finish_record(self):
        self.record_finished = True

    def clear_scenario(self):
        self.scenario.clear()

    def show_scenario(self):
        for command in self.scenario:
            print(command, sep=" ")
