from getpass import getpass
import bcrypt
import re
from database import Database
import sys
import random
import string
from search import Search
from prettytable import PrettyTable


db = Database()
db.createTable()
db.createUnderage()

username = None
password = None


class Login:

    """
        Class for Login
        @param username
        @param password
    """

    def __init__(self):
        self.username = input("\t\tEnter Your Username: ")
        self.password = getpass(prompt="\t\tEnter Your Password: ")
        global username 
        global password 
        username = self.username
        password = self.password

    def validate(self):
        data = (self.username,)
        inputData = (self.username, self.password,)
        returnVal = db.validateData(data, inputData)
        if returnVal == True:
            print("Logged In Successfully")
            #Did not need this because you are already validating it. We can reuse self.username
            #user_id = db.getUserId(self.username)
            while True:
                print("1. Search")
                print("2. View Matches")
                print("3. View Requests")
                print("4. View Profile")
                print("5. Log out")
                secondOption = input("Enter Your Option: ")
                if re.search("[0-9]", secondOption):
                    if secondOption == '1':
                        while True:
                            search=Search()
                            searchResults = db.search(self.username,search.min_age,search.max_age,search.interests,search.min_height,search.smoking_preference,search.drinking_preference)
                            ret_value = search.view(searchResults,self.username)
                            if ret_value == 2:
                                continue
                            elif ret_value == 3:
                                break
                    elif secondOption == '4':
                        profile = Profile()
                        profile.update()
                    elif secondOption == '2':
                        view_matches = ViewMatches(self.username)
                        view_matches.view()
                    elif secondOption == '3':
                        view_requests = ViewRequests(self.username)
                        view_requests.view()
                    elif secondOption == '5':
                        print("Bye Bye!! Come back to us!! Happy dating!! \n\n")
                        break
                    else:
                        print("Error: Wrong Input..\n\n")
                        break
                else:
                    print("Error: Wrong Input..\n\n")
                    break
        elif returnVal == False:
            print("Error: Wrong Credentials \n")
        else:
            print("Error: Account does not exist\n")


