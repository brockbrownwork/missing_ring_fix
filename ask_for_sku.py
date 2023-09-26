import tkinter as tk
from tkinter import simpledialog
import pyautogui
import time
import keyboard

class SKUDialog:
    def __init__(self, root):
        self.root = root
        self.sku = None
        
    def show(self):
        self.sku = simpledialog.askstring("Input", "Please enter the SKU:", parent=self.root)
        return self.sku

    def make_topmost(self):
        # This will make sure the window is brought to the front
        self.root.lift()
        self.root.attributes('-topmost', True)
        self.root.after_idle(self.root.attributes, '-topmost', False)

def get_sku():
    root = tk.Tk()
    root.withdraw()  # Hides the main window

    dialog = SKUDialog(root)
    dialog.make_topmost()
    
    sku_value = dialog.show()
    
    root.destroy()
    return sku_value

if __name__ == "__main__":
    while True:
        if keyboard.is_pressed('f8'):
            print("Keystroke detected!")
            # sku = get_sku()
            sku = pyautogui.prompt(text = "hello test")
            if sku:
                print(f"You entered SKU: {sku}")
        elif keyboard.is_pressed('esc'):
            print("Exiting...")
            break
        time.sleep(0.1)  # To prevent high CPU usage
    print("Done.")
