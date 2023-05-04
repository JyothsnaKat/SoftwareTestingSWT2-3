import sqlite3
import bcrypt


class Database:
    """
    Database class for sqlite3
    :param conn: sqlite3 Connection
    :param curr: cursor
    """

    def __init__(self):
        try:
            self.conn = sqlite3.connect("test.db")
            print("Successfully connected to the database")
            self.curr = self.conn.cursor()
        except:
            print("Failed to connect to the database")

    def createTables(self):
        """
        Method for creating tables in the database
        """
        create_cred_table = '''
            CREATE TABLE IF NOT EXISTS cred(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                password TEXT NOT NULL,
                age INTEGER,
                interests TEXT,
                height INTEGER,
                smoking TEXT,
                drinking TEXT,
                preferences TEXT,
                bio TEXT 
            );
        '''

        create_request_table = '''
            CREATE TABLE IF NOT EXISTS request(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                from_user_id INTEGER,
                to_user_id INTEGER,
                status TEXT NOT NULL,
                FOREIGN KEY (from_user_id) REFERENCES cred(id),
                FOREIGN KEY (to_user_id) REFERENCES cred(id)
            );
        '''

        create_matches_table = '''
            CREATE TABLE IF NOT EXISTS matches(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user1_id INTEGER,
                user2_id INTEGER,
                FOREIGN KEY (user1_id) REFERENCES cred(id),
                FOREIGN KEY (user2_id) REFERENCES cred(id)
            );
        '''

        self.curr.execute(create_cred_table)
        self.curr.execute(create_request_table)
        self.curr.execute(create_matches_table)
        self.conn.commit()

    def insertData(self, data):
        """
        Method for inserting data in cred table in the database
        :param data: tuple containing the values for the fields
        """
        insert_data = """
            INSERT INTO cred(username, password, age, interests, height, smoking, drinking, preferences, bio)
            VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?);
        """
        self.curr.execute(insert_data, data)
        self.conn.commit()

    def searchData(self, data):
        """
        Method for searching data in cred table in the database
        :param data: tuple containing the values for the fields
        :return: 1 if user does not exist, 0 otherwise
        """
        search_data = '''
            SELECT * FROM cred WHERE username = (?);
        '''
        self.curr.execute(search_data, data)

        rows = self.curr.fetchall()

        if rows == []:
            return 1
        return 0

    def validateData(self, data, inputData):
        """
        Method for validating data in cred table in the database
        :param data: tuple containing the values for the fields
        :param inputData: tuple containing the values for the fields
        :return: True if username and password match, False otherwise
        """
        validate_data = """
            SELECT * FROM cred WHERE username = (?);
        """

        self.curr.execute(validate_data, data)
        row = self.curr.fetchall()

        if not row:
            return None
        elif row[0][1] == inputData[0]:
            if row[0][2] == bcrypt.hashpw(inputData[1].encode(), row[0][2]):
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
            SELECT request.id, cred.username, cred.interests, cred.height, cred.preferences, cred.bio, request.status 
            FROM request 
            INNER JOIN cred 
            ON request.to_user_id = cred.id 
            WHERE request.from_user_id = (?);
        """
        self.curr.execute(sent_requests, (from_user_id,))
        rows = self.curr.fetchall()
        if rows:
            print("Sent Requests:")
            print("ID\tName\t\tInterests\tHeight\t\tPreferences\tBio\t\t\t\tStatus")
            for row in rows:
                print(f"{row[0]}\t{row[1]}\t{row[2]}\t{row[3]}cm\t{row[4]}\t{row[5][:25]}\t\t{row[6]}")
        else:
            print("You haven't sent any requests yet.")

    def getReceivedRequests(self, to_user_id):
        '''
            Method for Retrieving Received Requests for a User
        '''
        received_requests = """
            SELECT request.id, cred.username, cred.interests, cred.height, cred.preferences, cred.bio, request.status, request.to_user_id
            FROM request 
            INNER JOIN cred 
            ON request.from_user_id = cred.id 
            WHERE request.to_user_id = (?);
        """
        self.curr.execute(received_requests, (to_user_id,))
        rows = self.curr.fetchall()
        if rows:
            print("Received Requests:")
            print("ID\tName\t\tInterests\tHeight\t\tPreferences\tBio\t\t\t\tStatus")
            for row in rows:
                print(f"{row[0]}\t{row[1]}\t{row[2]}\t{row[3]}cm\t{row[4]}\t{row[5][:25]}\t\t{row[6]}")
        else:
            print("You don't have any received requests yet.")
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

        def createTables(self):

        '''
            Method for Creating Tables in Database
        '''

        create_table_cred = '''
            CREATE TABLE IF NOT EXISTS cred(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                password TEXT NOT NULL,
                age INTEGER,
                interests TEXT,
                height INTEGER,
                smoking TEXT,
                drinking TEXT,
                preferences TEXT,
                bio TEXT 
            );
        '''

        create_table_request = '''
            CREATE TABLE IF NOT EXISTS request(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                from_user_id INTEGER NOT NULL,
                to_user_id INTEGER NOT NULL,
                status INTEGER NOT NULL,
                FOREIGN KEY (from_user_id) REFERENCES cred(id),
                FOREIGN KEY (to_user_id) REFERENCES cred(id)
            );
        '''

        create_table_matches = '''
            CREATE TABLE IF NOT EXISTS matches(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user1_id INTEGER,
                user2_id INTEGER,
                FOREIGN KEY (user1_id) REFERENCES cred(id),
                FOREIGN KEY (user2_id) REFERENCES cred(id)
            );
        '''

        self.curr.execute(create_table_cred)
        self.curr.execute(create_table_request)
        self.curr.execute(create_table_matches)
        self.conn.commit()

    def insertData(self, data):

        '''
            Method for Inserting Data in Table in Database
        '''

        insert_data = """
            INSERT INTO cred(username, password, age, interests, height, smoking, drinking, preferences, bio)
            VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?);
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
        elif row[0][1] == inputData[0]:
            if row[0][2] == bcrypt.hashpw(inputData[1].encode(), row[0][2]):
                return True
            else:
                return False    
        else:
            return False

    def getUserId(self, username):
        '''
            Method for Retrieving User ID from the cred table
        '''
        get_user_id = '''
            SELECT id FROM cred WHERE username = (?);
        '''
        self.curr.execute(get_user_id, (username,))
        return self.curr.fetchone()[0]

    def getSentRequests(self, user_id):
        '''
            Method for Retrieving Sent Requests for a User
        '''
        sent_requests = '''
            SELECT c.id, c.username, r.status FROM request r
            JOIN cred c ON r.to_user_id = c.id
            WHERE r.from_user_id = (?);
        '''
        self.curr.execute(sent_requests, (user_id,))
        return self.curr.fetchall()

        def getReceivedRequests(self, user_id):
        '''
            Method for Retrieving Received Requests for a User
        '''
        received_requests = '''
            SELECT c.id, c.username, r.status, r.id as request_id FROM request r
            JOIN cred c ON r.from_user_id = c.id
            WHERE r.to_user_id = (?);
        '''
        self.curr.execute(received_requests, (user_id,))
        return self.curr.fetchall()

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

        request = self.getRequest(request_id)

        # check if the request is accepted by the other user as well
        if request[3] == 1:
            user1_id = request[1]
            user2_id = request[2]
            self.createMatch(user1_id, user2_id)

    def getRequest(self, request_id):
        '''
            Method for Retrieving a Request
        '''
        get_request = '''
            SELECT * FROM request WHERE id = (?);
        '''
        self.curr.execute(get_request, (request_id,))
        return self.curr.fetchone()

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
            WHERE c.id IN (
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

