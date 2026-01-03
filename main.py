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
        self.recorderController = recorder.RecorderController()
        ttk.Button(self, text="Исполнить запись", command=self.exec_scenario).pack()
        self.mouseMover = mover.MouseMover()

    def start_scenario_record(self):
        print("Запись началась")
        self.iconify()
        self.startMousePosition = pyautogui.position()

        self.recorderController.start_record()
        self.check_record_finished()

    def check_record_finished(self):
        if self.recorderController.is_threads_alive():
            self.after(50, self.check_record_finished)
            return

        pyautogui.moveTo(self.startMousePosition)
        self.deiconify()
        print("Запись завершена!")

    def exec_scenario(self):
        print("Началось исполнение записи")
        self.iconify()
        self.startMousePosition = pyautogui.position()

        self.mouseMover.exec_scenario(self.recorderController.calculate_general_scenario())

        pyautogui.moveTo(self.startMousePosition)
        self.deiconify()
        print("Закончилось исполнение записи")
    
    def take_screenshot(self):
        pyautogui.screenshot('foo.png')

def main():
    application = MainWindow()
    application.mainloop()

if __name__ == '__main__':
    main()
