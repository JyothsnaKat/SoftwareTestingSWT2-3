from getpass import getpass
import bcrypt
import re
from database import Database
from colorama import init, Fore, Style
import sys
import random
import string
from search import Search
from prettytable import PrettyTable
import time


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
        self.username = input("Enter Your User ID: ")
        self.password = getpass(prompt="Enter Your Password: ")
        global username 
        global password 
        username = self.username
        password = self.password

    def validate(self):
        data = (self.username,)
        inputData = (self.username, self.password,)
        returnVal = db.validateData(data, inputData)
        if returnVal == True:
            print(Fore.GREEN + "Logged In Successfully" + Style.RESET_ALL)
            #Did not need this because you are already validating it. We can reuse self.username
            #user_id = db.getUserId(self.username)
            while True:
                print("1. Search")
                print("2. View Matches")
                print("3. View Requests")
                print("4. My Profile")
                print("5. Logout")
                secondOption = input("Enter Your choice: ")
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
                        print(Fore.LIGHTMAGENTA_EX + "Bye Bye!! Come back to us!! Happy dating!!\n" + Style.RESET_ALL)
                        
                        break
                    else:
                        print(Fore.RED + "\nError: " + Fore.RESET + "Please enter a valid choice.\n")
                        
                        break
                else:
                    print(Fore.RED + "\nError: " + Fore.RESET + "Please enter a valid choice.\n")
                    
                    break
        elif returnVal == False:
            print(Fore.RED + "\nError: " + Fore.RESET + "Wrong Credentials.\n")
            
        else:
            print(Fore.RED + "\nError: "+ Fore.RESET + "Account does not exist.\n")
            


