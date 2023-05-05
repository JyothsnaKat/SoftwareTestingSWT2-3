# Importing Important Libraries

import sqlite3
import bcrypt


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
                height TEXT,
                smoking TEXT,
                drinking TEXT,
                genderpreferences TEXT,
                bio TEXT 
            );
        '''

        self.curr.execute(create_table)
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