class Register:

    """
        Class for Register
        @param username
        @param password
    """

    def __init__(self):
        # first name as input
        pattern1 = r'^[a-zA-Z\']+$'
        while True:
            val = 0
            self.firstname = input("Enter Your First Name: ")
            if re.match(pattern1, self.firstname):
                val = val + 1
            else:
                print("Error: Invalid characters in First Name \n")
            if len(self.firstname) < 3:
                print("Error: First name should have more than three characters \n")
                
            else:
                val = val + 1
            if not self.firstname.strip():
                print("Error: Name can't be blank")
            else:
                val = val + 1
            if val == 3:
                break
        #last name
        
        while True:
            self.lastname = input("Enter Last Name: ")
            val = 0
            if not self.lastname.isalpha():
                print("Error: Last name should have only alphabets \n")
            else:
                val = val + 1
            if not self.lastname.strip():
                print("Error: Name should not have any whitespaces \n")
            else:
                val = val + 1
            if val == 2:
                break
        #email address
        while True:
            pattern = r'^[a-zA-Z0-9]+(\.[a-zA-Z0-9]+)*@[a-zA-Z0-9]+\.[a-zA-Z]+(\.[a-zA-Z]+)*$'
            self.email = input("Enter your email address: ")
            if re.match(pattern, self.email):
               #do nothing
               break
            else:
                print("Error: Invalid email address. Mail should start with alphanumeric and can contain alphabets, digits and period only. \n")
        data = (self.email,)
        result = db.searchEmail(data)
        if result != 0:
            f = 1
        else:
            print("Sorry! An account is already with this email address \n")
            sys.exit()
        #age
        while True:
            val = 0
            try:
                self.age = int(input("Enter Your age: "))
                if self.age < 0:
                    print("Error: Please enter a valid age. \n")
                    val = val + 1
                if self.age >= 100:
                    print("Error: Please enter age less than 100")
                if self.age > 0 and self.age < 18:
                    data = (self.email,)
                    check = db.searchEmailUnderage(data)
                    if check == 0:
                        print("Sorry! we noticed that your mail address belongs to underage individual. \n")
                    else:
                        print("Sorry!! Come back to us once you are 18. \n")
                        data = (self.firstname, self.lastname, self.email, self.age )
                        result = db.insertDataUnder(data)
                    val = val + 1
                    sys.exit()
                if self.age >= 18:
                    check = db.searchEmailUnderage(data)
                    if check  == 0:
                        print("Sorry! we noticed that your mail address belongs to underage individual. \n")
                        sys.exit()
                    else:
                        print("Congrats!!Basic Validation done. \n")
                        break
            except ValueError:
                    print("Error: Please enter a valid age. \n")
        #end age
        #begin of gender
        while True:
            self.gender = input("What is your gender? (male or female): ")
            if self.gender.lower() == "male" or self.gender.lower() == "female" :
                break
            else:
                # Handle invalid input
                print("Error: please enter 'male' or 'female'. \n")
        #end gender
        #password
        while True:
            val = 0 
            self.password = getpass(prompt="Enter Your Password: ")
            # Check if password has at least one uppercase letter
            if not re.search(r'[A-Z]', self.password):
                print("Password should at least have one uppercase letter. \n")
                val = val + 1
            # Check if password has at least one lowercase letter
            if not re.search(r'[a-z]', self.password):
                print("Password should at least have one lowercase letter. \n")
                val = val + 1
            # Check if password has at least one digit
            if not re.search(r'\d', self.password):
                print("Password should at least have one digit. \n")
                val = val + 1
            # Check if password is at least 8 characters long
            if len(self.password) < 8:
                print("Password should at least be 8 characters long. \n")
                val = val + 1
            if not re.search(r"[!@#$%^&*()\-_=+{};:,<.>]", self.password):
                print("Password should at least have one special character. \n")
                val = val + 1
            if val == 0:
                break
        #begin interests
        interests = ['cricket', 'swimming', 'painting', 'dancing', 'reading']
        selected_interests = []
        print("Select your interests from the list below (enter the number): \n")
        for i, interest in enumerate(interests):
            print(f"{i+1}. {interest}")
        while True:
            interest_num = input("Enter the number of an interest (or 'done' to finish): ")
            if not selected_interests and interest_num.lower() == 'done':
                print("Error: Enter atleast one interest. \n")
            else:
                if interest_num.lower() == 'done':
                    break
                try:
                    interest_index = int(interest_num) - 1
                    if interest_index < 0 or interest_index >= len(interests):
                        raise ValueError
                    selected_interest = interests[interest_index]
                    if selected_interest in selected_interests:
                        print("You have already selected this interest. Enter a different interest. \n")
                    else:
                        selected_interests.append(selected_interest)
                        if set(selected_interests) == set(interests):
                            print("You have selected all possible interests. \n")
                            break
                except ValueError:
                    print("Error: Please enter a valid interest number. \n")
        self.interests = ','.join(selected_interests)
        #end interests
        #begin height
        while True:
            try:
                self.height = float(input("Enter your height in centimeters: "))
                if self.height <= 0.0:
                    raise ValueError
                elif self.height > 300.0:
                    print("Maximum height allowed is 300 centimeters \n ")
                else:
                    break
            except ValueError:
                print("Error: Please enter a valid height. \n")
        #end of height
        #begin of smoking
        while True:
            self.smoking = input("Do you smoke? (yes or no): ")
            if self.smoking.lower() == "yes" or self.smoking.lower() == "no":
                break
            else:
                # Handle invalid input
                print("Error: please enter 'yes' or 'no'. \n")
        #end of smoking
        #begin of smoking
        while True:
            self.drinking = input("Do you drink? (yes or no): ")
            if self.drinking.lower() == "yes" or self.drinking.lower() == "no":
                break
            else:
                # handle invalid input
                print("Error: please enter 'yes' or 'no'. \n")
        #end of smoking
        #begin of preferences
        while True:
            self.genderpreferences = input("What is your gender preference? (male or female or na for no preference): ")
            if self.genderpreferences.lower() == "male" or self.genderpreferences.lower() == "female" or self.genderpreferences.lower() == "na":
                break
            else:
                # Handle invalid input
                print("Error: please enter 'male' or 'female' or 'no preference'. \n")
        #end preferences
        #begin of bio
        while True:
            self.bio = input("Please enter your bio (maximum 100 characters): ")
            if len(self.bio) <= 100:
                break
            else:
                print("Your bio is too long. Please try again. \n")
        #end of bio
        self.salt = bcrypt.gensalt()
        self.hashed = bcrypt.hashpw(self.password.encode(), self.salt)
    def add(self):
        first_name_letters = self.firstname[:3]
        while True:
        # Generate a random string of length 5
            random_letters = ''.join(random.choices(string.digits, k=5))
            # Concatenate the first name letters with random letters
            self.username = first_name_letters + random_letters
            dataU = (self.username,)
            resultUser = db.searchData(dataU)
            if resultUser != 0:
                #result = db.searchData(data)
                data = (self.firstname, self.lastname, self.email, self.username, self.hashed, self.age, self.gender, self.interests, self.height, self.smoking, self.drinking, self.genderpreferences, self.bio )
                result = db.insertData(data)
                if result != 0:
                    print("Account Successfully Created!!! Your username is:",self.username)
                    break
                else:
                    print("Sorry!! Try again later. \n")
                    break
                
