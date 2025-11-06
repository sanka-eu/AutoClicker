import mover
import recorder

import pyautogui
import pyscreeze
from tkinter import *
from tkinter import ttk

class MainWindow(Tk):
    def __init__(self):
        super().__init__()
        self.applicationName = "AutoClicker"
        self.title(self.applicationName)
        self.geometry('300x300')
        ttk.Button(self, text="Начать запись", command=self.start_scenario_record).pack()
        self.mouseScenarioRecorder = recorder.MouseScenarioRecorder(self)
        ttk.Button(self, text="Исполнить запись", command=self.exec_scenario).pack()
        self.mouseMover = mover.MouseMover(self)

    def start_scenario_record(self):
        print("Запись началась")
        self.mouseScenarioRecorder.start_scenario_record(pyautogui.position())
        print("Запись завершена!")

    def exec_scenario(self):
        print("Началось исполнение записи")
        self.mouseMover.set_scenario(self.mouseScenarioRecorder.get_scenario())
        self.mouseScenarioRecorder.show_scenario()
        self.mouseMover.start_scenario(pyautogui.position())
        print("Закончилось исполнение записи")
    
    def take_screenshot(self):
        pyautogui.screenshot('foo.png')

def main():
    application = MainWindow()
    application.mainloop()

if __name__ == '__main__':
    main()