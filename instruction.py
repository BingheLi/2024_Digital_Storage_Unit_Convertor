from tkinter import *
from functools import partial  # To prevent unwanted windows
from datetime import date
from tkinter import filedialog
import re


class InstructionWindow:
    def __init__(self, parent, instructions_text):
        self.instruction_window = Toplevel(parent)
        self.instruction_window.title("Instructions")

        instructions_label = Label(self.instruction_window, text=instructions_text, font=("Arial", 12), justify=LEFT)
        instructions_label.pack(padx=20, pady=20)


class StorageConvertor:
    def __init__(self, parent):
        self.parent = parent
        self.parent.title("Digital Storage Unit Converter")

        self.all_conversions = []  # List to store conversion history

        self.frame = Frame(parent, padx=10, pady=10, bg="#FFE4E1")
        self.frame.grid()

        self.instructions_button = Button(self.frame, text="Instructions", bg="#FFD700", fg="#000000", font=("Arial", "12", "bold"), width=12, command=self.show_instructions)
        self.instructions_button.grid(row=7, column=1, columnspan=1, padx=5, pady=5)

    def show_instructions(self):
        instructions_text = (
            "1. Enter the value you want to convert in the 'Value' field.\n"
            "2. Select the unit you are converting from using the 'From' dropdown.\n"
            "3. Select the unit you are converting to using the 'To' dropdown.\n"
            "4. Click 'Convert' to perform the conversion.\n"
            "5. The result will be displayed below the 'Convert' button.\n"
            "6. Click 'Show Solution' to see detailed conversion steps.\n"
            "7. Click 'History / Export' to view and save your conversion history.\n"
            "8. Click 'History / Import' to import and convert historical data."
        )
        InstructionWindow(self.parent, instructions_text)


if __name__ == "__main__":
    root = Tk()
    app = StorageConvertor(root)
    root.mainloop()
