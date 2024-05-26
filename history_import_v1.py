from tkinter import *
from functools import partial
from datetime import date
import re
from tkinter import filedialog


class StorageConvertor:
    def __init__(self, parent):
        self.parent = parent
        self.parent.title("Digital Storage Unit Converter")

        self.all_conversions = []

        self.frame = Frame(parent, padx=10, pady=10, bg="#FFE4E1")
        self.frame.grid()

        button_bg = "#FF69B4"

        self.solution = Label(self.frame, text="", bg="#FFE4E1", fg="#FF69B4")
        self.solution.grid(row=4, columnspan=2, padx=5, pady=5)

        self.current_solution = ""
        self.solution_details = []

        self.history_button = Button(self.frame, text="History / Export", bg="#FFC0CB", fg="#000000", font=("Arial", "12", "bold"), width=12, command=self.show_history)
        self.history_button.grid(row=7, column=2, columnspan=2, padx=5, pady=5)

        self.import_button = Button(self.frame, text="Import History", bg="#ADD8E6", fg="#000000", font=("Arial", "12", "bold"), width=12, command=self.import_history)
        self.import_button.grid(row=7, column=0, columnspan=2, padx=5, pady=5)

    def show_history(self):
        HistoryExport(self, self.all_conversions)

    def import_history(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if not file_path:
            return

        with open(file_path, "r") as file:
            lines = file.readlines()

        start_index = None
        for i, line in enumerate(lines):
            if line.strip() == "Here is your calculation history (oldest to newest)...":
                start_index = i + 1
                break

        if start_index is None:
            self.solution.config(text="Invalid file format.")
            return

        imported_conversions = []
        for line in lines[start_index:]:
            parts = line.strip().split("\t")
            if len(parts) == 4:
                value, from_unit, converted_value, to_unit = parts
                imported_conversions.append(f"{value} {from_unit} is {converted_value} {to_unit}")

        self.all_conversions.extend(imported_conversions)
        if len(self.all_conversions) > 50:
            self.all_conversions = self.all_conversions[-50:]

        self.solution.config(text="History imported successfully.")
        self.history_button.config(state=NORMAL)


class HistoryExport:
    def __init__(self, partner, calc_list):
        max_calcs = 50
        self.var_max_calcs = IntVar()
        self.var_max_calcs.set(max_calcs)

        self.var_filename = StringVar()
        self.var_todays_date = StringVar()
        self.var_calc_list = StringVar()

        calc_string_text = self.get_calc_string(calc_list)

        self.history_box = Toplevel()

        partner.history_button.config(state=DISABLED)

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
        partner.history_button.config(state=NORMAL)
        self.history_box.destroy()


if __name__ == "__main__":
    root = Tk()
    root.title("Digital Storage Unit Converter")
    StorageConvertor(root)
    root.mainloop()
