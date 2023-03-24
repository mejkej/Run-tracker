import datetime
import gspread
import re
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
            runs_sheet.update('D1', 'Avg Time/Km')
            runs_sheet.update('E1', 'Avg speed')
            runs_sheet.update('F1', 'Calories burned')
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

while True:
    # PROFILE SHEET
    profile_sheet = SHEET.worksheet(f'{username}_profile')
    profile_values = profile_sheet.get_all_values()

    # RUNS SHEET
    runs_sheet = SHEET.worksheet(f'{username}_runs')
    runs_values = runs_sheet.get_all_values()

    # MAIN MENU
    print("MAIN MENU")
    print("1. View profile. 2. Update profile.")
    print("3. View runs. 4. Add run.")
    print("5. Logout/Exit.")
    go_to = input("Enter number: ")
    if go_to not in ['1', '2', '3', '4', '5']:
        print("Invalid input. Enter digit only Ex: '1'")
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

            print("VIEW PROFILE")
            print("1. View last profile update.")
            print("2. View complete profile history.")
            print("3. Go back to main menu.")
            go_to_one = input("Enter number: ")

            if go_to_one == '1':
                print(profile_values[0])
                print(profile_values[-1])

            elif go_to_one == '2':
                print(runs_values)

            elif go_to_one == '3':
                break

            else:
                print("Invalid input. Enter '1', '2', or '3'")
                continue

    # 2. UPDATE PROFILE
    if go_to == '2':
        while True:

            print("UPDATE PROFILE")
            current_date = datetime.date.today()
            str_date = current_date.strftime('%Y-%m-%d')

            gender = input("Enter your Gender (man/woman/other): ")
            if gender.low() in ['man', 'woman', 'other']:
                continue
            else:
                print("Invalid input. Enter 'man', 'woman', or 'other'")
                continue

            age = input("Enter your age (Digits only): ")
            if age.isdigit() and 1 <= len(age) <= 3:
            else:
                print("Invalid input. Enter Ex: '32' (Digits only): ")
                continue

            weight = input("Enter your weight in KG Ex: '84' or '73.4': ")
            if re.match(r'^\d{1,3}(\.\d)?$', weight):
            else:
                print("Invalid input. Ex: '73.4' or '65').")
                continue

            height = input("Enter your height in Cm (Digits only): ")
            if height.isdigit() and 1 <= len(height) <= 3:
            else:
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

            print("VIEW RUNS")
            print("1. View last added run.")
            print("2. View complete history.")
            print("3. Go back to main menu.")
            go_to_three = input("Enter number: ")
            values = runs_sheet.get_all_values()
            last_row = values[-1]

            if go_to_three == '1':
                print(runs_values[0])
                print(runs_values[-1])

            elif go_to_three == '2':
                print(runs_values)

            elif go_to_three == '3':
                break
            else:
                print("Invalid input. Enter '1', '2' or '3'")
                continue

    # 4. ADD RUN
    if go_to == '4':
        while True:
            print("ADD RUN")
            
            profile_data.get_all_values()
            last_row = values[-1]
            weight = (last_row[3])
            weight_float = float(weight)

            current_date = datetime.date.today()
            str_date = current_date.strftime('%Y-%m-%d')
            print("To set date of run to current date enter (y)")
            date = input("If other date Enter (YYYY-MM-DD): ")
            if date == 'y':
                date = str_date
            elif not re.match(r'\d{4}-\d{2}-\d{2}', date):
                print("Invalid input. Enter 'YYYY-MM-DD'.")
                continue

            distance = input("Distance in Km (Ex '5' or '5.3'): ")
            distance_float = distance

            time = input("Time MM:SS (Ex '27:14' or '06:02'): ")

            minutes = int(time.split(':')[0])
            seconds = int(time.split(':')[1])

            min_to_sec = minutes * 60 + seconds

            sec_per_km = min_to_sec / distance

            result_min = int(sec_per_km // 60)

            result_sec = int(sec_per_km % 60)

            avg_time_km = f"{result_min}:{result_sec:02d}"

            avg_speed = (distance * 3600) / min_to_sec

            avg_speed_kmh = f"{avg_speed:.2f} km/h"

            calories_burned = 0.75 * weight_float * distance_float

            run_data = [date, distance, time, avg_time_km, avg_speed_kmh, calories_burned]
            profile_sheet.append_row(profile_data)
            print("Run added succesfully.")

    # 5. EXIT / LOG OUT
    if go_to == '5':
        print("GOOD BYE!")

