import re
from prettytable import PrettyTable
from database import Database
import sys
from colorama import init, Fore, Style

db = Database()
class Search():
    """
        Class for Search
        @param age_range
        @param interests
        @param height
        @param smoking_preference
    """

    def __init__(self):
        while True:
            try:
                self.age_range = input("Enter your preferred age range in the format 'min-max'(e.g. 20-30):")
                age_range_regex = re.compile(r'^(\d+)-(\d+)$')
                match = age_range_regex.match(self.age_range)
                if match:
                    self.min_age = int(match.group(1))
                    self.max_age = int(match.group(2))
                    if self.min_age < 18 or self.max_age > 100:
                        raise ValueError(Fore.RED + "Error:" + Fore.RESET + "Please enter a valid age range between 18 and 100.")
                    elif self.min_age > self.max_age or self.min_age == self.max_age:
                        raise ValueError(Fore.RED + "Error:" + Fore.RESET + "Please enter a valid age range in the format 'min-max'(e.g. 20-30).")
                    break
                else:
                    raise ValueError(Fore.RED + "Error:" + Fore.RESET +  "Please enter a valid age range in the format 'min-max'(e.g. 20-30).")
            except ValueError as e:
                    print(e)

        interests = ['cricket', 'swimming', 'painting', 'dancing', 'reading']
        print("Select your preferred interests from the list below (enter the number).")
        for i, interest in enumerate(interests):
            print(f"{i+1}. {interest}")
        self.interests = []
        while True:
            try:
                if len(self.interests) == len(interests):
                    print("You have selected all possible interests. \n")
                    break
                interest_num = input("Enter the number of an interest (or 'na' for no preference or 'done' to finish): ")
                if interest_num.lower() == 'done':
                    if len(self.interests) == 0:
                        print(Fore.RED + "Error:" + Fore.RESET + "Please select at least one interest or na for no preference.")
                        continue
                    else:
                        break
                elif interest_num.lower() == 'na':
                    print("Please note that on choosing na all the previously entered interests, if any will be dropped")
                    self.interests = []
                    break
                interest_index = int(interest_num) - 1
                if interest_index < 0 or interest_index >= len(interests):
                    raise ValueError
                selected_interest = interests[interest_index]
                if selected_interest in self.interests:
                    print("You have already selected this interest.")
                else:
                    self.interests.append(selected_interest)
            except ValueError:
                print(Fore.RED + "Error:" + Fore.RESET + "Please enter a valid interest number.")

        while True:
            try:
                self.min_height = int(input("Enter the minimum height preferred (in cm): "))
                if self.min_height < 55 or self.min_height > 300:
                    raise ValueError
                break
            except ValueError:
                print(Fore.RED + "Error:" + Fore.RESET + "Please enter a valid height between 55 and 300 cm.")
        while True:
            self.smoking_preference = input("Enter your smoking preference 'yes' or 'no' or 'na' for no preference: ")
            if self.smoking_preference.lower() == "yes" or self.smoking_preference.lower() == "no" or self.smoking_preference.lower() == "na":
                break
            else:
                print(Fore.RED + "Error:" + Fore.RESET + "Please enter 'yes' or 'no' or 'na' for no preference.")
        while True:
            self.drinking_preference = input("Enter your drinking preference 'yes' or 'no' or 'na' for no preference: ")
            if self.drinking_preference.lower() == "yes" or self.drinking_preference.lower() == "no" or self.drinking_preference.lower() == "na":
                break
            else:
                print(Fore.RED + "Error:" + Fore.RESET + "Please enter 'yes' or 'no' or 'na' for no preference")


    def view(self,data,userID):
        flag = 0
        # Prompt user for input
        while True:
            if not data:
                    print("No matches found according to the preferences entered.\n")
                    print("1. Search again")
                    print("2. Main Menu")
                    print("3. Exit")
                    user_input = input("Enter your choice: ")
                    if user_input == '1':
                        flag=0
                        return 2
                    elif user_input == '2':
                        flag=0
                        return 3
                    elif user_input == '3':
                        print("Bye Bye!! Come back to us!! Happy dating!! \n")
                        sys.exit()
                    else:
                        print(Fore.RED + "Error:" + Fore.RESET + "Wrong Input. Please enter a valid choice.\n")
                        flag=1
            #displaying all search results in a table
            else:
                table = PrettyTable()
                table.field_names = ["User ID", "Name", "Age"]
                for result in data:
                    table.add_row([result[4], result[1]+" "+result[2],result[6]])
                if not flag:
                    print("\nBased on your preferred gender and other preferences you entered just now, here is a list of potential matches:")
                    print(table)
                    print("\n")
                    #user prompted to either view profile, search again or go back to the main menu
                    print("1. View Profile")
                    print("2. Search again")
                    print("3. Main Menu")
                    print("4. Exit")
                user_input = input("Enter your choice: ")
                if re.search("[0-9]",user_input):
                    #View profile
                    if user_input == '1':
                        flag=0
                        while True:
                            found = False
                            user_id = input("Please enter the userID of the profile you want to view:")
                            if not any(result[4]==user_id for result in data):
                                print(Fore.RED + "Error:" + Fore.RESET + "Please enter userID from the list.\n")
                                continue
                            for result in data:
                                if result[4]==user_id:
                                    profile = PrettyTable()
                                    profile.field_names = ["userID", "Name", "Age", "Interests", "Height","Smoking","Drinking","Gender","Bio"]
                                    profile.add_row([result[4],result[1]+" "+result[2],result[6],result[8],result[9],result[10],result[11],result[7],result[13]])
                                    print(profile)
                                    #Inside view profile to either send a request or go back to search results
                                    while True:
                                        print("1. Send request")
                                        print("2. Back to search results")
                                        user_input = input("Your choice: ")
                                        if user_input == '1':
                                            db.sendRequest(userID,result[4])
                                            data = [d for d in data if d[4] != user_id]
                                            print(Fore.GREEN + "Request sent successfully!"+Style.RESET_ALL)
                                            table.clear_rows()
                                            found=True
                                            break
                                        elif user_input == '2':
                                            found=True
                                            break
                                        else:
                                            print(Fore.RED + "Error:" + Fore.RESET + "Please enter a valid choice.\n")
                                            continue
                            if found:
                                break
                    #Search new results
                    elif user_input == '2':
                        flag=0
                        return 2
                    #Main menu
                    elif user_input == '3':
                        flag=0
                        return 3
                    #Exit
                    elif user_input == '4':
                        print("Bye Bye!! Come back to us!! Happy dating!! \n\n")
                        sys.exit()
                    else:
                        print(Fore.RED + "Error:" + Fore.RESET + "Please enter a valid choice.\n")
                        flag=1
                else:
                    print(Fore.RED + "Error:" + Fore.RESET + "Wrong Input. Please enter a valid choice.\n")
                    flag=1

                    


