import pyautogui
import event_types

class MouseMover:
    def exec_scenario(self, scenario : list):
        for point in scenario:
            eventType = point[0]
            autoGuiPoint = point[2]
            if eventType == event_types.MouseEvent.MouseMove:
                pyautogui.moveTo(autoGuiPoint.x, autoGuiPoint.y, duration=0.1)
            elif eventType == event_types.MouseEvent.MouseLeftClick:
                pyautogui.click(autoGuiPoint.x, autoGuiPoint.y)
