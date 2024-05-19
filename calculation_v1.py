from tkinter import *


class CalculationGUI:
    def __init__(self, parent):
        self.parent = parent
        self.parent.title("Digital Storage Unit Converter")

        self.frame = Frame(parent, padx=10, pady=10, bg="#FFE4E1")
        self.frame.grid()

        self.from_label = Label(self.frame, text="From:", bg="#FFE4E1", fg="#FF69B4")
        self.from_label.grid(row=0, column=0, padx=5, pady=5)

        self.from_unit_var = StringVar()
        self.from_unit_var.set("bytes")
        self.from_unit_dropdown = OptionMenu(self.frame, self.from_unit_var,
                                              "bytes", "kilobytes", "megabytes", "gigabytes")
        self.from_unit_dropdown.grid(row=0, column=1, padx=5, pady=5)

        self.to_label = Label(self.frame, text="To:", bg="#FFE4E1", fg="#FF69B4")
        self.to_label.grid(row=1, column=0, padx=5, pady=5)

        self.to_unit_var = StringVar()
        self.to_unit_var.set("kilobytes")
        self.to_unit_dropdown = OptionMenu(self.frame, self.to_unit_var,
                                            "bytes", "kilobytes", "megabytes", "gigabytes")
        self.to_unit_dropdown.grid(row=1, column=1, padx=5, pady=5)

        self.convert_button = Button(self.frame, text="Convert", bg="#FF69B4", fg="#FFFFFF",
                                     font=("Arial", "12", "bold"), width=12, command=self.convert)
        self.convert_button.grid(row=2, columnspan=2, padx=5, pady=5)

    def convert(self):
        from_unit = self.from_unit_var.get()
        to_unit = self.to_unit_var.get()

        conversion_factors = {
            "bytes": 1,
            "kilobytes": 1024,
            "megabytes": 1024 ** 2,
            "gigabytes": 1024 ** 3
        }

        value_to_convert = 1287  # Example value
        converted_value = value_to_convert * (conversion_factors[from_unit] / conversion_factors[to_unit])

        result_text = f"{value_to_convert} {from_unit} is {round(converted_value, 5)} {to_unit}"
        self.result_label = Label(self.frame, text=result_text, bg="#FFE4E1", fg="#FF69B4")
        self.result_label.grid(row=3, columnspan=2, padx=5, pady=5)


if __name__ == "__main__":
    root = Tk()
    CalculationGUI(root)
    root.mainloop()
