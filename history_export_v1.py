from tkinter import *
from functools import partial  # To prevent unwanted windows

class SolutionWindow:
    def __init__(self, parent, solution_details):
        self.solution_window = Toplevel(parent)
        self.solution_window.title("Conversion Solution")

        for detail in solution_details:
            Label(self.solution_window, text=detail, font=("Arial", 12)).pack(padx=20, pady=5)


class StorageConvertor:
    def __init__(self, parent):
        self.parent = parent
        self.parent.title("Digital Storage Unit Converter")

        self.all_conversions = []  # List to store conversion history

        self.frame = Frame(parent, padx=10, pady=10, bg="#FFE4E1")
        self.frame.grid()

        self.value_label = Label(self.frame, text="Value:", bg="#FFE4E1", fg="#FF69B4")
        self.value_label.grid(row=0, column=0, padx=5, pady=5)

        self.value_entry = Entry(self.frame, font=("Arial", 12))
        self.value_entry.grid(row=0, column=1, padx=5, pady=5)

        self.from_label = Label(self.frame, text="From:", bg="#FFE4E1", fg="#FF69B4")
        self.from_label.grid(row=1, column=0, padx=5, pady=5)

        self.from_unit_var = StringVar()
        self.from_unit_var.set("bytes")
        self.from_unit_dropdown = OptionMenu(self.frame, self.from_unit_var,
                                             "bytes", "kilobytes", "megabytes", "gigabytes")
        self.from_unit_dropdown.grid(row=1, column=1, padx=5, pady=5)

        self.to_label = Label(self.frame, text="To:", bg="#FFE4E1", fg="#FF69B4")
        self.to_label.grid(row=2, column=0, padx=5, pady=5)

        self.to_unit_var = StringVar()
        self.to_unit_var.set("kilobytes")
        self.to_unit_dropdown = OptionMenu(self.frame, self.to_unit_var,
                                           "bytes", "kilobytes", "megabytes", "gigabytes")
        self.to_unit_dropdown.grid(row=2, column=1, padx=5, pady=5)

        button_bg = "#FF69B4"
        self.solution_button = Button(self.frame, text="Show Solution", bg=button_bg, fg="#FFFFFF",
                                      font=("Arial", 12, "bold"), width=12, command=self.show_solution, state=DISABLED)
        self.solution_button.grid(row=3, column=2, columnspan=1, padx=5, pady=5)

        self.convert_button = Button(self.frame, text="Convert", bg=button_bg, fg="#FFFFFF",
                                     font=("Arial", 12, "bold"), width=12, command=self.convert)
        self.convert_button.grid(row=3, column=0, columnspan=1, padx=5, pady=5)

        self.solution = Label(self.frame, text="", bg="#FFE4E1", fg="#FF69B4")
        self.solution.grid(row=4, columnspan=2, padx=5, pady=5)

        self.current_solution = ""
        self.solution_details = []

        self.history_button = Button(self.frame,
                                     text="Export/History",
                                     bg="#FFC0CB",
                                     fg="#000000",
                                     font=("Arial", "12", "bold"), width=12,
                                     command=self.show_history, state=DISABLED)
        self.history_button.grid(row=7, column=2, columnspan=2, padx=5, pady=5)

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

            converted_value = value_to_convert * (conversion_factors[from_unit] / conversion_factors[to_unit])
            conversion_factor = conversion_factors[from_unit] / conversion_factors[to_unit]

            if converted_value < 1e-5:
                formatted_value = "{:.5e}".format(converted_value)
            else:
                formatted_value = "{:.5f}".format(converted_value)

            self.current_solution = f"{value_to_convert} {from_unit} is {formatted_value} {to_unit}"
            self.solution.config(text=self.current_solution)
            self.solution_button.config(state=NORMAL)

            self.solution_details = [
                f"Value entered: {value_to_convert} {from_unit}",
                f"Conversion factor from {from_unit} to {to_unit}: {conversion_factor}",
                f"Converted value: {formatted_value} {to_unit}"
            ]

            # Add the current conversion to the history
            self.all_conversions.append(self.current_solution)
            self.history_button.config(state=NORMAL)

        except ValueError:
            self.solution.config(text="Invalid input. Please enter a valid number.")
            self.solution_button.config(state=DISABLED)
            self.current_solution = ""
            self.solution_details = []

    def show_solution(self):
        if self.current_solution:
            SolutionWindow(self.frame, self.solution_details)

    def show_history(self):
        HistoryExport(self, self.all_conversions)


