from tkinter import *
from functools import partial  # To prevent unwanted windows
from datetime import date
from tkinter import filedialog
import re


class SolutionWindow:
    def __init__(self, parent, solution_details):
        self.solution_window = Toplevel(parent)
        self.solution_window.title("Conversion Solution")

        for detail in solution_details:
            Label(self.solution_window, text=detail, font=("Arial", 12)).pack(padx=20, pady=5)


class HistoryConverter:
    def __init__(self, parent):
        self.parent = parent
        self.parent.title("History Import, Conversion, and Export")

        self.frame = Frame(parent, padx=10, pady=10, bg="#FFE4E1")
        self.frame.grid()

        self.unit_var = StringVar()
        self.unit_var.set("bytes")

        self.file_path = None
        self.conversions = []

        self.import_button = Button(self.frame, text="Import History", bg="#ADD8E6", fg="#000000", font=("Arial", "12", "bold"), width=20, command=self.import_history)
        self.import_button.grid(row=0, column=0, padx=5, pady=5)

        self.unit_dropdown = OptionMenu(self.frame, self.unit_var, "bytes", "kilobytes", "megabytes", "gigabytes")
        self.unit_dropdown.grid(row=0, column=1, padx=5, pady=5)

        self.convert_and_export_button = Button(self.frame, text="Convert and Export", bg="#4CAF50", fg="#FFFFFF", font=("Arial", "12", "bold"), width=20, command=self.convert_and_export)
        self.convert_and_export_button.grid(row=0, column=2, padx=5, pady=5)

        self.history_label = Label(self.frame, text="Imported History:", font=("Arial", 12, "bold"), bg="#FFE4E1")
        self.history_label.grid(row=1, columnspan=3, pady=5)

        self.history_text = Text(self.frame, height=10, width=50, state=DISABLED)
        self.history_text.grid(row=2, columnspan=3, padx=5, pady=5)

    def import_history(self):
        self.file_path = filedialog.askopenfilename()

        if not self.file_path:
            return

        try:
            with open(self.file_path, "r") as file:
                lines = file.readlines()

            self.conversions.clear()
            self.process_lines(lines)

            self.history_text.config(state=NORMAL)
            self.history_text.delete(1.0, END)
            for conv in self.conversions:
                self.history_text.insert(END, conv + "\n")
            self.history_text.config(state=DISABLED)

        except Exception as e:
            print(f"Error importing history: {str(e)}")

    def process_lines(self, lines):
        target_unit = self.unit_var.get()
        conversion_factors = {
            "bytes": 1,
            "kilobytes": 1024,
            "megabytes": 1024 ** 2,
            "gigabytes": 1024 ** 3
        }
        for line in lines:
            if not line.startswith("****") and not line.startswith("Generated") and not line.startswith("Here"):
                parts = line.split()
                if len(parts) >= 4:
                    value = float(parts[0])
                    from_unit = parts[1]
                    converted_value = value * (conversion_factors[from_unit] / conversion_factors[target_unit])
                    formatted_value = "{:.5f}".format(converted_value) if converted_value >= 1e-5 else "{:.5e}".format(converted_value)
                    self.conversions.append(f"{value}\t{from_unit}\t{formatted_value}\t{target_unit}")

    def convert_and_export(self):
        if not self.file_path:
            print("No file selected. Please import a history file first.")
            return

        try:
            filename = filedialog.asksaveasfilename(defaultextension=".txt")
            if not filename:
                return

            with open(self.file_path, "r") as file:
                lines = file.readlines()

            self.conversions.clear()
            self.process_lines(lines)

            with open(filename, "w") as file:
                heading = "**** Digital Storage Calculations ****\n"
                generated_date = f"Generated: {self.get_date()}\n"
                sub_heading = "Here is your calculation history (oldest to newest)...\n"
                file.write(heading)
                file.write(generated_date)
                file.write(sub_heading)

                for conv in self.conversions:
                    file.write(conv + "\n")

            print("History converted and exported successfully.")

        except Exception as e:
            print(f"Error converting and exporting history: {str(e)}")

    @staticmethod
    def get_date():
        today = date.today()
        return today.strftime("%d/%m/%Y")


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
        self.from_unit_dropdown = OptionMenu(self.frame, self.from_unit_var, "bytes", "kilobytes", "megabytes", "gigabytes")
        self.from_unit_dropdown.grid(row=1, column=1, padx=5, pady=5)

        self.to_label = Label(self.frame, text="To:", bg="#FFE4E1", fg="#FF69B4")
        self.to_label.grid(row=2, column=0, padx=5, pady=5)

        self.to_unit_var = StringVar()
        self.to_unit_var.set("kilobytes")
        self.to_unit_dropdown = OptionMenu(self.frame, self.to_unit_var, "bytes", "kilobytes", "megabytes", "gigabytes")
        self.to_unit_dropdown.grid(row=2, column=1, padx=5, pady=5)

        button_bg = "#FF69B4"
        self.solution_button = Button(self.frame, text="Show Solution", bg=button_bg, fg="#FFFFFF", font=("Arial", 12, "bold"), width=12, command=self.show_solution, state=DISABLED)
        self.solution_button.grid(row=3, column=2, columnspan=1, padx=5, pady=5)

        self.convert_button = Button(self.frame, text="Convert", bg=button_bg, fg="#FFFFFF", font=("Arial", 12, "bold"), width=12, command=self.convert)
        self.convert_button.grid(row=3, column=0, columnspan=1, padx=5, pady=5)

        self.solution = Label(self.frame, text="", bg="#FFE4E1", fg="#FF69B4",font=("Arial", 12, "bold"))
        self.solution.grid(row=4, columnspan=5, padx=5, pady=5)

        self.current_solution = ""
        self.solution_details = []

        self.history_export_button = Button(self.frame, text="History / Export", bg="#FFC0CB", fg="#000000", font=("Arial", "12", "bold"), width=12, command=self.show_history, state=DISABLED)
        self.history_export_button.grid(row=7, column=2, columnspan=2, padx=5, pady=5)

        self.history_import_button = Button(self.frame, text="History / Import", bg="#ADD8E6", fg="#000000", font=("Arial", "12", "bold"), width=12, command=self.open_history_converter)
        self.history_import_button.grid(row=7, column=0, columnspan=1, padx=5, pady=5)

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
            # Keep only the last 50 conversions
            if len(self.all_conversions) > 50:
                self.all_conversions.pop(0)

            self.history_export_button.config(state=NORMAL)

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

    def open_history_converter(self):
        history_converter_window = Toplevel(self.parent)
        history_converter_app = HistoryConverter(history_converter_window)


