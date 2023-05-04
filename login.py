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
        if returnVal == True:
            print("Logged In Successfully")

            user_id = db.get_user_id(self.username)
            while True:
                print("\t\t1. Search")
                print("\t\t2. View Matches")
                print("\t\t3. View Requests")
                print("\t\t4. View Profile")
                print("\t\t5. Exit")
                secondOption = input("\t\tEnter Your Option: ")
                if re.search("[0-9]", secondOption):
                    if secondOption == '4':
                        profile = Profile()
                        profile.update()
                    elif secondOption == '2':
                        view_matches = ViewMatches(user_id)
                        view_matches.view()
                    elif secondOption == '3':
                        view_requests = ViewRequests(user_id)
                        view_requests.view()
                    else:
                        print("\t\tWrong Input..\n\n")
                        break
                else:
                    print("\t\tWrong Input..\n\n")
                    break
        elif returnVal == False:
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


class ViewRequests:
    """
        Class for viewing friend requests
    """
    def __init__(self, user_id):
        self.user_id = user_id

    def view(self):
        print("1. Sent Requests")
        print("2. Received Requests")
        option = input("Enter Your Option: ")
        if option == '1':
            sent_requests = db.getSentRequests(self.user_id)
            if not sent_requests:
                print("You have no sent friend requests.")
            else:
                print("Sent friend requests:")
                for r in sent_requests:
                    status = "Accepted" if r[2] == 1 else "Pending"
                    print(f"{r[0]}. {r[1]} - Status: {status}")

                req_id = input("Enter the request ID to delete or type 'back' to go back: ")
                if req_id.lower() == 'back':
                    return
                else:
                    # Bug: Incorrect variable type
                    db.deleteSentRequest(self.user_id, req_id)
                    print("Sent request deleted successfully.")
        elif option == '2':
            received_requests = db.getReceivedRequests(self.user_id)
            if not received_requests:
                print("You have no friend requests.")
            else:
                print("Received friend requests:")
                for r in received_requests:
                    status = "Accepted" if r[2] == 1 else "Pending"
                    print(f"{r[0]}. {r[1]} - Status: {status}")

                req_id = input("Enter the request ID to accept or reject, or type 'back' to go back: ")
                if req_id.lower() == 'back':
                    return
                else:
                    action = input("Type 'accept' or 'reject' to take action on the request: ")
                    if action.lower() == 'accept':
                        db.acceptReceivedRequest(self.user_id, int(req_id))
                        print("Request accepted successfully.")
                    elif action.lower() == 'reject':
                        db.rejectReceivedRequest(self.user_id, int(req_id))
                        print("Request rejected successfully.")
                    else:
                        print("Invalid action. Going back.")
        else:
            print("Invalid option. Going back.")


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
        else:
            print("Your matches:")
            for m in matches:
                # Bug: Index out of range
                print(f"{m[0]}. {m[2]}")