class HistoryExport:

    def __init__(self, partner, calc_list):
        # set maximum number of calculations to display
        max_calcs = 50
        self.var_max_calcs = IntVar()
        self.var_max_calcs.set(max_calcs)

        # Function converts contents of calculation list into a string.
        calc_string_text = self.get_calc_string(calc_list)

        # setup dialogue box and background color
        self.history_box = Toplevel()

        # disable history button
        partner.history_button.config(state=DISABLED)

        # If users press cross at top, closes help and 'releases' help button
        self.history_box.protocol('WM_DELETE_WINDOW',
                                  partial(self.close_history, partner))

        self.history_frame = Frame(self.history_box, width=300, height=200)
        self.history_frame.grid()

        self.history_heading_label = Label(self.history_frame,
                                           text="History / Export",
                                           font=("Arial", "16", "bold"),
                                           width=25)
        self.history_heading_label.grid(row=0)

        # Customize text and background color for calculation area
        num_calcs = len(calc_list)

        if num_calcs > max_calcs:
            calc_background = "#FFE6CC"  # peach
            showing_all = f"Here are your recent calculations ({max_calcs}/{num_calcs} calculations shown). " \
                          f"Please export your calculations to see your full calculation history."
        else:
            calc_background = "#B4FACB"  # pale green
            showing_all = "Below is your calculation history."

        # History text and label
        hist_text = f"{showing_all}  \n\nAll calculations are shown to the nearest degree."
        self.text_instructions_label = Label(self.history_frame,
                                             text=hist_text,
                                             width=40, justify="left",
                                             wraplength=300,
                                             padx=10, pady=10)
        self.text_instructions_label.grid(row=1)

        self.all_calcs_label = Label(self.history_frame,
                                     text=calc_string_text,
                                     padx=10, pady=10, bg=calc_background,
                                     width=40, justify="left")
        self.all_calcs_label.grid(row=2)

        # Instructions for saving files
        save_text = "Either choose a custom file name (and push <Export>) or simply push <Export> to save your " \
                    "calculations in a text file. If the filename already exists, it will be overwritten!"
        self.save_instructions_label = Label(self.history_frame,
                                             text=save_text,
                                             wraplength=300,
                                             justify="left", width=40,
                                             padx=10, pady=10)
        self.save_instructions_label.grid(row=3)

        # Filename entry widget, white background to start
        self.filename_entry = Entry(self.history_frame,
                                    font=("Arial", "14"),
                                    bg="#ffffff", width=25)
        self.filename_entry.grid(row=4, padx=10, pady=10)

        self.filename_error_label = Label(self.history_frame,
                                          text="",  # Initially no error
                                          fg="#9C0000",
                                          font=("Arial", "12", "bold"))
        self.filename_error_label.grid(row=5)

        self.button_frame = Frame(self.history_frame)
        self.button_frame.grid(row=6)

        self.export_button = Button(self.button_frame,
                                    font=("Arial", "12", "bold"),
                                    text="Export", bg="#004C99",
                                    fg="#FFFFFF", width=12,
                                    command=self.export_history)
        self.export_button.grid(row=0, column=0, padx=10, pady=10)

        self.dismiss_button = Button(self.button_frame,
                                     font=("Arial", "12", "bold"),
                                     text="Dismiss", bg="#666666",
                                     fg="#FFFFFF", width=12,
                                     command=partial(self.close_history, partner))
        self.dismiss_button.grid(row=0, column=1, padx=10, pady=10)

        self.calc_list = calc_list

    def get_calc_string(self, var_calculations):
        # get maximum calculations to display (was set in __init__ function)
        max_calcs = self.var_max_calcs.get()
        calc_string = ""

        # work out how many times we need to loop to output either the last five calculations or all the calculations
        if len(var_calculations) >= max_calcs:
            stop = max_calcs
        else:
            stop = len(var_calculations)

        # iterate to all but last item, adding item and line break to calculation string
        for item in range(0, stop - 1):
            calc_string += var_calculations[len(var_calculations) - item - 1]
            calc_string += "\n"

        # add final item without an extra linebreak
        # ie: last item on list will be fifth from the end!
        calc_string += var_calculations[-stop]

        return calc_string

    def export_history(self):
        filename = self.filename_entry.get()
        if not filename:
            self.filename_error_label.config(text="Filename cannot be empty.")
            return

        if not filename.endswith(".txt"):
            filename += ".txt"

        try:
            with open(filename, 'w') as file:
                for calc in self.calc_list:
                    file.write(calc + "\n")
            self.filename_error_label.config(text="History exported successfully!", fg="green")
        except Exception as e:
            self.filename_error_label.config(text=f"Failed to export history: {e}", fg="red")

    def close_history(self, partner):
        # Put history button back to normal...
        partner.history_button.config(state=NORMAL)
        self.history_box.destroy()


if __name__ == "__main__":
    root = Tk()
    StorageConvertor(root)
    root.mainloop()