class ViewRequests:
    """
        Class for viewing friend requests
    """
    def __init__(self, user_id):
        self.user_id = user_id

    def view(self):
        
        
        
        
            while True:
                print("1. Sent Requests")
                print("2. Received Requests")
                print("3. Go back")
                option = input("Enter your option: ")
                if option == '1':
                    sent_requests = db.getSentRequests(self.user_id)
                    if not sent_requests:
                        print("You haven't sent any requests.")
                    else:
                        print("")
                        print("Sent friend requests:")
                        print(sent_requests)
                        while True:
                            exitvariable = input("Enter 'back' to go back to the list: ")
                            if re.search(r'\bback\b', exitvariable, re.IGNORECASE):
                                break
                            else:
                                print("Invalid option")
                            break     

                                
                elif option == '2':
                    while True:
                        received_requests, requests_dict = db.getReceivedRequests(self.user_id)
                        if not received_requests:
                            print("")
                            print("You don't have any received requests.")
                            break
                            
                        else:
                            print(received_requests)

                            req_id = input("Enter the User ID to accept/reject or type 'back' to go back: ")
                            if req_id.lower() == 'back':
                                break
                            else:
                                if req_id in requests_dict:                       
                                    while True:
                                        choice = input("Do you want to accept or reject the request? (a/r): ")
                                        if choice.lower() == 'a':
                                            db.acceptRequest(req_id, self.user_id)                                            
                                            print("Friend request accepted.")
                                            while True:
                                                go_back = input("Enter 'back' to go back to the list:" )
                                                if re.search(r'\bback\b', go_back, re.IGNORECASE):
                                                    break
                                                else:
                                                    print("Invalid Option")
                                            break
                                        elif choice.lower() == 'r':
                                            db.rejectRequest(req_id, self.user_id)
                                            print("Friend request rejected.")
                                            break
                                        else:
                                            print("Invalid choice.")
                                else:
                                    print("Inavlid ID")
                elif option == '3':
                    break
                else:
                    print("Invalid option.")