class Profile:

    """
        Class for Profile
    """

    def __init__(self):
        
        while True:
            self.username = input("\t\tConfirm Your Username: ")
            self.password = getpass(prompt="\t\tConfirm Your Password: ")
            data = (self.username,)
            inputData = (self.username, self.password,)
            returnVal = db.validateData(data, inputData)
            if returnVal == True:
                print("Validation Successful")
                data = (self.username,)
                user_info = db.fetchData(data)
                print("Profile Info")
                print(f"Age: {user_info[0][3]}")
                print(f"Interests: {user_info[0][4]}")
                print(f"Height: {user_info[0][5]}")
                print(f"Smoking: {user_info[0][6]}")
                print(f"Drinking: {user_info[0][7]}")
                print(f"Preferred Gender: {user_info[0][8]}")
                print(f"Bio: {user_info[0][9]}")
                break
            elif returnVal == False:
                print("Wrong Credentials")
            else:
                print("Wrong username provided")
    def update(self):
        while True:
            choice = input("Do you want to change any information? (y/n): ")
            if choice.lower() == "y":
                self.username = input("\t\tConfirm Your Username: ")
                self.password = getpass(prompt="\t\tConfirm Your Password: ")
                data = (self.username,)
                inputData = (self.username, self.password,)
                returnVal = db.validateData(data, inputData)
                returnVal = True
                if returnVal == True:
                    user_id = self.username
                    user_info = db.fetchData(data)
                    print("Which info do you prefer to change?")
                    print("1. Age")
                    print("2. Interests")
                    print("3. Height")
                    print("4. Smoking")
                    print("5. Drinking")
                    print("6. Preferred Gender")
                    print("7. Bio")
                    field = input("Enter your choice to change? ")
                    if re.search("[0-9]", field):
                        if field == '1':
                            age = input("Enter new age: ")
                            db.update_user_info(user_id, "age", age)
                            print("Age updated successfully!")
                        elif field == '2':
                            existing_interests = user_info[0][4]
                            complete_interests = ["cricket", "swimming", "painting", "dancing", "reading"]  # Complete list of interests
                            existing_interests_list = existing_interests.split(',')
                            add_interests = [interest for interest in complete_interests if interest not in existing_interests_list]
                            remove_interests = [interest for interest in existing_interests_list]
                            print("1. Add")
                            print("2. Remove")
                            choice_in = input("Do you want to add or remove?")
                            if choice_in == '1':
                                print("Available Interests for Adding:")
                                selected_interests = []
                                for i, interest in enumerate(add_interests, 1):
                                        print(f"{i}. {interest}")
                                while True:
                                    interest_num = input("Enter the number of an interest (or 'done' to finish): ")
                                    if interest_num.lower() == 'done':
                                        break
                                    if set(selected_interests) == set(add_interests):
                                        print("You have selected all possible gender preferences.")
                                        break
                                    try:
                                        interest_index = int(interest_num) - 1
                                        if interest_index < 0 or interest_index >= len(add_interests):
                                            raise ValueError
                                        selected_interest = add_interests[interest_index]
                                        if selected_interest in selected_interests:
                                            print("You have already selected this interest.")
                                        else:
                                            selected_interests.append(selected_interest)
                                            existing_interests_list.append(selected_interest)
                                    except ValueError:
                                            print("Error: Please enter a valid interest number.")
                                updated_interests = ','.join(existing_interests_list)
                                db.update_user_info(user_id, "interests", updated_interests)
                                print("Interests updated successfully!")
                            elif choice_in == '2':
                                print("\nCurrent Interests for Removing:")
                                selected_interests = []
                                for i, interest in enumerate(remove_interests, 1):
                                    print(f"{i}. {interest}")
                                while True:
                                    interest_num = input("Enter the number of an interest (or 'done' to finish): ")
                                    if interest_num.lower() == 'done':
                                        break
                                    if set(selected_interests) == set(remove_interests):
                                        print("You have selected all possible gender preferences.")
                                        break
                                    try:
                                        interest_index = int(interest_num) - 1
                                        if interest_index < 0 or interest_index >= len(remove_interests):
                                            raise ValueError
                                        selected_interest = remove_interests[interest_index]
                                        if selected_interest in selected_interests:
                                            print("You have already selected this interest.")
                                        else:
                                           # selected_interests.remove(selected_interest)
                                            existing_interests_list.remove(selected_interest)
                                    except ValueError:
                                            print("Error: Please enter a valid interest number.")
                                updated_interests = ','.join(existing_interests_list)
                                db.update_user_info(user_id, "interests", updated_interests)
                                print("Interests removed successfully!")
                            else:
                                print("Invalid choice")
                            #interests = input("Enter your interests (comma-separated): ")
                            #interests_set = set(interests.split(","))
                        elif field == '3':
                            height = input("Enter new height: ")
                            db.update_user_info(user_id, "height", height)
                            print("Height updated successfully!")
                        elif field == '4':
                            smoking = input("Do you smoke? (y/n): ")
                            db.update_user_info(user_id, "smoking", smoking)
                            print("Smoking status updated successfully!")
                        elif field == '5':
                            smoking = input("Do you drink? (y/n): ")
                            db.update_user_info(user_id, "smoking", smoking)
                            print("Smoking status updated successfully!")
                        elif field == '6':
                            preferred_gender = input("Enter your preferred gender (male/female/both/no preference): ")
                            db.update_user_info(user_id, "preferred_gender", preferred_gender)
                            print("Preferred gender updated successfully!")
                        elif field == '7':
                            bio = input("Enter new bio (max 100 characters): ")
                            if len(bio) <= 100:
                                db.update_user_info(user_id, "bio", bio)
                                print("Bio updated successfully!")
                            else:
                                print("Bio should be 100 characters or less.")
                        else:
                            print("Invalid choice.")
                    else:
                        print("Invalid choice.")
                elif returnVal == False:
                    print("Wrong Credentials")
                else:
                    print("Wrong username provided")
            elif choice.lower() == "n":
                print("No changes made")
                break
            else:
                print("Invalid choice.")

while True:
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
            break
        else:
            print("\t\tWrong Input..\n\n")
    else:
        print("\t\tWrong Input..\n\n")
