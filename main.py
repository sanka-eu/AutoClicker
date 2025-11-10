import mover
import recorder

import pyautogui
import pyscreeze
from tkinter import *
from tkinter import ttk
import threading
class MainWindow(Tk):
    def __init__(self):
        super().__init__()
        self.applicationName = "AutoClicker"
        self.title(self.applicationName)
        self.geometry('300x300')
        ttk.Button(self, text="Начать запись", command=self.start_scenario_record).pack()
        self.mouseMoveScenarioRecorder = recorder.MouseMoveScenarioRecorder(self)
        self.mouseClickScenarioRecorder = recorder.MouseClickScenarioRecorder(self)
        ttk.Button(self, text="Исполнить запись", command=self.exec_scenario).pack()
        self.mouseMover = mover.MouseMover(self)

    def start_scenario_record(self):
        print("Запись началась")
        self.mouseMoveScenarioRecorderThread = threading.Thread(target=self.mouseMoveScenarioRecorder.start_scenario_record, args=[pyautogui.position()], daemon=True)
        self.mouseMoveScenarioRecorderThread.start()
        self.mouseClickScenarioRecorderThread = threading.Thread(target=self.mouseClickScenarioRecorder.start_scenario_record, daemon=True)
        self.mouseClickScenarioRecorderThread.start()

        self.check_threads_finished()

    def check_threads_finished(self):
        if (self.mouseMoveScenarioRecorderThread.is_alive() or
            self.mouseClickScenarioRecorderThread.is_alive()):
            self.after(50, self.check_threads_finished)
            return

        print("Запись завершена!")

    def calculate_general_scenario(self):
        mouseMoveScenario = self.mouseMoveScenarioRecorder.get_scenario()
        for el in mouseMoveScenario:
            el.insert(0, mover.MouseEvent.MouseMove)
        mouseClickScenario = self.mouseClickScenarioRecorder.get_scenario()
        for el in mouseClickScenario:
            el.insert(0, mover.MouseEvent.MouseLeftClick)

        general_scenario = mouseMoveScenario + mouseClickScenario
        general_scenario.sort(key=lambda row: row[1])
        return general_scenario

    def exec_scenario(self):
        print("Началось исполнение записи")
        current_scenario = self.calculate_general_scenario()
        print(current_scenario)
        self.mouseMover.set_scenario(current_scenario)
        #self.mouseMoveScenarioRecorder.show_scenario()
        self.mouseMover.start_scenario(pyautogui.position())
        print("Закончилось исполнение записи")
    
    def take_screenshot(self):
        pyautogui.screenshot('foo.png')

def main():
    application = MainWindow()
    application.mainloop()

if __name__ == '__main__':
    main()
