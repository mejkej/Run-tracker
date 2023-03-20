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

# Welcome
print("Hello & Welcome to Run Tracker!")

# Log in or Register
while True:
    user_type = input("Login or create new account (login/new): ")
    if user_type in ['new', 'login']:
        break
    else:
        print("Invalid input. Please enter 'new' or 'login'.")

# Create new account
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
            SHEET.add_worksheet(title=f'{username}_profile', rows=100, cols=6)
            profile = SHEET.worksheet(f'{username}_profile')
            profile.update('A1', 'Date')
            profile.update('B1', 'Gender')
            profile.update('C1', 'Age')
            profile.update('D1', 'Weight')
            profile.update('E1', 'Height')
            profile.update('F1', 'Goal')
            SHEET.add_worksheet(title=f'{username}_runs', rows=100, cols=6)
            runs = SHEET.worksheet(f'{username}_runs')
            runs.update('A1', 'Date')
            runs.update('B1', 'Distance')
            runs.update('C1', 'Time')
            runs.update('D1', 'Avg speed')
            runs.update('E1', 'Calories burnt')
            runs.update('F1', 'Note')
            break
        else:
            print("Pin format incorrect. Please enter 4-6 digits only.")

    print("Registration succesful.")
    print("Good to have you onboard, " + username)

# Login existing user
if user_type == 'login':
    while True:
        username = input("Username: ")
        pin = input("Pin: ")
        cell = accounts.find(username)
        row = cell.row
        values = accounts.row_values(row)
        if values[1] == pin:
            print("Welcome back, " + username)
            break
        else:
            print("Username or pin incorrect.")
            choice = input("Try again or create a new account? (try/new): ")
            if choice == 'new':
                user_type = 'new'
                break
            else:
                continue

# User profile

