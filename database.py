# Importing Important Libraries

import sqlite3
import bcrypt
from prettytable import PrettyTable

class Database:
    '''
        Database Class for sqlite3
        :params conn - sqlite3Connection
        :params curr - cursor
    '''
    def __init__(self):
        try:
            self.conn = sqlite3.connect("test.db")
            print("Successfully connected to the system")
            self.curr = self.conn.cursor()
        except:
            print("Failed")
    def createUnderage(self):
        '''
            Method for Creating Table in Database
        '''
        create_table_underage = '''
            CREATE TABLE IF NOT EXISTS cred_under(
                id Integer PRIMARY KEY AUTOINCREMENT,
                firstname TEXT NOT NULL,
                lastname TEXT NOT NULL,
                email TEXT NOT NULL,
                age TEXT NOT NULL
            );
        '''

        self.curr.execute(create_table_underage)
        self.conn.commit()
    def insertDataUnder(self, datav):

        '''
            Method for Inserting Data in Table in Database
        '''

        insert_data_under = """
            INSERT INTO cred_under(firstname, lastname, email, age)
            VALUES(?, ?, ?, ?);
        """
        self.curr.execute(insert_data_under, datav)
        self.conn.commit()


    def createTable(self):

        '''
            Method for Creating Table in Database
        '''

        create_table = '''
            CREATE TABLE IF NOT EXISTS cred(
                id Integer PRIMARY KEY AUTOINCREMENT,
                firstname TEXT NOT NULL,
                lastname TEXT NOT NULL,
                email TEXT NOT NULL,
                username TEXT NOT NULL,
                password TEXT NOT NULL,
                age TEXT,
                gender TEXT,
                interests TEXT,
                height FLOAT(2),
                smoking TEXT,
                drinking TEXT,
                genderpreferences TEXT,
                bio TEXT 
            );
        '''
        create_request_table = '''
            CREATE TABLE IF NOT EXISTS request(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                from_user_id TEXT,
                to_user_id TEXT,
                status TEXT NOT NULL,
                FOREIGN KEY (from_user_id) REFERENCES cred(username),
                FOREIGN KEY (to_user_id) REFERENCES cred(username)
            );
        '''

        create_matches_table = '''
            CREATE TABLE IF NOT EXISTS matches(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user1_id TEXT,
                user2_id TEXT,
                FOREIGN KEY (user1_id) REFERENCES cred(username),
                FOREIGN KEY (user2_id) REFERENCES cred(username)
            );
        '''

        self.curr.execute(create_table)
        self.curr.execute(create_request_table)
        self.curr.execute(create_matches_table)
        self.conn.commit()
    def insertData(self, data):

        '''
            Method for Insertig Data in Table in Database
        '''

        insert_data = """
            INSERT INTO cred(firstname, lastname, email, username, password, age, gender, interests, height, smoking, drinking, genderpreferences, bio)
            VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
        """
        self.curr.execute(insert_data, data)
        self.conn.commit()

    def searchData(self, data):

        '''
            Method for Searching Data in Table in Database
        '''

        search_data = '''
            SELECT * FROM cred WHERE username = (?);
        '''

        self.curr.execute(search_data, data)

        rows = self.curr.fetchall()
        #print(rows)

        if rows == []:
            return 1
        return 0

    def validateData(self, data, inputData):

        '''
            Method for Validating Data Table in Database
        '''

        validate_data = """
            SELECT * FROM cred WHERE username = (?);
        """

        self.curr.execute(validate_data, data)
        row = self.curr.fetchall()
        if not row:
            return None
        elif row[0][4] == inputData[0]:
            if row[0][5] == bcrypt.hashpw(inputData[1].encode(), row[0][5]):
                return True
            else:
                return False    
        else:
            return False
    def sendRequest(self, from_user_id, to_user_id):
        '''
            Method for sending Request to a User
        '''
        request_data = (from_user_id, to_user_id, 0)
        add_request = """
            INSERT INTO request(from_user_id, to_user_id, status)
            VALUES(?, ?, ?);
        """
        self.curr.execute(add_request, request_data)
        self.conn.commit()

    def getSentRequests(self, from_user_id):
        '''
            Method for Retrieving Sent Requests for a User
        '''
        sent_requests = """
            SELECT request.id, cred.username, cred.interests, cred.height, cred.genderpreferences, cred.bio, request.status 
            FROM request 
            INNER JOIN cred 
            ON request.to_user_id = cred.username 
            WHERE request.from_user_id = (?);
        """
        self.curr.execute(sent_requests, (from_user_id,))
        rows = self.curr.fetchall()
        if rows:
            table = PrettyTable()
            table.field_names = ["ID", "Name", "Interests", "Height", "Preferences", "Bio", "Status"]
            print("Sent Requests:")
            for row in rows:
                table.add_row([row[0], row[1], row[2], f"{row[3]}cm", row[4], row[5][:25], row[6]])
            print(table)
        return rows

    def getReceivedRequests(self, to_user_id):
        '''
            Method for Retrieving Received Requests for a User
        '''
        received_requests = """
            SELECT request.id, cred.username, cred.interests, cred.height, cred.preferences, cred.bio, request.status, request.to_user_id
            FROM request 
            INNER JOIN cred 
            ON request.from_user_id = cred.username 
            WHERE request.to_user_id = (?);
        """
        self.curr.execute(received_requests, (to_user_id,))
        rows = self.curr.fetchall()
        if rows:
            print("Received Requests:")
            print("ID\tName\t\tInterests\tHeight\t\tPreferences\tBio\t\t\t\tStatus")
            for row in rows:
                print(f"{row[0]}\t{row[1]}\t{row[2]}\t{row[3]}cm\t{row[4]}\t{row[5][:25]}\t\t{row[6]}")
        return rows

    def acceptRequest(self, request_id):
        '''
            Method for Accepting Friend Request
        '''
        accept_request = """
            UPDATE request 
            SET status = 1 
            WHERE id = (?);
        """
        self.curr.execute(accept_request, (request_id,))
        self.conn.commit()

    def rejectRequest(self, request_id):
        '''
            Method for Rejecting Friend Request
        '''
        reject_request = """
            DELETE FROM request 
            WHERE id = (?);
        """
        self.curr.execute(reject_request, (request_id,))
        self.conn.commit()
    def fetchData(self, user_id):
        get_user_by_id = '''
            SELECT * FROM cred WHERE username = (?);
        '''
        self.curr.execute(get_user_by_id, user_id)
        user = self.curr.fetchall()
        print(user)
        return user
    def searchEmail(self,user_email):
        get_user_by_email = '''
            SELECT * FROM cred WHERE email = (?);
        '''
        self.curr.execute(get_user_by_email, user_email)

        rows = self.curr.fetchall()
        if rows == []:
            return 1
        return 0
    def searchEmailUnderage(self,user_email):
        get_user_by_email = '''
            SELECT * FROM cred_under WHERE email = (?);
        '''
        self.curr.execute(get_user_by_email, user_email)

        rows = self.curr.fetchall()
        if rows == []:
            return 1
        return 0
    def update_user_info(self, username, field, new_value):
        '''
        Update a specific field for a given username in the cred table
        '''
        update_query = f'''
            UPDATE cred
            SET {field} = ?
            WHERE username = ?
        '''

        data = (new_value, username)
        self.curr.execute(update_query, data)
        self.conn.commit()
    def getUserId(self, username):
        '''
            Method for Retrieving User ID from the cred table
        '''
        get_user_id = '''
            SELECT id FROM cred WHERE username = (?);
        '''
        self.curr.execute(get_user_id, (username,))
        return self.curr.fetchone()[0]
    def createMatch(self, user1_id, user2_id):
        '''
            Method for Creating Match between two users
        '''
        insert_match = """
            INSERT INTO matches(user1_id, user2_id)
            VALUES(?, ?);
        """
        self.curr.execute(insert_match, (user1_id, user2_id))
        self.conn.commit()

    def getMatches(self, user_id):
        '''
            Method for Retrieving Matches for a User
        '''
        matches_query = """
            SELECT c.id, c.username, c.age, c.interests, c.height, c.smoking, c.drinking, c.preferences, c.bio
            FROM cred c
            WHERE c.username IN (
                SELECT m.user2_id 
                FROM matches m 
                WHERE m.user1_id = (?)
                UNION
                SELECT m.user1_id 
                FROM matches m 
                WHERE m.user2_id = (?)
            );
        """
        self.curr.execute(matches_query, (user_id, user_id))
        return self.curr.fetchall()

    def search(self,userID, min_age, max_age, interests, min_height, smoking_preference, drinking_preference):
        """
            Method for Searching Data in Table in Database
            @param age_range: str - age range in the format 'min-max'
            @param interests: list - list of selected interests
            @param min_height: int - minimum height preferred (in cm)
            @param smoking_preference: str - smoking preference ('yes', 'no', or 'na' for no preference)
            @param drinking_preference: str - drinking preference ('yes', 'no', or 'na' for no preference)
            @return: list - list of rows matching the search criteria
        """
        #sub query to remove the users to which the request has already been sent.
        exclude_query = '''
            SELECT to_user_id FROM request WHERE from_user_id = ? 
        '''
        self.curr.execute(exclude_query, (userID,))
        exclude_usernames = [row[0] for row in self.curr.fetchall()]

        #Adding own user name so that we exclude our profile while searching.
        exclude_usernames.append(userID)

        #Main query to search based on preferences
        search_query = '''
            SELECT * FROM cred 
            WHERE age BETWEEN ? AND ? 
            AND height >= ?
            AND username NOT IN ({})
            {} {} {} {}
        '''
        #user names whose profiles we do not want to fetch
        exclude_usernames_str = ', '.join([f'"{username}"' for username in exclude_usernames])

        #Query to fetch the gender the user prefers to search
        get_user_preferences = '''
            SELECT genderpreferences FROM cred WHERE username = (?);
        '''
        self.curr.execute(get_user_preferences, (userID,))
        gender = self.curr.fetchone()[0]
        gender_condition = ''
        if gender != "na":
            gender_condition = f'AND gender = "{gender}"'

        #params will contain the parameters required for the query to run. It basically replaces the ? in the query
        params = [min_age, max_age, min_height]

        #Joining the interests in the form 'AND interests like cricket AND interests like swimming' and adding it to the param list
        interests_query = ''
        if interests:
            interests_query = ' '.join([f'AND interests LIKE ?' for _ in interests])
            params+= [f'%{interest}%' for interest in interests]

        #Smoking and drinking conditions for the query
        smoking_preference_condition = ''
        drinking_preference_condition = ''

        if smoking_preference.lower() == "yes":
            smoking_preference_condition = 'AND smoking = "yes"'
        elif smoking_preference.lower() == "no":
            smoking_preference_condition = 'AND smoking = "no"'

        if drinking_preference.lower() == "yes":
            drinking_preference_condition = 'AND drinking = "yes"'
        elif drinking_preference.lower() == "no":
            drinking_preference_condition = 'AND drinking = "no"'

        #Formating the search query to include all preferences
        if smoking_preference.lower() == "na" and drinking_preference.lower() == "na" and gender == "na":
            search_query = search_query.format(exclude_usernames_str,interests_query, '', '','')
        else:
            search_query = search_query.format(exclude_usernames_str,interests_query, smoking_preference_condition, drinking_preference_condition,gender_condition)
        
        self.curr.execute(search_query, params)

        rows = self.curr.fetchall()

        return rows