class ViewMatches:
    """
        Class for viewing matches
    """
    def __init__(self, user_id):
        self.user_id = user_id

    def view(self):
        matches = db.getMatches(self.user_id)
        if not matches:
            print("You have no matches.")
            print("")
        else:
            print("Your matches:")
            table = PrettyTable()
            table.field_names = ["ID", "Name" , "Age" , "Bio"]
            usernames = []
            for m in matches:
                table.add_row([m[2], m[1], m[3], m[9]])
                usernames.append(m[2])  # Add the username to the list
            print(table.get_string(fields=["ID", "Name", "Age", "Bio"]))

            
            while True:
                print("")
                print("Please choose an option")
                print("")
                print("1. View Profile")
                print("2. Go Back")
                user_input = input("Your choice: ")
            
                if re.search("[0-9]", user_input):
                 # View profile
                    if user_input == '1':
                        while True:
                            print("")
                            user_id = input("Please enter the user ID of the profile you want to view or enter 'back' to go to the: ")
                            if re.search(r'\bback\b', user_id, re.IGNORECASE):
                                break
                            elif user_id in usernames:
                                row = db.getUserDetails(user_id)
                                if row:
                                    profile = PrettyTable()
                                    profile.field_names = ["ID", "Name", "Age", "Interests", "Height", "Smoking", "Drinking", "Bio"]
                                    profile.add_row([row[4], row[1] + " " + row[2], row[6], row[8], row[9], row[10], row[11], row[12]])
                                    print(profile)
                                    while True:
                                        go_back = input("Enter 'back' to go back to the list: ")
                                        if re.search(r'\bback\b', go_back, re.IGNORECASE):
                                            break
                                        else:
                                            print("Invalid option. Please try again.")
                                else:
                                    print("No user found with this ID.")
                            else:
                                print("Invalid user ID. Please try again.")
                            
                    elif user_input == '2':
                        break
                    else:
                        print("Error: Wrong Input..\n\n")
                        continue
                      
                


