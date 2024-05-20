from tkinter import *


class StorageConverter:

    def __init__(self):

        # Set up GUI Frame
        self.storage_frame = Frame(padx=10, pady=10, bg="#FFE4E1")
        self.storage_frame.grid()

        self.storage_heading = Label(self.storage_frame,
                                     text="Digital Storage Unit Converter",
                                     font=("Arial", "16", "bold"),
                                     bg="#FFE4E1",
                                     fg="#FF69B4")
        self.storage_heading.grid(row=0, columnspan=4, pady=(0, 10))

        instructions = "Please enter a value below and " \
                       "select the units to convert from and to."
        self.storage_instructions = Label(self.storage_frame,
                                          text=instructions,
                                          wrap=250, width=40,
                                          justify="left",
                                          bg="#FFE4E1",
                                          fg="#FF69B4")
        self.storage_instructions.grid(row=1, columnspan=4, pady=(0, 10))

        self.value_entry = Entry(self.storage_frame,
                                   font=("Arial", "14"))
        self.value_entry.grid(row=2, column=0, padx=5, pady=5, sticky="we", columnspan=2)

        self.from_unit_label = Label(self.storage_frame, text="From:", bg="#FFE4E1", fg="#FF69B4")
        self.from_unit_label.grid(row=3, column=0, padx=5, pady=5, sticky=W)

        self.from_unit_var = StringVar()
        self.from_unit_var.set("bytes")
        self.from_unit_dropdown = OptionMenu(self.storage_frame, self.from_unit_var,
                                              "bytes", "kilobytes", "megabytes", "gigabytes")
        self.from_unit_dropdown.grid(row=3, column=1, padx=5, pady=5, sticky=W)

        self.to_unit_label = Label(self.storage_frame, text="To:", bg="#FFE4E1", fg="#FF69B4")
        self.to_unit_label.grid(row=4, column=0, padx=5, pady=5, sticky=W)

        self.to_unit_var = StringVar()
        self.to_unit_var.set("kilobytes")
        self.to_unit_dropdown = OptionMenu(self.storage_frame, self.to_unit_var,
                                            "bytes", "kilobytes", "megabytes", "gigabytes")
        self.to_unit_dropdown.grid(row=4, column=1, padx=5, pady=5, sticky=W)

        error = "Please enter a number"
        self.output_label = Label(self.storage_frame, text="",
                                  fg="#FF69B4",
                                  bg="#FFE4E1")
        self.output_label.grid(row=5, columnspan=4)

        # Buttons
        button_bg = "#FF69B4"
        self.history_button = Button(self.storage_frame,
                                      text="Export/History",
                                      bg="#FFC0CB",
                                      fg="#000000",
                                      font=("Arial", "12", "bold"), width=12)
        self.history_button.grid(row=7,column=2, columnspan=2, padx=5, pady=5)

        self.clear_button = Button(self.storage_frame,
                                   text="Clear",
                                   bg=button_bg,
                                   fg="#FFFFFF",
                                   font=("Arial", "12", "bold"), width=12)
        self.clear_button.grid(row=2, column=2, padx=5, pady=5)

        self.convert_button = Button(self.storage_frame,
                                     text="Convert",
                                     bg=button_bg,
                                     fg="#FFFFFF",
                                     font=("Arial", "12", "bold"), width=12)
        self.convert_button.grid(row=6, columnspan=1, padx=5, pady=5)

        self.solution_button = Button(self.storage_frame,
                                      text="Show Solution",
                                      bg=button_bg,
                                      fg="#FFFFFF",
                                      font=("Arial", "12", "bold"), width=12)
        self.solution_button.grid(row=6,column=2, columnspan=2, padx=5, pady=5)


# main routine
if __name__ == "__main__":
    root = Tk()
    root.title("Digital Storage Unit Converter")
    StorageConverter()
    root.mainloop()