class HistoryExport:

    def __init__(self, partner, calc_list):
        # set maximum number of calculations to 50
        max_calcs = 50
        self.var_max_calcs = IntVar()
        self.var_max_calcs.set(max_calcs)

        # Set variables to hold filename and date
        # for when writing to file
        self.var_filename = StringVar()
        self.var_todays_date = StringVar()
        self.var_calc_list = StringVar()

        # Function converts contents of calculation list
        # into a string.
        calc_string_text = self.get_calc_string(calc_list)

        # setup dialogue box and background colour
        self.history_box = Toplevel()

        partner.history_export_button.config(state=DISABLED)

        self.history_box.protocol('WM_DELETE_WINDOW', partial(self.close_history, partner))

        self.history_frame = Frame(self.history_box, width=300, height=200)
        self.history_frame.grid()

        self.history_heading_label = Label(self.history_frame, text="History / Export", font=("Arial", "16", "bold"), width=25)
        self.history_heading_label.grid(row=0)

        num_calcs = len(calc_list)

        if num_calcs > max_calcs:
            calc_background = "#FFE6CC"
            showing_all = f"Here are your recent calculations ({max_calcs}/{num_calcs} calculations shown). Please export your calculations to see your full calculation history."
        else:
            calc_background = "#B4FACB"
            showing_all = "Below is your conversion history."

        hist_text = f"{showing_all}  \n\nAll conversion are shown to the nearest 5 decimal places or scientific figures."
        self.text_instructions_label = Label(self.history_frame, text=hist_text, width=40, justify="left", wraplength=300, padx=10, pady=10)
        self.text_instructions_label.grid(row=1)

        self.all_calcs_label = Label(self.history_frame, text=calc_string_text, padx=10, pady=10, bg=calc_background, width=40, justify="left")
        self.all_calcs_label.grid(row=2)

        save_text = "Either choose a custom file name (and push <Export>) or simply push <Export> to save your calculations in a text file. If the filename already exists, it will be overwritten!"
        self.save_instructions_label = Label(self.history_frame, text=save_text, wraplength=300, justify="left", width=40, padx=10, pady=10)
        self.save_instructions_label.grid(row=3)

        self.filename_entry = Entry(self.history_frame, font=("Arial", "14"), bg="#ffffff", width=25)
        self.filename_entry.grid(row=4, padx=10, pady=10)

        self.filename_feedback_label = Label(self.history_frame, text="", fg="#9C0000", wraplength=300, font=("Arial", "12", "bold"))
        self.filename_feedback_label.grid(row=5)

        self.button_frame = Frame(self.history_frame)
        self.button_frame.grid(row=6)

        self.export_button = Button(self.button_frame, font=("Arial", "12", "bold"), text="Export", bg="#004C99", fg="#FFFFFF", width=12, command=self.make_file)
        self.export_button.grid(row=0, column=0, padx=10, pady=10)

        self.dismiss_button = Button(self.button_frame, font=("Arial", "12", "bold"), text="Dismiss", bg="#666666", fg="#FFFFFF", width=12, command=partial(self.close_history, partner))
        self.dismiss_button.grid(row=0, column=1, padx=10, pady=10)

    def get_calc_string(self, var_calculations):
        max_calcs = self.var_max_calcs.get()
        calc_string = ""

        oldest_first = ""
        for item in var_calculations:
            oldest_first += item
            oldest_first += "\n"

        self.var_calc_list.set(oldest_first)

        if len(var_calculations) >= max_calcs:
            stop = max_calcs
        else:
            stop = len(var_calculations)

        for item in range(0, stop):
            calc_string += var_calculations[len(var_calculations) - item - 1]
            calc_string += "\n"

        calc_string = calc_string.strip()
        return calc_string

    def make_file(self):
        filename = self.filename_entry.get()

        filename_ok = ""
        date_part = self.get_date()

        if filename == "":
            filename = "{}_storage_calculations".format(date_part)
        else:
            filename_ok = self.check_filename(filename)

        if filename_ok == "":
            filename += ".txt"
            success = "Your calculations have been saved (filename: {}).".format(filename)
            self.var_filename.set(filename)
            self.filename_feedback_label.config(text=success, fg="dark green")
            self.filename_entry.config(bg="#FFFFFF")

            self.write_to_file()
        else:
            self.filename_feedback_label.config(text=filename_ok, fg="dark red")
            self.filename_entry.config(bg="#F8CECC")

    def get_date(self):
        today = date.today()
        day = today.strftime("%d")
        month = today.strftime("%m")
        year = today.strftime("%Y")

        todays_date = "{}/{}/{}".format(day, month, year)
        self.var_todays_date.set(todays_date)

        return "{}_{}_{}".format(year, month, day)

    @staticmethod
    def check_filename(filename):
        problem = ""
        valid_char = "[A-Za-z0-9_]"

        for letter in filename:
            if re.match(valid_char, letter):
                continue
            elif letter == " ":
                problem = "Sorry, no spaces allowed"
            else:
                problem = "Sorry, no {}'s allowed".format(letter)
            break

        if problem != "":
            problem = "{}. Use letters/numbers/underscores only.".format(problem)

        return problem

    def write_to_file(self):
        filename = self.var_filename.get()
        generated_date = self.var_todays_date.get()

        heading = "**** Digital Storage Calculations ****\n"
        generated = "Generated: {}\n".format(generated_date)
        sub_heading = "Here is your calculation history (oldest to newest)...\n"
        all_calculations = self.var_calc_list.get()

        to_output_list = [heading, generated, sub_heading]

        for calculation in all_calculations.split('\n'):
            if calculation:
                parts = calculation.split()
                if len(parts) >= 5:
                    value = parts[0]
                    from_unit = parts[1]
                    to_value = parts[3]
                    to_unit = parts[4]
                    row = f"{value}\t{from_unit}\t{to_value}\t{to_unit}\n"
                    to_output_list.append(row)

        with open(filename, "w") as text_file:
            text_file.writelines(to_output_list)

    def close_history(self, partner):
        partner.history_export_button.config(state=NORMAL)
        self.history_box.destroy()


if __name__ == "__main__":
    root = Tk()
    root.title("Digital Storage Unit Converter")
    StorageConvertor(root)
    root.mainloop()
