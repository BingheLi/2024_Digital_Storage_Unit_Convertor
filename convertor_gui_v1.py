from tkinter import *

# Main class for the storage unit converter GUI.
class StorageConverter:

    def __init__(self):
        # Set up the main frame.
        self.storage_frame = Frame(padx=10, pady=10, bg="#FFE4E1")
        self.storage_frame.grid()

        # Heading label for the GUI.
        self.storage_heading = Label(self.storage_frame,
                                     text="Digital Storage Unit Converter",
                                     font=("Arial", "16", "bold"),
                                     bg="#FFE4E1",
                                     fg="#FF69B4")
        self.storage_heading.grid(row=0, columnspan=2, pady=(0, 10))

        # Instructions label.
        instructions = "Please enter a value below and select the units to convert from and to."
        self.storage_instructions = Label(self.storage_frame,
                                          text=instructions,
                                          wrap=250, width=40,
                                          justify="left",
                                          bg="#FFE4E1",
                                          fg="#FF69B4")
        self.storage_instructions.grid(row=1, columnspan=2, pady=(0, 10))

        # Entry widget for input value.
        self.storage_entry = Entry(self.storage_frame,
                                   font=("Arial", "14"))
        self.storage_entry.grid(row=2, column=0, padx=5, pady=5, sticky="we")

        # Output label to display error messages.
        error = "Please enter a number"
        self.output_label = Label(self.storage_frame, text="",
                                  fg="#FF69B4",
                                  bg="#FFE4E1")
        self.output_label.grid(row=3, columnspan=2)


# Main routine to run the application.
if __name__ == "__main__":
    root = Tk()
    root.title("Digital Storage Unit Converter")
    StorageConverter()
    root.mainloop()
