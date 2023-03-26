import datetime
import re
import sys
import gspread
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]
# CREDS SAME CODE AS USED IN THE LOVE SANDWICHES
CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)

# OPEN RUN TRACKER MAIN SHEET
SHEET = GSPREAD_CLIENT.open('runtracker')


# EXIT PROGRAM FUNCTION
def exit_program():
    print("GOOD BYE!")
    sys.exit()


# WELCOME
print("Hello & Welcome to Run Tracker!")
print("Enter 'exit' at any time to quit the program.")

# LOG IN OR REGISTER
while True:
    user_type = input("Login or create new account (login/new): ")
    if user_type in ['new', 'login']:
        break
    elif user_type == 'exit':
        exit_program()
    else:
        print("Invalid input. Please enter 'new' or 'login'.")

# CREATE NEW ACCOUNT
accounts = SHEET.worksheet('accounts')
if user_type == 'new':
    while True:
        # CHECKING USERNAMES LENGHT & THAT IT ONLY CONTAINS LETTERS
        username = input("Select a username (3-10 letters): ")
        if not username.isalpha() and 3 <= len(username) <= 10:
            print("Invalid input. 3-10 Letters only.")
            continue
        elif accounts.find(username):
            print("Username already taken. Please choose another one.")
            continue
        elif username == 'exit':
            exit_program()

        pin = input("Select pin (4-6 digits): ")
        if not pin.isdigit() and 4 <= len(pin) <= 6:
            print("Invalid input. 4-6 Digits Ex: '9999', '5555', '123451'.")
            continue
        elif pin == 'exit':
            exit_program()

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
            runs_sheet.update('D1', 'Avg Time/Km')
            runs_sheet.update('E1', 'Avg speed')
            runs_sheet.update('F1', 'Calories burned')
            break
    print("Registration succesful.")
    print("Good to have you onboard, " + username)


# LOG IN EXISTING USER
if user_type == 'login':
    while True:

        username = input("Username: ")
        if username == 'exit':
            exit_program()

        pin = input("Pin: ")
        if pin == 'exit':
            exit_program()

        cell = accounts.find(username)
        row = cell.row
        values = accounts.row_values(row)

        if values[1] == pin:
            print("Welcome back, " + username)
            break

        elif cell is None:
            print("Username not found.")
            choice = input("Try again or create a new account? (try/new): ")

            if choice == 'try':
                continue

            elif choice == 'new':
                user_type = 'new'

            elif choice == 'exit':
                exit_program()
            else:
                print("Invalid input. Enter 'try' or 'new'.")
        else:
            print("Username or pin incorrect.")
            choice = input("Try again or create a new account? (try/new): ")

            if choice == 'try':
                continue

            elif choice == 'new':
                user_type = 'new'

            elif choice == 'exit':
                exit_program()
            else:
                print("Invalid input. Enter 'try' or 'new'.")

# PROFILE SHEET
profile_sheet = SHEET.worksheet(f'{username}_profile')
profile_values = profile_sheet.get_all_values()

# RUNS SHEET
runs_sheet = SHEET.worksheet(f'{username}_runs')
runs_values = runs_sheet.get_all_values()