class Profile:

    """
        Class for Profile
    """

    def __init__(self):
        #self.username = input("\t\tConfirm Your Username: ")
        #self.password = getpass(prompt="\t\tConfirm Your Password: ")
        data = (username,)
        user_info = db.fetchData(data)
        print("Profile Info: \n")
        print(f"First Name: {user_info[0][1]}")
        print(f"Last Name: {user_info[0][2]}")
        print(f"Email address: {user_info[0][3]}")
        print(f"Username: {user_info[0][4]}")
        print(f"Age: {user_info[0][6]}")
        print(f"Gender: {user_info[0][7]}")
        print(f"Interests: {user_info[0][8]}")
        print(f"Height: {user_info[0][9]}")
        print(f"Smoking: {user_info[0][10]}")
        print(f"Drinking: {user_info[0][11]}")
        print(f"Preferred Gender: {user_info[0][12]}")
        print(f"Bio: {user_info[0][13]}")
    def update(self):
        val = 0
        while True:
            choice = input("Do you want to change any information? (yes/no): ")
            if choice.lower() == "yes":
                self.username = input("Confirm Your Username: ")
                self.password = getpass(prompt="Confirm Your Password: ")
                data = (self.username,)
                inputData = (self.username, self.password,)
                returnVal = db.validateData(data, inputData)
                if returnVal == True and username == self.username:
                    val = 1
                    user_id = self.username
                    user_info = db.fetchData(data)
                    print("Which info do you prefer to change? \n")
                    print("1. Age")
                    print("2. Gender")
                    print("3. Interests")
                    print("4. Height")
                    print("5. Smoking")
                    print("6. Drinking")
                    print("7. Preferred Gender")
                    print("8. Bio")
                    print("9. Exit")
                    field = input("Enter your choice to change? ")
                    if re.search("[0-9]", field):
                        if field == '1':
                            val = val + 1
                            while True:
                                flag = 0
                                try:
                                    age = int(input("Enter new age: "))
                                    
                                    if age < (0):
                                        print("Error: Please enter a valid age. \n")
                                        flag = flag + 1
                                    elif age < int(user_info[0][6]):
                                        print("Age can't be decreased. \n")
                                        flag = flag + 1
                                    elif age == int(user_info[0][6]):
                                        print("No changes made. \n")
                                        break
                                        #wait
                                        val = 0
                                    if flag == 0:
                                        db.update_user_info(user_id, "age", age)
                                        print("Age updated successfully! \n")
                                        break
                                except ValueError:
                                    print("Error: Please enter a valid age. \n")
                        elif field == '2':
                            val = val + 1
                            while True:
                                gender = input("What is your gender? (male or female): ")
                                if gender.lower() == "male" or gender.lower() == "female" :
                                    if gender == user_info[0][7]:
                                        print("No changes made. \n")
                                        break
                                    else:
                                        db.update_user_info(user_id, "gender", gender)
                                        print("Gender updated successfully! \n")
                                        break
                                else:
                                    # Handle invalid input
                                    print("Error: please enter 'male' or 'female'. \n")
                                
                        elif field == '3':
                            val = val + 1
                            existing_interests = user_info[0][8]
                            complete_interests = ["cricket", "swimming", "painting", "dancing", "reading"]  # Complete list of interests
                            existing_interests_list = existing_interests.split(',')
                            add_interests = [interest for interest in complete_interests if interest not in existing_interests_list]
                            remove_interests = [interest for interest in existing_interests_list]
                            print("1. Add")
                            print("2. Remove")
                            choice_in = input("Do you want to add or remove?")
                            if choice_in == '1':                        
                                if add_interests == []:
                                    print("No new Interests to add")
                                    
                                else:
                                    print("Available Interests for Adding: \n")
                                    selected_interests = []
                                    for i, interest in enumerate(add_interests, 1):
                                            print(f"{i}. {interest}") 
                                    while True:
                                        interest_num = input("Enter the number of an interest (or 'done' to finish): ")
                                        if not selected_interests and interest_num.lower() == 'done':
                                            print("Error: Enter atleast one interest. \n")
                                        else:
                                            if interest_num.lower() == 'done': 
                                                break   
                                            try:
                                                interest_index = int(interest_num) - 1
                                                if interest_index < 0 or interest_index >= len(add_interests):
                                                    raise ValueError
                                                selected_interest = add_interests[interest_index]
                                                if selected_interest in selected_interests:
                                                    print("You have already selected this interest. \n")
                                                else:
                                                    selected_interests.append(selected_interest)
                                                    existing_interests_list.append(selected_interest)
                                                    print("Interests updated successfully! \n")
                                                    if set(selected_interests) == set(add_interests):
                                                        print("You have selected all possible interests. \n")
                                                        print("Interests updated successfully! \n")
                                                        break      
                                            except ValueError:
                                                print("Error: Please enter a valid interest number. \n")
                                    updated_interests = ','.join(existing_interests_list)
                                    db.update_user_info(user_id, "interests", updated_interests)
                                            
                            elif choice_in == '2':
                                val = val + 1
                                if remove_interests == []:
                                    print("No new Interests to remove")
                                else:
                                    print("\nCurrent Interests for Removing:")
                                    selected_interests = []
                                    for i, interest in enumerate(remove_interests, 1):
                                        print(f"{i}. {interest}")
                                    while True:
                                        interest_num = input("Enter the number of an interest (or 'done' to finish): ")
                                        if not selected_interests and interest_num.lower() == 'done':
                                            print("Error: Enter atleast one interest. \n")
                                        else:
                                            if interest_num.lower() == 'done':
                                                break
                                            try:
                                                interest_index = int(interest_num) - 1
                                                if interest_index < 0 or interest_index >= len(remove_interests):
                                                    raise ValueError
                                                selected_interest = remove_interests[interest_index]
                                                if selected_interest in selected_interests:
                                                    print("You have already selected this interest. \n")
                                                else:
                                                    selected_interests.append(selected_interest)
                                                    existing_interests_list.remove(selected_interest)
                                                    print("Interests removed successfully! \n")
                                                    if set(selected_interests) == set(remove_interests):
                                                        print("You have selected all possible interests. \n")
                                                        print("Interests removed successfully! \n")
                                                        break
                                            except ValueError:
                                                print("Error: Please enter a valid interest number. \n")
                                    updated_interests = ','.join(existing_interests_list)
                                    db.update_user_info(user_id, "interests", updated_interests)
                                            
                            else:
                                print("Invalid choice")
                            #interests = input("Enter your interests (comma-separated): ")
                            #interests_set = set(interests.split(","))
                        elif field == '4':
                            val = val + 1
                            while True:
                                try:
                                    height = float(input("Enter new height: \n"))
                                    if height <= 0.0:
                                        raise ValueError
                                    if self.height > 300.0:
                                        print("Maximum height allowed is 300 centimeters \n ")
                                    if int(height) ==  user_info[0][9]:
                                        print("No changes made. \n")
                                        break
                                    else:
                                        db.update_user_info(user_id, "height", height)
                                        print("Height updated successfully! \n")
                                        break
                                except ValueError:
                                    print("Error: Please enter a valid height. \n")
                        elif field == '5':
                            val = val + 1
                            while True:
                                smoking = input("Do you smoke? (yes or no): ")
                                if smoking.lower() == "yes" or smoking.lower() == "no":
                                    if smoking.lower() == user_info[0][10]:
                                        print("No changes made. \n")
                                    else:
                                        db.update_user_info(user_id, "smoking", smoking)
                                        print("Smoking status updated successfully! \n")
                                    break
                                else:
                                # Handle invalid input
                                    print("Error: please enter 'yes' or 'no'. \n")
                        elif field == '6':
                            val = val + 1
                            while True:
                                drinking = input("Do you drink? (yes or no): ")
                                if drinking.lower() == "yes" or drinking.lower() == "no":
                                    if drinking.lower() == user_info[0][11]:
                                        print("No changes made. \n")
                                    else:
                                        db.update_user_info(user_id, "drinking", drinking)
                                        print("Drinking status updated successfully! \n")
                                    break
                                else:
                                # Handle invalid input
                                    print("Error: please enter 'yes' or 'no'. \n")
                        elif field == '7':
                            val = val + 1
                            while True:
                                genderpreferences = input("Enter your new gender preference? (male or female or no preference): ")
                                if genderpreferences.lower() == "male" or genderpreferences.lower() == "female" or genderpreferences.lower() == "no preference":
                                    if genderpreferences == user_info[0][12]:
                                        print("No changes made. \n")
                                        break
                                    else:
                                        db.update_user_info(user_id, "genderpreferences", genderpreferences)
                                        print("Gender preference updated successfully! \n")
                                        break
                                else:
                                    # Handle invalid input
                                    print("Error: please enter 'male' or 'female' or 'no preference'. \n")
                       
                        elif field == '8':
                            val = val + 1
                            while True:
                                bio = input("Enter new bio (max 100 characters): ")
                                if bio == user_info[0][13]:
                                    print("No changes made. \n")
                                    break
                                if len(bio) <= 100:
                                    db.update_user_info(user_id, "bio", bio)
                                    print("Bio updated successfully! \n")
                                    break
                                else:
                                    print("Bio should be 100 characters or less. \n")
                        elif field == '9':
                            Profile()
                            break
                        else:
                            print("Error: Invalid choice. \n")
                    else:
                        print("Error: Invalid choice. \n")
                elif returnVal == False:
                    print("Error: Wrong Credentials. \n")
                else:
                    print("Error: Wrong username provided. \n")
            elif choice.lower() == "no":
                if val == 0:
                    print("No changes made. \n")
                    break
                else:
                    print("Updated!!! \n")
                    Profile()
                    break
            else:
                print("Error: Invalid choice. \n")

while True:
    print("Heyo!! Welcome to dating App")
    print("1. Login")
    print("2. Register")
    print("3. Exit")
    option = input("Enter Your Option: ")
    if re.search("[0-9]", option):
        if option == '1':
            login = Login()
            login.validate()
        elif option == '2':
            register = Register()
            register.add()
        elif option == '3':
            print("See you!! comeback, Happy dating..\n\n")
            break
        else:
            print("Wrong Input..\n\n")
    else:
        print("Wrong Input..\n\n")
