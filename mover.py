import pyautogui

class MouseMover:
    def __init__(self):
        self.scenario = []

    def set_scenario(self, scenario : list):
        self.scenario = scenario

    def start_scenario(self):
        print("Началось исполнение записи")
        for point in self.scenario:
            pyautogui.moveTo(point.x, point.y, duration=0.1)
        print("Закончилось исполнение записи")
