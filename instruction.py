from tkinter import *


# Class for displaying instructions in a new window
class InstructionWindow:
    def __init__(self, parent, instructions_text):
        # Create a new top-level window for instructions
        self.instruction_window = Toplevel(parent)
        self.instruction_window.title("Instructions")

        # Add a label to display the instructions text
        instructions_label = Label(self.instruction_window, text=instructions_text, font=("Arial", 12), justify=LEFT)
        instructions_label.pack(padx=20, pady=20)


# Main class for the digital storage unit converter application
class StorageConvertor:
    def __init__(self, parent):
        self.parent = parent
        self.parent.title("Digital Storage Unit Converter")

        self.all_conversions = []  # List to store conversion history

        # Set up the main frame
        self.frame = Frame(parent, padx=10, pady=10, bg="#FFE4E1")
        self.frame.grid()

        # Button to show instructions
        self.instructions_button = Button(self.frame, text="Instructions", bg="#FFD700", fg="#000000", font=("Arial", "12", "bold"), width=12, command=self.show_instructions)
        self.instructions_button.grid(row=7, column=1, columnspan=1, padx=5, pady=5)

    # Method to show the instructions window
    def show_instructions(self):
        # Define the instructions text
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
        # Create and show the instructions window
        InstructionWindow(self.parent, instructions_text)


# Main entry point of the application
if __name__ == "__main__":
    root = Tk()  # Create the main window
    app = StorageConvertor(root)  # Instantiate the main application
    root.mainloop()  # Start the main event loop
