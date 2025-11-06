import pyautogui
from tkinter import Tk
from enum import Enum

class MouseEvent(Enum):
    MouseMove = 1
    MouseLeftClick = 2
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
            eventType = point[0]
            autoGuiPoint = point[2]
            if eventType == MouseEvent.MouseMove:
                pyautogui.moveTo(autoGuiPoint.x, autoGuiPoint.y, duration=0.1)
            elif eventType == MouseEvent.MouseLeftClick:
                pyautogui.click(autoGuiPoint.x, autoGuiPoint.y)
        self.parentWindow.deiconify()
        pyautogui.moveTo(self.startPosition)