class Register:

    """
        Class for Register
        @param username
        @param password
    """

    def __init__(self):
        # first name as input
        pattern1 = r"^(?!')(?!.*''.*$)[a-zA-Z']+"
        pattern2 = r"''"
        while True:
            val = 0
            self.firstname = input("Enter Your First Name: ")
           
            if re.match(pattern1, self.firstname):
                val = val + 1
            else:
                if self.firstname.startswith("'"):
                    print(Fore.RED + "\nError: " + Fore.RESET + "First name can't start with ' \n") 
                elif re.search(pattern2, self.firstname):
                    print(Fore.RED + "\nError: " + Fore.RESET + "Consecutive ' found in first name. Please enter valid name.\n")
                else:
                    print(Fore.RED + "\nError: " + Fore.RESET + "Invalid characters in first name.\n")
            if len(self.firstname) < 3:
                print(Fore.RED + "\nError: " + Fore.RESET + " First name should have atleast three characters.\n") 
            else:
                val = val + 1
            if not self.firstname.strip():
                print(Fore.RED + "\nError: " + Fore.RESET + " Name can't be blank.\n")
                
            else:
                val = val + 1
            if val == 3:
                break
        #last name
        
        while True:
            self.lastname = input("Enter Last Name: ")
            val = 0
            if not self.lastname.isalpha():
                print(Fore.RED + "\nError: " + Fore.RESET + " Last name should have only alphabets.\n")
            else:
                val = val + 1
            if not self.lastname.strip():
                print(Fore.RED + "\nError: " + Fore.RESET + " Name should not have any whitespaces.\n")
            else:
                val = val + 1
            if val == 2:
                break
        #email address
        while True:
            pattern = r"^(?![\d.])(?:[a-zA-Z0-9]+[.]?)+@[a-zA-Z0-9]+\.[a-zA-Z0-9]+$"
            pattern1 = r'^.+@.+\..+$'
            self.email = input("Enter your email address: ")
            if re.match(pattern, self.email):
               #do nothing
               break
            else:
                if re.search(pattern1,self.email):
                    print(Fore.RED + "\nError: " + Fore.RESET + "Invalid email address. Mail should start with alphabets only and can contain alphabets, digits and period.\n")
                    
                else:
                    print(Fore.RED + "\nError: " + Fore.RESET + "Please enter valid email address.\n")
                    
        data = (self.email,)
        result = db.searchEmail(data)
        if result != 0:
            f = 1
        else:
            print(Fore.RED + "Sorry! An account already exists with this email address.\n" + Style.RESET_ALL)
            time.sleep(3)
            sys.exit()
        #age
        while True:
            val = 0
            flag = 2
            try:
                self.age = int(input("Enter Your age: "))
                if self.age <= 0:
                    print(Fore.RED + "\nError: " + Fore.RESET + "Please enter a valid age.\n")
                    
                    val = val + 1
                if self.age >= 100:
                    print(Fore.RED + "\nError: " + Fore.RESET + "Please enter age less than 100.\n")
                    
                    flag = 0
                if self.age > 0 and self.age < 18:
                    data = (self.email,)
                    check = db.searchEmailUnderage(data)
                    if check == 0:
                        print(Fore.RED + "Sorry! we noticed that your mail address belongs to underage individual.\n" + Style.RESET_ALL)
                        
                    else:
                        print(Fore.LIGHTMAGENTA_EX + "Sorry!! Come back to us once you are 18.\n" + Style.RESET_ALL)
                        
                        data = (self.firstname, self.lastname, self.email, self.age )
                        result = db.insertDataUnder(data)
                    val = val + 1
                    time.sleep(3)
                    sys.exit()
                if self.age >= 18 and flag != 0:
                    check = db.searchEmailUnderage(data)
                    if check  == 0:
                        print(Fore.RED + "Sorry! we noticed that your mail address belongs to underage individual.\n" + Style.RESET_ALL)
                        time.sleep(3)
                        sys.exit()
                    else:
                        print(Fore.GREEN + "Congrats!!Basic Validation done.\n" + Style.RESET_ALL)
                        
                        break
            except ValueError:
                    print(Fore.RED + "\nError: " + Fore.RESET + "Please enter a valid age.\n")
                    
        #end age
        #begin of gender
        while True:
            self.gender = input("Enter your gender ('male' or 'female'): ")
            if self.gender.lower() == "male" or self.gender.lower() == "female" :
                break
            else:
                # Handle invalid input
                print(Fore.RED + "\nError: " + Fore.RESET + "Please enter 'male' or 'female'.\n")
        #end gender
        #password
        while True:
            val = 0 
            self.password = getpass(prompt="Enter Your Password: ")
            # Check if password has at least one uppercase letter
            if not re.search(r'[A-Z]', self.password):
                print(Fore.RED + "Error: " + Fore.RESET + "Password should at least have one uppercase letter.")
                val = val + 1
            # Check if password has at least one lowercase letter
            if not re.search(r'[a-z]', self.password):
                print(Fore.RED + "Error: " + Fore.RESET + "Password should at least have one lowercase letter.")
                val = val + 1
            # Check if password has at least one digit
            if not re.search(r'\d', self.password):
                print(Fore.RED + "Error: " + Fore.RESET + "Password should at least have one digit.")
                val = val + 1
            # Check if password is at least 8 characters long
            if len(self.password) < 8:
                print(Fore.RED + "Error: " + Fore.RESET + "Password should at least be 8 characters long.")
                val = val + 1
            if not re.search(r"[!@#$%^&*()\-_=+{};:,<.>]", self.password):
                print(Fore.RED + "Error: " + Fore.RESET + "Password should at least have one special character.")
                val = val + 1
            if val == 0:
                break
        #begin interests
        interests = ['travelling', 'swimming', 'painting', 'dancing', 'reading']
        selected_interests = []
        print("Select your interests from the list below (enter the number): ")
        for i, interest in enumerate(interests):
            print(f"{i+1}. {interest}")
        while True:
            interest_num = input("Enter the number of an interest (or 'done' to finish): ")
            if not selected_interests and interest_num.lower() == 'done':
                print(Fore.RED + "\nError: " + Fore.RESET + "Enter atleast one interest.\n")
                
            else:
                if interest_num.lower() == 'done':
                    break
                try:
                    interest_index = int(interest_num) - 1
                    if interest_index < 0 or interest_index >= len(interests):
                        raise ValueError
                    selected_interest = interests[interest_index]
                    if selected_interest in selected_interests:
                        print(Fore.RED + "\nError: " + Fore.RESET + "You have already selected this interest. Enter a different interest.\n")
                        
                    else:
                        selected_interests.append(selected_interest)
                        if set(selected_interests) == set(interests):
                            print("You have selected all possible interests.")
                            break
                except ValueError:
                    print(Fore.RED + "\nError: " + Fore.RESET + "Please enter a valid interest number.\n")
                    
        self.interests = ','.join(selected_interests)
        #end interests
        #begin height
        while True:
            try:
                self.height = float(input("Enter your height in centimeters: "))
                if self.height <= 0.0:
                    raise ValueError
                elif self.height > 300.0:
                    print(Fore.RED + "\nError: " + Fore.RESET + "Maximum height allowed is 300 centimeters.\n")
                    
                elif self.height < 55.0:
                    print(Fore.RED + "\nError: " + Fore.RESET + "Minimum height allowed is 55 centimeters.\n")
                    
                else:
                    break
            except ValueError:
                print(Fore.RED + "\nError: " + Fore.RESET + "Please enter a valid height.\n")
                
        #end of height
        #begin of smoking
        while True:
            self.smoking = input("Do you smoke? ('yes' or 'no'): ")
            if self.smoking.lower() == "yes" or self.smoking.lower() == "no":
                break
            else:
                # Handle invalid input
                print(Fore.RED + "\nError: " + Fore.RESET + " please enter 'yes' or 'no'.\n")
        #end of smoking
        #begin of smoking
        while True:
            self.drinking = input("Do you drink? ('yes' or 'no'): ")
            if self.drinking.lower() == "yes" or self.drinking.lower() == "no":
                break
            else:
                # handle invalid input
                print(Fore.RED + "\nError: " + Fore.RESET + "Please enter 'yes' or 'no'.\n")
        #end of smoking
        #begin of preferences
        while True:
            self.genderpreferences = input("What is your gender preference? ('male' or 'female' or 'na' for no preference): ")
            if self.genderpreferences.lower() == "male" or self.genderpreferences.lower() == "female" or self.genderpreferences.lower() == "na":
                break
            else:
                # Handle invalid input
                print(Fore.RED + "\nError: " + Fore.RESET + "Please enter 'male' or 'female' or 'na' for no preference.\n")
                
        #end preferences
        #begin of bio
        while True:
            self.bio = input("Please enter your bio (maximum 100 characters): ")
            if len(self.bio) <= 100:
                break
            else:
                print(Fore.RED + "\nError: " + Fore.RESET + "Your bio is too long. Please try again.\n")
                
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
                    print("\nAccount Successfully Created!!! Your User ID is:",  Fore.GREEN + self.username + Style.RESET_ALL)
                    
                    break
                else:
                    print(Fore.RED + "\nError:" + Fore.RESET + "Sorry!! Try again later.\n")
                    
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
                print("3. Main Menu")
                print("4. Logout")
                option = input("Enter your choice: ")
                if option == '1':
                    sent_requests = db.getSentRequests(self.user_id)
                    if not sent_requests:
                        print("You haven't sent any requests. \n")
                    else:
                        print("")
                        print("Sent requests:")
                        print(sent_requests)
                        while True:
                            exitvariable = input("Enter 'back' to go back to the list: ")
                            if re.search(r'\bback\b', exitvariable, re.IGNORECASE):
                                break
                            else:
                                print(Fore.RED + "\nError: " + Fore.RESET + "Enter a valid option.\n")
                                
                                continue     
                elif option == '2':
                    while True:
                        received_requests, requests_dict = db.getReceivedRequests(self.user_id)
                        if not received_requests:
                            
                            print("You don't have any pending received requests. \n")
                            
                            break
                            
                        else:                           

                            while received_requests:
                                print(received_requests)
                                
                                print("1. View Profile")
                                print("2. Go Back")

                                user_input = input("Enter your choice: ")
                                if user_input == '1':
                                    req_id = input("Enter User ID from the list to view or type 'back' to go back: ")
                                    if req_id.lower() == 'back':
                                        break
                                    else:
                                        if req_id in requests_dict:                                 
                                            user_details = requests_dict[req_id]
                                            user_table = PrettyTable()
                                            user_table.field_names = ["ID", "Name", "Age", "Interests", "Height", "Preferences", "Bio"]
                                            user_table.add_row([user_details[0], user_details[1], user_details[6], user_details[2], f"{user_details[3]}cm", user_details[4], user_details[5][:25]])
                                            print(user_table)
                                          
                                            while True:
                                                choice = input("Do you want to accept(a) or reject(r) the request? ('a'/'r'): ")
                                                if choice.lower() == 'a':
                                                    db.acceptRequest(req_id, self.user_id)                                            
                                                    print(Fore.GREEN + "Request accepted.\n" + Style.RESET_ALL)
                                                    
                                                    print(Fore.LIGHTMAGENTA_EX + "Its a match!!!" + Style.RESET_ALL)
                                                    
                                                    del requests_dict[req_id]
                                                    while True:
                                                        go_back = input("Enter 'back' to go back to the list: " )
                                                        if re.search(r'\bback\b', go_back, re.IGNORECASE):
                                                            break
                                                        else:
                                                            print(Fore.RED + "\nError: " + Fore.RESET + "Please enter a valid option.\n")
                                                            
                                                    break
                                                elif choice.lower() == 'r':
                                                    db.rejectRequest(req_id, self.user_id)
                                                    print("Request rejected.\n")
                                                    
                                                    del requests_dict[req_id]
                                                    break
                                                else:
                                                    print(Fore.RED + "\nError: " + Fore.RESET + "Please enter a valid choice.\n")
                                                    
                                            break
                                        else:
                                            print(Fore.RED + "\nError: " + Fore.RESET + "Please enter a valid User ID from the list.\n")
                                            

                                elif user_input == '2':
                                    break
                elif option == '3':
                    break
                elif option == '4':
                    time.sleep(3)
                    sys.exit()
                else:
                    print(Fore.RED + "\nError: " + Fore.RESET + "Please enter a valid option.\n")
                    


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
            table.field_names = ["User ID", "Name" , "Age" , "Bio"]
            usernames = []
            for m in matches:
                table.add_row([m[2], m[1], m[3], m[9]])
                usernames.append(m[2])  # Add the username to the list
            
            
            
            
            
            while True:
                
                print(table.get_string(fields=["User ID", "Name", "Age", "Bio"]))
                print("")
                print("Please choose an option: ")
                print("1. View Profile")
                print("2. Go Back")
                user_input = input("Your choice: ")
            
                
                if re.search("[0-9]", user_input):
                 # View profile
                    if user_input == '1':
                        while True:
                            check_flag=0
                            if check_flag==1:
                                break
                            print("")
                            user_id = input("Please enter the User ID from the list you want to view or enter 'back' to go to the list: ")
                            if re.search(r'\bback\b', user_id, re.IGNORECASE):
                                break                                
                            elif user_id in usernames:
                                row = db.getUserDetails(user_id)
                                if row:
                                    profile = PrettyTable()
                                    profile.field_names = ["User ID", "Name", "Age", "Interests", "Height", "Smoking", "Drinking", "Bio"]
                                    profile.add_row([row[4], row[1] + " " + row[2], row[6], row[8], row[9], row[10], row[11], row[13]])
                                    print(profile)
                                    while True:
                                        go_back = input("Enter 'back' to view another Profile: ")
                                        if re.search(r'\bback\b', go_back, re.IGNORECASE):
                                            check_flag = 1
                                            break
                                        else:
                                            print(Fore.RED + "Error:" + Fore.RESET + "Please enter a valid option.")
                                else:
                                    print("No user found with this User ID.")
                            else:
                                print(Fore.RED + "Error:" + Fore.RESET + "Please enter a valid User ID from the list.")
                            
                    elif user_input == '2':
                        break
                    else:
                        print(Fore.RED + "Error:" + Fore.RESET + " Wrong Input.")
                        continue

                      
                      
                

    """
        Class for viewing matches
    """
    def __init__(self, user_id):
        self.user_id = user_id

    def view(self):
        matches = db.getMatches(self.user_id)
        if not matches:
            print("You have no matches. \n")
            
        else:
            print("Your matches:\n")
            table = PrettyTable()
            table.field_names = ["User ID", "Name" , "Age" , "Bio"]
            usernames = []
            for m in matches:
                table.add_row([m[2], m[1], m[3], m[9]])
                usernames.append(m[2])  # Add the username to the list
            print(table.get_string(fields=["User ID", "Name", "Age", "Bio"]))
            flag = 0
            
            while True:
                if flag == 1:
                    break
                print("Please choose an option: \n")
                print("1. View Profile")
                print("2. Main Menu")
                print("3. Logout")
                user_input = input("Enter your choice: ")
                if re.search("[0-9]", user_input):
                 # View profile
                    if user_input == '1':
                        while True:
                            print("")
                            user_id = input("Please enter the User ID from the list or enter 'back' to go back: ")
                            if re.search(r'\bback\b', user_id, re.IGNORECASE):
                                flag = 1
                                break
                            elif user_id in usernames:
                                row = db.getUserDetails(user_id)
                                if row:
                                    profile = PrettyTable()
                                    profile.field_names = ["User ID", "Name", "Age", "Interests", "Height", "Smoking", "Drinking", "Bio"]
                                    profile.add_row([row[4], row[1] + " " + row[2], row[6], row[8], row[9], row[10], row[11], row[13]])
                                    print(profile)
                                    while True:
                                        go_back = input("Enter 'back' to go back to the list: ")
                                        if re.search(r'\bback\b', go_back, re.IGNORECASE):
                                            print(table.get_string(fields=["User ID", "Name", "Age", "Bio"]))
                                            break
                                        else:
                                            print(Fore.RED + "\nError: " + Fore.RESET + "Please enter a valid option.\n")
                                            
                                else:
                                    print(Fore.RED + "\nError: " + Fore.RESET + "Please enter a User ID from the list.\n")
                                    
                            else:
                                print(Fore.RED + "\nError: " + Fore.RESET + "Please enter a valid User ID from the list.\n")
                                
                            
                    elif user_input == '2':
                        break
                    elif user_input == '3':
                        time.sleep(3)
                        sys.exit()
                    else:
                        print(Fore.RED + "\nError: " + Fore.RESET + " Please enter a valid option.\n")
                        
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
        print(f"User ID: {user_info[0][4]}")
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
            choice = input("Do you want to change any information? ('yes' or 'no'): ")
            if choice.lower() == "yes":
                self.username = input("Confirm Your User ID: ")
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
                    print("9. Main Menu")
                    print("10. Logout")
                    field = input("Enter your choice to change: ")
                    if re.search("[0-9]", field):
                        if field == '1':
                            while True:
                                flag = 0
                                try:
                                    age = int(input("Enter new age: "))
                                    
                                    if age <= (0):
                                        print(Fore.RED + "\nError:" + Fore.RESET + "Please enter a valid age.\n")
                                        
                                        flag = flag + 1
                                    elif age >= (100):
                                        print(Fore.RED + "\nError: " + Fore.RESET + "Please enter age less than 100.\n")
                                        
                                        flag = flag + 1
                                    elif age < int(user_info[0][6]):
                                        print(Fore.RED + "\nError: " + Fore.RESET + "Age can't be decreased.\n")
                                        
                                        flag = flag + 1
                                    elif age == int(user_info[0][6]):
                                        print("No changes made. \n")
                                        break
                                        #wait
                                        val = 0
                                    if flag == 0:
                                        db.update_user_info(user_id, "age", age)
                                        val = val + 1
                                        print(Fore.GREEN + "Age updated successfully! \n" +Style.RESET_ALL)
                                        
                                        break
                                except ValueError:
                                    print(Fore.RED + "Error: " + Fore.RESET + "Please enter a valid age.")
                                    
                        elif field == '2':
                            while True:
                                gender = input("What is your gender? ('male' or 'female'): ")
                                if gender.lower() == "male" or gender.lower() == "female" :
                                    if gender == user_info[0][7]:
                                        print("No changes made. \n")
                                        break
                                    else:
                                        db.update_user_info(user_id, "gender", gender)
                                        val = val + 1
                                        print(Fore.GREEN + "Gender updated successfully! \n" +Style.RESET_ALL)
                                        break
                                else:
                                    # Handle invalid input
                                    print(Fore.RED + "\nError: " + Fore.RESET + "Please enter 'male' or 'female'. \n")
                                
                        elif field == '3':
                            existing_interests = user_info[0][8]
                            complete_interests = ["travelling", "swimming", "painting", "dancing", "reading"]  # Complete list of interests
                            existing_interests_list = existing_interests.split(',')
                            add_interests = [interest for interest in complete_interests if interest not in existing_interests_list]
                            remove_interests = [interest for interest in existing_interests_list]
                            while True:
                                print("1. Add")
                                print("2. Remove")
                                choice_in = input("Enter your choice:")
                                if choice_in == '1':                        
                                    if add_interests == []:
                                        print("No new Interests to add.\n")
                                        
                                    
                                    else:
                                        print("Available Interests for Adding: \n")
                                        selected_interests = []
                                        for i, interest in enumerate(add_interests, 1):
                                                print(f"{i}. {interest}") 
                                        while True:
                                            interest_num = input("Enter the number of an interest (or 'done' to finish): ")
                                            if not selected_interests and interest_num.lower() == 'done':
                                                print(Fore.RED + "\nError: " + Fore.RESET + "Enter atleast one interest. \n")
                                                
                                            else:
                                                if interest_num.lower() == 'done': 
                                                    break   
                                                try:
                                                    interest_index = int(interest_num) - 1
                                                    if interest_index < 0 or interest_index >= len(add_interests):
                                                        raise ValueError
                                                    selected_interest = add_interests[interest_index]
                                                    if selected_interest in selected_interests:
                                                        print(Fore.RED + "\nError: " + Fore.RESET + "You have already selected this interest.\n")
                                                        
                                                    else:
                                                        selected_interests.append(selected_interest)
                                                        existing_interests_list.append(selected_interest)
                                                        val = val + 1
                                                        print(Fore.GREEN + "Interests updated successfully!\n" +Style.RESET_ALL)
                                                        
                                                        if set(selected_interests) == set(add_interests):
                                                            val = val + 1
                                                            print(Fore.RED + "\nError: " + Fore.RESET + "You have selected all possible interests. \n")
                                                            print(Fore.Green + "Interests updated successfully!\n" +Style.RESET_ALL)
                                                            
                                                            break      
                                                except ValueError:
                                                    print(Fore.RED + "\nError: " + Fore.RESET + "Please enter a valid interest number.\n")
                                                    
                                        updated_interests = ','.join(existing_interests_list)
                                        db.update_user_info(user_id, "interests", updated_interests)
                                        break         
                                elif choice_in == '2':
                                    if remove_interests == []:
                                        print("No new Interests to remove\n")
                                        
                                    else:
                                        print("\nCurrent Interests for Removing:")
                                        selected_interests = []
                                        for i, interest in enumerate(remove_interests, 1):
                                            print(f"{i}. {interest}")
                                        while True:
                                            interest_num = input("Enter the number of an interest (or 'done' to finish): ")
                                            if not selected_interests and interest_num.lower() == 'done':
                                                print(Fore.RED + "\nError: " + Fore.RESET + "Please enter atleast one interest.\n")
                                            else:
                                                if interest_num.lower() == 'done':
                                                    break
                                                try:
                                                    interest_index = int(interest_num) - 1
                                                    if interest_index < 0 or interest_index >= len(remove_interests):
                                                        raise ValueError
                                                    selected_interest = remove_interests[interest_index]
                                                    if selected_interest in selected_interests:
                                                        print(Fore.RED + "\nError: " + Fore.RESET + "You have already selected this interest.\n")
                                                        
                                                    else:
                                                        selected_interests.append(selected_interest)
                                                        existing_interests_list.remove(selected_interest)
                                                        val = val + 1
                                                        print(Fore.GREEN + "Interests removed successfully!\n" +Style.RESET_ALL)
                                                        
                                                        if set(selected_interests) == set(remove_interests):
                                                            val = val + 1
                                                            print(Fore.RED + "\nError: " + Fore.RESET + "You have selected all possible interests.\n")
                                                            print(Fore.Green + "Interests removed successfully!\n" +Style.RESET_ALL)
                                                            
                                                            break
                                                except ValueError:
                                                    print(Fore.RED + "\nError: " + Fore.RESET + "Please enter a valid interest number.\n")
                                                    
                                        updated_interests = ','.join(existing_interests_list)
                                        db.update_user_info(user_id, "interests", updated_interests)
                                        break              
                                else:
                                    print(Fore.RED + "\nError: " + Fore.RESET + "Please enter a valid choice.\n")
                                    
                            #interests = input("Enter your interests (comma-separated): ")
                            #interests_set = set(interests.split(","))
                        elif field == '4':
                            while True:
                                try:
                                    height = float(input("Enter new height:"))
                                    if height <= 0.0:
                                        raise ValueError
                                    if height > 300.0:
                                        print(Fore.RED + "\nError: " + Fore.RESET + "Maximum height allowed is 300 centimeters. \n")
                                        
                                    if height < 55.0:
                                        print(Fore.RED + "\nError: " + Fore.RESET + "Minimum height allowed is 55 centimeters.\n")
                                        
                                    elif height > 300.0:
                                        print(Fore.RED + "\nError: " + Fore.RESET + "Maximum height allowed is 300 centimeters.\n")
                                        
                                    elif int(height) ==  user_info[0][9]:
                                        print("No changes made.\n")
                                        
                                        break
                                    else:
                                        db.update_user_info(user_id, "height", height)
                                        val = val + 1
                                        print(Fore.GREEN + "Height updated successfully!\n" +Style.RESET_ALL)
                                        
                                        break
                                except ValueError:
                                    print(Fore.RED + "\nError: " + Fore.RESET + " Please enter a valid height.\n")
                                    
                        elif field == '5':
                            while True:
                                smoking = input("Do you smoke? ('yes' or 'no'): ")
                                if smoking.lower() == "yes" or smoking.lower() == "no":
                                    if smoking.lower() == user_info[0][10]:
                                        print("No changes made.\n")
                                        
                                    else:
                                        db.update_user_info(user_id, "smoking", smoking)
                                        val = val + 1
                                        print(Fore.GREEN + "Smoking status updated successfully!\n" + Style.RESET_ALL)
                                        
                                    break
                                else:
                                # Handle invalid input
                                    print(Fore.RED + "\nError: " + Fore.RESET + "Please enter 'yes' or 'no'.\n")
                                    
                        elif field == '6':
                            while True:
                                drinking = input("Do you drink? ('yes' or 'no'): ")
                                if drinking.lower() == "yes" or drinking.lower() == "no":
                                    if drinking.lower() == user_info[0][11]:
                                        print("No changes made.\n")
                                        
                                    else:
                                        db.update_user_info(user_id, "drinking", drinking)
                                        val = val + 1
                                        print(Fore.GREEN + "Drinking status updated successfully!\n" +Style.RESET_ALL)
                                        
                                    break
                                else:
                                # Handle invalid input
                                    print(Fore.RED + "Error: " + Fore.RESET + "Please enter 'yes' or 'no'.")
                                    
                        elif field == '7':
                            while True:
                                genderpreferences = input("Enter your new gender preference? ('male' or 'female' or 'na' no preference): ")
                                if genderpreferences.lower() == "male" or genderpreferences.lower() == "female" or genderpreferences.lower() == "na":
                                    if genderpreferences == user_info[0][12]:
                                        print("No changes made.\n")
                                        
                                        break
                                    else:
                                        db.update_user_info(user_id, "genderpreferences", genderpreferences)
                                        val = val + 1
                                        print(Fore.GREEN + "Gender preference updated successfully!\n" +Style.RESET_ALL)
                                        
                                        break
                                else:
                                    # Handle invalid input
                                    print(Fore.RED + "\nError: " + Fore.RESET + "Please enter 'male' or 'female' or 'na' for no preference.\n")
                       
                        elif field == '8':
                            while True:
                                bio = input("Enter new bio (max 100 characters): ")
                                if bio == user_info[0][13]:
                                    print("No changes made.")
                                    
                                    break
                                if len(bio) <= 100:
                                    db.update_user_info(user_id, "bio", bio)
                                    val = val + 1
                                    print(Fore.GREEN + "Bio updated successfully!\n" + Style.RESET_ALL)
                                    
                                    break
                                else:
                                    print(Fore.RED + "\nError: " + Fore.RESET + "Bio should be 100 characters or less.\n")
                                    
                        elif field == '9':
                            Profile()
                            break
                        elif field == '10':
                            print(Fore.LIGHTMAGENTA_EX + "\nSee you!! comeback soon, Happy dating." + Style.RESET_ALL)
                            time.sleep(3)
                            sys.exit()
                        else:
                            print(Fore.RED + "\nError: " + Fore.RESET + "Please enter a valid choice.\n")
                            
                    else:
                        print(Fore.RED + "\nError: " + Fore.RESET + "Please enter a valid choice.\n")
                        
                elif returnVal == False:
                    print(Fore.RED + "\nError: " + Fore.RESET + "Wrong Credentials.\n")
                    
                else:
                    print(Fore.RED + "\nError: " + Fore.RESET + "Wrong User ID provided.\n")
                    
            elif choice.lower() == "no":
                if val == 0:
                    print("No changes made.")
                    
                    break
                else:
                    #print(Fore.GREEN + "Updated!!! \n" + Style.RESET_ALL)
                    Profile()
                    break
            else:
                print(Fore.RED + "\nError: " + Fore.RESET + "Please enter a valid choice.\n")
                
print(Fore.LIGHTMAGENTA_EX + "Heyo!! Welcome to VU Dating App!!!" + Style.RESET_ALL)
while True:
    
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
            print(Fore.LIGHTMAGENTA_EX + "See you!! comeback soon, Happy dating!!!" + Style.RESET_ALL)
            
            break
        else:
            print(Fore.RED + "\nError: " + Fore.RESET + "Please enter a valid choice. \n")
            
    else:
        print(Fore.RED + "\nError: " + Fore.RESET + "Please enter a valid choice. \n")
        
