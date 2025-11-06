import pyautogui
from tkinter import Tk

class MouseMover:
    def __init__(self, parentWindow : Tk):
        self.parentWindow = parentWindow
        self.scenario = []

    def set_scenario(self, scenario : list):
        self.scenario = scenario

    def start_scenario(self, startPosition: pyautogui.Point):
        self.startPosition = startPosition
        self.parentWindow.iconify()
        for point in self.scenario:
            pyautogui.moveTo(point.x, point.y, duration=0.1)
        self.parentWindow.deiconify()
        pyautogui.moveTo(self.startPosition)