while True:
    # MAIN MENU
    print("MAIN MENU")
    print("1. View profile. 2. Update profile.")
    print("3. View runs. 4. Add run.")
    print("5. Logout/Exit.")
    go_to = input("Enter number: ")
    if go_to not in ['1', '2', '3', '4', '5', 'exit']:
        print("Invalid input. Enter digits only Ex: '1'")
        continue

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
        runs_sheet.update('D1', 'Avg Time/Km')
        runs_sheet.update('E1', 'Avg speed')
        runs_sheet.update('F1', 'Calories burned')

    # 1. VIEW PROFILE
    if go_to == '1':
        while True:
            # IF USERS PROFILE HAS NEVER BEEN FILLED OUT
            if len(profile_values) <= 1:
                print("Profile empty. Update your profile!")
                break

            print(profile_values[0])
            print(profile_values[-1])
            previous_row = -2

            while True:
                print("1. View previous profile update")
                print("2. Go back to main menu.")
                vp_nav = input("Enter number: ")

                if vp_nav == '1':
                    if len(profile_values) + previous_row < 1:
                        print("No more runs to view.")
                        break
                    else:
                        print(profile_values[previous_row])
                        previous_row -= 1
                elif vp_nav == '2':
                    break
                else:
                    print("Invalid input. Enter '1' or '2'")
                    continue

    # 2. UPDATE PROFILE
    if go_to == '2':
        while True:
            current_date = datetime.date.today()
            str_date = current_date.strftime('%Y-%m-%d')

            gender = input("Enter your Gender (man/woman/other): ")
            if gender.lower() not in ['man', 'woman', 'other']:
                print("Invalid input. Enter 'man', 'woman', or 'other'")
                continue

            age = input("Enter your age (Digits only): ")
            if not age.isdigit() or not 1 <= len(age) <= 3:
                print("Invalid input. Enter Ex: '28' or '51'")
                continue

            weight = input("Enter your weight in KG Ex: '84' or '73.4': ")
            if not re.match(r'^\d{1,3}(\.\d)?$', weight):
                print("Invalid input. Enter Ex: '73.4' or '65').")
                continue

            height = input("Enter your height in Cm (Digits only): ")
            if not height.isdigit() or not 2 <= len(height) <= 3:
                print("Invalid input. Enter Ex: '182'.")
                continue

            profile_data = [str_date, gender, age, weight, height]
            profile_sheet.append_row(profile_data)
            print("Your profile has been updated succesfully.")
            break

    # 3. VIEW RUNS
    if go_to == '3':
        while True:
            # IF NO RUNS ADDED
            if len(runs_values) <= 1:
                print("Runs empty. Add run first!")
                break

            print(runs_values[0])
            print(runs_values[-1])
            previous_row = -2

            while True:
                print("1. View previous profile update")
                print("2. Go back to main menu.")
                vr_nav = input("Enter number: ")

                if vr_nav == '1':
                    if len(runs_values) + previous_row < 1:
                        print("No more runs to view.")
                        break
                    else:
                        print(runs_values[previous_row])
                        previous_row -= 1
                elif vr_nav == '2':
                    break
                else:
                    print("Invalid input. Enter '1' or '2'")
                    continue

    # 4. ADD RUN
    if go_to == '4':
        while True:
            print("ADD RUN")
            profile_sheet = SHEET.worksheet(f'{username}_profile')
            get_weight = profile_sheet.cell(profile_sheet.row_count, 4).value
            weight_float = float(get_weight)

            current_date = datetime.date.today()
            str_date = current_date.strftime('%Y-%m-%d')
            print("To set date of run to current date enter (y)")
            date = input("If other date Enter (YYYY-MM-DD): ")
            if date == 'y':
                date = str_date
            elif not re.match(r'\d{4}-\d{2}-\d{2}', date):
                print("Invalid input. Enter 'YYYY-MM-DD'.")
                continue

            distance = input("Distance in Km Ex '5' or '5.3': ")
            if not re.match(r'^\d{1,2}(\.\d)?$', distance):
                print("Invalid input. Enter Ex: '12.4' or '3'.")
                continue

            distance_float = float(distance)

            tot_time = input("Total run time MM:SS (Ex '27:14' or '06:02'): ")
            if not re.match(r"^\d{2}:\d{2}$", tot_time):
                print("Invalid input. Enter Ex: '07:04' or '55:41'")

            minutes, seconds = map(int, tot_time.split(':'))

            min_to_sec = minutes * 60 + seconds

            sec_per_km = min_to_sec / distance_float

            result_min = int(sec_per_km // 60)

            result_sec = int(sec_per_km % 60)

            avg_km = f"{result_min}:{result_sec:02d}"

            avg_speed = (distance_float * 3600) / min_to_sec

            kmh = f"{avg_speed:.2f} km/h"

            calories = 0.75 * weight_float * distance_float

            runs_data = [date, distance, tot_time, avg_km, kmh, calories]
            runs_sheet.append_row(runs_data)
            print("Run added succesfully.")

    # 5. EXIT / LOG OUT
    if go_to == ['exit', '5']:
        while True:
            print("GOOD BYE!")
            exit_program()
