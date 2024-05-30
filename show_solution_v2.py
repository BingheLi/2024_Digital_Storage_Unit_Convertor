from tkinter import *

# Class to display the conversion solution details in a new window
class SolutionWindow:
    def __init__(self, parent, solution_details):
        # Create a new top-level window for displaying the solution details
        self.solution_window = Toplevel(parent)
        self.solution_window.title("Conversion Solution")

        # Display each detail in the solution details list using a Label
        for detail in solution_details:
            Label(self.solution_window, text=detail, font=("Arial", 12)).pack(padx=20, pady=5)

# Main class for the digital storage unit converter application
class StorageConvertor:
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
        self.solution_button = Button(self.frame, text="Show Solution", bg=button_bg, fg="#FFFFFF", font=("Arial", 12, "bold"), width=12, command=self.show_solution, state=DISABLED)
        self.solution_button.grid(row=3, column=2, columnspan=1, padx=5, pady=5)

        self.convert_button = Button(self.frame, text="Convert", bg=button_bg, fg="#FFFFFF", font=("Arial", 12, "bold"), width=12, command=self.convert)
        self.convert_button.grid(row=3, column=0, columnspan=1, padx=5, pady=5)

        # Label to display the conversion result
        self.solution = Label(self.frame, text="", bg="#FFE4E1", fg="#FF69B4")
        self.solution.grid(row=4, columnspan=2, padx=5, pady=5)

        self.current_solution = ""  # Store the current conversion result as a string
        self.solution_details = []  # Store the details of the conversion for displaying in the solution window

    # Method to perform the conversion
    def convert(self):
        from_unit = self.from_unit_var.get()
        to_unit = self.to_unit_var.get()

        value_to_convert = self.value_entry.get()
        if not value_to_convert:
            self.solution.config(text="Input field is empty. Please enter a number.")
            self.current_solution = ""
            self.solution_button.config(state=DISABLED)
            return

        try:
            value_to_convert = float(value_to_convert)
            conversion_factors = {
                "bytes": 1,
                "kilobytes": 1024,
                "megabytes": 1024 ** 2,
                "gigabytes": 1024 ** 3
            }

            # Perform the conversion
            converted_value = value_to_convert * (conversion_factors[from_unit] / conversion_factors[to_unit])
            conversion_factor = conversion_factors[from_unit] / conversion_factors[to_unit]

            # Format the converted value
            if converted_value < 1e-5:
                formatted_value = "{:.5e}".format(converted_value)
            else:
                formatted_value = "{:.5f}".format(converted_value)

            # Update the current solution and enable the solution button
            self.current_solution = f"{value_to_convert} {from_unit} is {formatted_value} {to_unit}"
            self.solution.config(text=self.current_solution)
            self.solution_button.config(state=NORMAL)

            # Store the solution details for displaying in the solution window
            self.solution_details = [
                f"Value entered: {value_to_convert} {from_unit}",
                f"Conversion factor from {from_unit} to {to_unit}: {conversion_factor}",
                f"Converted value: {formatted_value} {to_unit}"
            ]
        except ValueError:
            self.solution.config(text="Invalid input. Please enter a valid number.")
            self.solution_button.config(state=DISABLED)
            self.current_solution = ""
            self.solution_details = []

    # Method to show the conversion solution in a new window
    def show_solution(self):
        if self.current_solution:
            SolutionWindow(self.frame, self.solution_details)

# Main entry point of the application
if __name__ == "__main__":
    root = Tk()  # Create the main window
    StorageConvertor(root)  # Instantiate the main application
    root.mainloop()  # Start the main event loop
