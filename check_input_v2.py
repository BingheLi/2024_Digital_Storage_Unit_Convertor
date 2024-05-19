def check_value(min_value):
    error = "Please enter a number that is more " \
            "than {}".format(min_value)

    try:
        response = float(input("Choose a number: "))

        if response < min_value:
            print(error)
        else:
            return "Success"

    except ValueError:
        print("Error: Please enter a numerical value.")


# *** Main routine ****
while True:
    result = check_value(0)
    if result == "Success":
        print("Success")
        break
