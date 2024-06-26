from tkinter import *

# Class to display the conversion solution in a new window
class SolutionWindow:
    def __init__(self, parent, solution):
        # Create a new top-level window for displaying the solution
        self.solution_window = Toplevel(parent)
        self.solution_window.title("Conversion Solution")

        # Add a label to display the solution text
        Label(self.solution_window, text=solution, font=("Arial", 12)).pack(padx=20, pady=20)

# Main GUI class for the digital storage unit converter application
class CalculationGUI:
    def __init__(self, parent):
        self.parent = parent
        self.parent.title("Digital Storage Unit Converter")

        # Set up the main frame
        self.frame = Frame(parent, padx=10, pady=10, bg="#FFE4E1")
        self.frame.grid()

        # Label and entry for the value to convert
        self.value_label = Label(self.frame, text="Value:", bg="#FFE4E1", fg="#FF69B4")
        self.value_label.grid(row=0, column=0, padx=5, pady=5)

        self.value_entry = Entry(self.frame, font=("Arial", 12))
        self.value_entry.grid(row=0, column=1, padx=5, pady=5)

        # Label and dropdown for the unit to convert from
        self.from_label = Label(self.frame, text="From:", bg="#FFE4E1", fg="#FF69B4")
        self.from_label.grid(row=1, column=0, padx=5, pady=5)

        self.from_unit_var = StringVar()
        self.from_unit_var.set("bytes")
        self.from_unit_dropdown = OptionMenu(self.frame, self.from_unit_var, "bytes", "kilobytes", "megabytes", "gigabytes")
        self.from_unit_dropdown.grid(row=1, column=1, padx=5, pady=5)

        # Label and dropdown for the unit to convert to
        self.to_label = Label(self.frame, text="To:", bg="#FFE4E1", fg="#FF69B4")
        self.to_label.grid(row=2, column=0, padx=5, pady=5)

        self.to_unit_var = StringVar()
        self.to_unit_var.set("kilobytes")
        self.to_unit_dropdown = OptionMenu(self.frame, self.to_unit_var, "bytes", "kilobytes", "megabytes", "gigabytes")
        self.to_unit_dropdown.grid(row=2, column=1, padx=5, pady=5)

        # Buttons for converting and showing the solution
        button_bg = "#FF69B4"
        self.solution_button = Button(self.frame, text="Show Solution", bg=button_bg, fg="#FFFFFF", font=("Arial", 12, "bold"), width=12, command=self.show_solution)
        self.solution_button.grid(row=3, column=2, columnspan=1, padx=5, pady=5)

        self.convert_button = Button(self.frame, text="Convert", bg=button_bg, fg="#FFFFFF", font=("Arial", 12, "bold"), width=12, command=self.convert)
        self.convert_button.grid(row=3, column=0, columnspan=1, padx=5, pady=5)

    # Method to convert the value from one unit to another
    def convert(self):
        from_unit = self.from_unit_var.get()
        to_unit = self.to_unit_var.get()

        try:
            value_to_convert = float(self.value_entry.get())
        except ValueError:
            value_to_convert = 0

        # Conversion factors for different units
        conversion_factors = {
            "bytes": 1,
            "kilobytes": 1024,
            "megabytes": 1024 ** 2,
            "gigabytes": 1024 ** 3
        }

        # Perform the conversion
        converted_value = value_to_convert * (conversion_factors[from_unit] / conversion_factors[to_unit])

        # Display the solution
        solution = f"{value_to_convert} {from_unit} is {round(converted_value, 2)} {to_unit}"
        self.solution = Label(self.frame, text=solution, bg="#FFE4E1", fg="#FF69B4")
        self.solution.grid(row=4, columnspan=2, padx=5, pady=5)
        return solution

    # Method to show the solution in a new window
    def show_solution(self):
        solution = self.convert()
        SolutionWindow(self.frame, solution)

# Main entry point of the application
if __name__ == "__main__":
    root = Tk()  # Create the main window
    CalculationGUI(root)  # Instantiate the main application
    root.mainloop()  # Start the main event loop
