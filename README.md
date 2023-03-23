![CI logo](https://codeinstitute.s3.amazonaws.com/fullstack/ci_logo_small.png)

Welcome mejkej,

This is the Code Institute student template for deploying your third portfolio project, the Python command-line project. The last update to this file was: **August 17, 2021**

## Reminders

* Your code must be placed in the `run.py` file
* Your dependencies must be placed in the `requirements.txt` file
* Do not edit any of the other files or your code may not deploy properly

## Creating the Heroku app

When you create the app, you will need to add two buildpacks from the _Settings_ tab. The ordering is as follows:

1. `heroku/python`
2. `heroku/nodejs`

You must then create a _Config Var_ called `PORT`. Set this to `8000`

If you have credentials, such as in the Love Sandwiches project, you must create another _Config Var_ called `CREDS` and paste the JSON into the value field.

Connect your GitHub repository and deploy as normal.

## Constraints

The deployment terminal is set to 80 columns by 24 rows. That means that each line of text needs to be 80 characters or less otherwise it will be wrapped onto a second line.

-----
Happy coding!



# Your code goes here.
# You can delete these comments, but do not change the name of this file
# Write your code to expect a terminal of 80 characters wide and 24 rows high

# Run Tracker.

## Introduction:
Run Tracker is a programe written in Python. With Run Tracker you can get a good overview of your
Running and your weight over time. By logging your runs and updating your profile.
Run tracker will also calculate your avg speed of every run in Km/h and the average time it takes you to run a Km of each run. Run Tracker will also calculate approximatly how many calories you burned during the run.
## Purpose:
Tracking your running and your weight over time. By logging your runs and updating your profile you will be able to look back and see exact stats. The computer never lies but the human memory does have a tendancy to slighly edit the past or just blankly deleting some memories.
This is only the first version of the program but i would love to one day make it in to a fitness app.

## The code:
User will first be promted if user want to login or create a new account.

If selecting new: You can register a account with a username. The requirement is 3-10 letters only.

Then you will be prompted to set a pin for your account. Pin requirement is 4-6 digits.

The program will then create two personal google sheets for the account. One for users gender, age, weight and height plus it will automatically add the current date the data was added.

Registered accounts Username & Pin will be saved on a googlesheet.
If you select login instead of create new account the code will check if any of the rows in the accounts sheet matches the Username & Pin, if it does user will be logged in.

The second sheet is for logging the users runs. User gets the choice to automatically fill in the current date or incase the run occured before they can set the date.
User will then get asked to input the distance in Km and lastly the time of the run.

The program will then calculate: 
1. Average speed in Km/h.
2. Average time per Km.
3. Amount of calories burned.

When logged in the user will see the main menu. Where there is 5 possible options.

1. View your profile. 
If this one is selected the user will get three options:
1. View last profile update.
2. View complete profile history.
3. Go back to main menu.

2. Update your profile.
User gets asked to input: Gender, Age, Weight and Height.
All of these plus the current date will be saved on their personal google sheet.

3. View your runs.
If this one is selected the user will get three options:
1. View last updated run.
2. View complete history.
3. Go back to main menu.

5. Logout/Exit.
If this one is selected the program will print GOOD BYE! and shut down the program.

## Resources:
the resources i have used to learn how to code and work with github along the project:

https://codeinstitute.net/global/

https://www.youtube.com/ 

https://www.w3schools.com/