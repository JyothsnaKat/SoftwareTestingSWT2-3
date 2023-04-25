from getpass import getpass
import bcrypt
import re
from database import Database


db = Database()
db.createTable()


class Login:

    """
        Class for Login
        @param username
        @param password
    """

    def __init__(self):
        self.username = input("\t\tEnter Your Username: ")
        self.password = getpass(prompt="\t\tEnter Your Password: ")

    def validate(self):
        data = (self.username,)
        inputData = (self.username, self.password,)
        returnVal = db.validateData(data, inputData)
        if (returnVal == True):
            print("Logged In Successfully")
        elif(returnVal == False):
            print("Wrong Credentials")
        else:
            print("Account does not exist")


class Register:

    """
        Class for Register
        @param username
        @param password
    """

    def __init__(self):
        #name as input
        self.username = input("\t\tEnter Your Name: ")
        #password
        self.password = getpass(prompt="\t\tEnter Your Password: ")
        #begin age
        while True:
            try:
                self.age = int(input("\t\tEnter Your age: "))
                if self.age < 0:
                    raise ValueError
                break
            except ValueError:
                print("Error: Please enter a valid number.")
        #end age
        #begin interests
        interests = ['cricket', 'swimming', 'painting', 'dancing', 'reading']
        selected_interests = []
        print("Select your interests from the list below (enter the number):")
        for i, interest in enumerate(interests):
            print(f"{i+1}. {interest}")
        while True:
            interest_num = input("Enter the number of an interest (or 'done' to finish): ")
            if interest_num.lower() == 'done':
                break
            if set(selected_interests) == set(interests):
                print("You have selected all possible gender preferences.")
                break
            try:
                interest_index = int(interest_num) - 1
                if interest_index < 0 or interest_index >= len(interests):
                    raise ValueError
                selected_interest = interests[interest_index]
                if selected_interest in selected_interests:
                    print("You have already selected this interest.")
                else:
                    selected_interests.append(selected_interest)
            except ValueError:
                    print("Error: Please enter a valid interest number.")
        self.interests = ','.join(selected_interests)
        #end interests
        #begin height
        while True:
            try:
                self.height = int(input("Enter your height in centimeters: "))
                if self.height < 0:
                    raise ValueError
                break
            except ValueError:
                print("Error: Please enter a valid height.")
        #end of height
        #begin of smoking
        while True:
            self.smoking = input("Do you smoke? (yes or no): ")
            if self.smoking.lower() == "yes" or self.smoking.lower() == "no":
                break
            else:
                # Handle invalid input
                print("Error: please enter 'yes' or 'no'.")
        #end of smoking
        #begin of smoking
        while True:
            self.drinking = input("Do you drink? (yes or no): ")
            if self.drinking.lower() == "yes" or self.drinking.lower() == "no":
                break
            else:
                # Handle invalid input
                print("Error: please enter 'yes' or 'no'.")
        #end of smoking
        #begin of preferences
        preferences = ['male','female','no preference']
        selected_preferences = []
        print("Select your interests from the list below (enter the number):")
        for i, preference in enumerate(preferences):
            print(f"{i+1}. {preference}")
        while True:
            preference_num = input("Enter the number of an interest (or 'done' to finish): ")
            if preference_num.lower() == 'done':
                break
            if set(selected_preferences) == set(preferences):
                print("You have selected all possible gender preferences.")
                break
            try:
                preference_index = int(preference_num) - 1
                if preference_index < 0 or preference_index >= len(preferences):
                    raise ValueError
                selected_preference = preferences[preference_index]
                if selected_preference in selected_preferences:
                    print("You have already selected this interest.")
                else:
                    selected_preferences.append(selected_preference)
            except ValueError:
                    print("Error: Please enter a valid interest number.")
        self.preferences = ','.join(selected_preferences)
        #end preferences
        #begin of bio
        while True:
            self.bio = input("Please enter your bio (maximum 100 characters): ")
            if len(self.bio) <= 100:
                break
            else:
                print("Your bio is too long. Please try again.")
        #end of bio
        self.salt = bcrypt.gensalt()
        self.hashed = bcrypt.hashpw(self.password.encode(), self.salt)
    def add(self):
        data = (self.username,)

        result = db.searchData(data)

        if result != 0:
            data = (self.username, self.hashed, self.age, self.interests, self.height, self.smoking, self.drinking, self.preferences, self.bio )
            db.insertData(data)
            print("Account Successfully Created!!! Happy Dating!!")
        else:
            print("Username already Exists")


print("Heyo!! Welcome to dating App")
print("\t\t1. Login")
print("\t\t2. Register")
print("\t\t3. Exit")
option = input("\t\tEnter Your Option: ")
if re.search("[0-9]", option):
    if option == '1':
        login = Login()
        login.validate()
    elif option == '2':
        register = Register()
        register.add()
    elif option == '3':
        print("\t\tSee you!! comeback, Happy dating..\n\n")
    else:
        print("\t\tWrong Input..\n\n")
else:
    print("\t\tWrong Input..\n\n")
