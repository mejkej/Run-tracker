import datetime
import gspread
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('runtracker')


# WELCOME
print("Hello & Welcome to Run Tracker!")

# LOG IN OR REGISTER
while True:
    user_type = input("Login or create new account (login/new): ")
    if user_type in ['new', 'login']:
        break
    else:
        print("Invalid input. Please enter 'new' or 'login'.")

# CREATE NEW ACCOUNT
accounts = SHEET.worksheet('accounts')
if user_type == 'new':
    while True:
        username = input("Select a username (3-10 letters): ")
        if username.isalpha() and 3 <= len(username) <= 10:
            if not accounts.find(username):
                break
            else:
                print("Username already taken. Please choose another one.")
        else:
            print("Username format incorrect. Please enter 3-10 letters only.")

    while True:
        pin = input("Select pin (4-6 digits): ")
        if pin.isdigit() and 4 <= len(pin) <= 6:
            accounts.append_row([username, pin])
            # CREATING WORKSHEETS FOR NEW USERS
            SHEET.add_worksheet(title=f'{username}_profile', rows=100, cols=5)
            profile_sheet = SHEET.worksheet(f'{username}_profile')
            profile_sheet.update('A1', 'Date')
            profile_sheet.update('B1', 'Gender')
            profile_sheet.update('C1', 'Age')
            profile_sheet.update('D1', 'Weight')
            profile_sheet.update('E1', 'Height')
            SHEET.add_worksheet(title=f'{username}_runs', rows=100, cols=6)
            runs_sheet = SHEET.worksheet(f'{username}_runs')
            runs_sheet.update('A1', 'Date')
            runs_sheet.update('B1', 'Distance')
            runs_sheet.update('C1', 'Time')
            runs_sheet.update('D1', 'Avg speed')
            runs_sheet.update('E1', 'Calories burnt')
            runs_sheet.update('F1', 'Note')
            break
        else:
            print("Pin format incorrect. Please enter 4-6 digits only.")

    print("Registration succesful.")
    print("Good to have you onboard, " + username)


# LOG IN EXISTING USER
if user_type == 'login':
    while True:
        username = input("Username: ")
        pin = input("Pin: ")

        cell = accounts.find(username)

        if cell is None:
            print("Username not found.")
        else:
            row = cell.row
            values = accounts.row_values(row)

            if values[1] == pin:
                print("Welcome back, " + username)
                break
            else:
                print("Username or pin incorrect.")

        while True:
            choice = input("Try again or create a new account? (try/new): ")
            if choice in ['new', 'try']:
                break
            else:
                print("Invalid input. Please enter 'try' or 'new'.")

        if choice == 'new':
            user_type = 'new'
            break
        else:
            continue

# MAIN MENU
while True:
    print("")
    print("MAIN MENU")
    print("1. View your profile.")
    print("2. Update your profile.")
    print("3. View your runs.")
    print("4. Add to your runs.")
    print("5. Logout/Exit.")
    go_to = input("Enter number: ")

    # CREATES NEW WORKSHEETS INCASE THEY WHERE NOT FOUND
    try:
        profile_sheet = SHEET.worksheet(f'{username}_profile')
    except gspread.exceptions.WorksheetNotFound:
        SHEET.add_worksheet(title=f'{username}_profile', rows=100, cols=5)
        profile_sheet = SHEET.worksheet(f'{username}_profile')
        profile_sheet.update('A1', 'Date')
        profile_sheet.update('B1', 'Gender')
        profile_sheet.update('C1', 'Age')
        profile_sheet.update('D1', 'Weight')
        profile_sheet.update('E1', 'Height')
    try:
        runs_sheet = SHEET.worksheet(f'{username}_runs')
    except gspread.exceptions.WorksheetNotFound:
        SHEET.add_worksheet(title=f'{username}_runs', rows=100, cols=6)
        runs_sheet = SHEET.worksheet(f'{username}_runs')
        runs_sheet.update('A1', 'Date')
        runs_sheet.update('B1', 'Distance')
        runs_sheet.update('C1', 'Time')
        runs_sheet.update('D1', 'Avg speed')
        runs_sheet.update('E1', 'Calories burnt')
        runs_sheet.update('F1', 'Note')

    # 1. VIEW PROFILE
    if go_to == '1':
        while True:
            print("VIEW PROFILE")
            print("1. View last profile update.")
            print("2. View complete profile history.")
            print("3. Go back to main menu.")
            go_totwo = input("Enter number: ")
            values = profile_sheet.get_all_values()
            last_row = values[-1]

            if go_totwo == '1':
                print(values[0])
                print(values[-1])

            elif go_totwo == '2':
                print(values)

            elif go_totwo == '3':
                break
            else:
                print("Invalid input. Enter '1' '2' '3' ")
                continue

    # 2. UPDATE PROFILE
    if go_to == '2':
        while True:

            print("UPDATE PROFILE")
            current_date = datetime.date.today()
            str_date = current_date.strftime('%Y-%m-%d')

            gender = input("Enter your Gender (man/woman/other): ")
            if gender.lower() not in ['man', 'woman', 'other']:
                print("Invalid input. Enter (man/woman/other)")
                continue

            age = input("Enter your age (only digits): ")
            if not age.isdigit():
                print("Invalid input. Enter (man/woman/other)")
                continue

            weight = input("Enter your weight (in Kg only digits): ")
            if not weight.isdigit():
                print("Invalid input. Enter weight using digits only.")
                continue

            height = input("Enter your height in Cm (only digits): ")
            if not height.isdigit():
                print("Invalid input. Enter weight using digits only.")
                continue

            profile_data = [str_date, gender, age, weight, height]
            profile_sheet.append_row(profile_data)
            print("Your profile has been updated.")
            break

    # 3. VIEW RUNS
    if go_to == '3':
        while True:
            print("VIEW RUNS")
            print("1. View last updated run.")
            print("2. View complete history.")
            print("3. Go back to main menu.")
            go_to = input("Enter number: ")
            values = runs_sheet.get_all_values()
            last_row = values[-1]

            if go_to == '1':
                print(values[0])
                print(values[-1])

            elif go_to == '2':
                print(values)

            elif go_to == '3':
                break

    # 4. ADD RUN
    if go_to == '4':
        while True:
            print("ADD RUN")
    # 5. EXIT / LOG OUT
    if go_to == '5':
        print("GOOD BYE!")

