import sqlite3
#Db name
DATABASE_NAME='portfolio_database.db'

def add_db_table(table_name, columns):#columns is a tuple and all are strings
        try:
            dbcon=sqlite3.connect(DATABASE_NAME)
            dbcon.execute(f'CREATE TABLE {table_name} {columns}')
            dbcon.close()
            print( '****db project tables created successfuly****')

        except sqlite3.OperationalError as err:
            print(f'****db could not be created ({err}) ****')

def save(table_name,values):
        dbcon=sqlite3.connect(DATABASE_NAME)
        cur=dbcon.cursor()
        if table_name=='Projects':
             cur.execute("INSERT INTO Projects (name,client,description,project_image_url,project_image_filename) VALUES (?,?,?,?,?)",values)
        elif table_name =='Messages':
             cur.execute("INSERT INTO Messages (visitor_name,visitor_email,subject,message) VALUES (?,?,?,?)",values)
        elif table_name =='Testimonials':
             cur.execute("INSERT INTO Testimonials (client_name,client_message) VALUES (?,?)",values)
        dbcon.commit()
        dbcon.close()

def delete(table_name,id):
        dbcon = sqlite3.connect(DATABASE_NAME)
        cur = dbcon.cursor()

        # Use parameterized query to safely delete the row
        query = f"DELETE FROM {table_name} WHERE id = ?"
        cur.execute(query, (id))

        dbcon.commit()
        dbcon.close()


def get( table_name):
        dbcon=sqlite3.connect(DATABASE_NAME)
        cur=dbcon.cursor()
        cur.execute(f"select * from {table_name}")
        rows = cur.fetchall()
        dbcon.close()
        return rows

class Project:
    def __init__(self, name, client, description, project_image_url, project_image_filename):
        self.name=name
        self.client=client
        self.description=description
        self.project_image_url=project_image_url
        self.project_image_filename=project_image_filename
        self.db_table_name='Projects'
        db_table_name='Projects'

    def __str__(self) -> str:
        return self.name
        
    def create_db_table():
         add_db_table('Projects','(ID INTEGER PRIMARY KEY AUTOINCREMENT,name TEXT , client TEXT, description TEXT, project_image_url TEXT, project_image_filename TEXT)')
    
    def save_to_db(self):
        save(self.db_table_name, (self.name,self.client,self.description,self.project_image_url,self.project_image_filename) )
        

    def remove_from_db(id):
        delete('Projects', id)

    def get_from_db():
        return get('Projects')

class Message:
    def __init__(self, name, email,subject, message):
        self.visitor_name=name
        self.visitor_email=email
        self.message=message
        self.subject=subject
        self.db_table_name='Messages'


    def __str__(self) -> str:
        return f"{self.subject} -{self.visitor_name}"
    
    def create_db_table():
         add_db_table('Messages','(ID INTEGER PRIMARY KEY AUTOINCREMENT, visitor_name TEXT NOT NULL, visitor_email EMAIL NOT NULL, subject TEXT  NOT NULL, message TEXT NOT NULL , time_submitted TIMESTAMP DEFAULT CURRENT_TIMESTAMP)')

    def add_to_db(self):
         save(self.db_table_name,(self.visitor_name,self.visitor_email, self.subject, self.message))

    def get_from_db():
        return get('Messages')
    
    def delete_message(id):
         delete("messages", id)


class Testimony:
    def __init__(self, name, message):
        self.client_name=name
        self.client_message=message
        self.db_table_name='Testimonials'


    def __str__(self) -> str:
        return f"{self.client_message} -{self.client_name}"
    
    def create_db_table():
         add_db_table('Testimonials','(ID INTEGER PRIMARY KEY AUTOINCREMENT, client_name TEXT NOT NULL, client_message TEXT NOT NULL , time_submitted TIMESTAMP DEFAULT CURRENT_TIMESTAMP)')

    def add_to_db(self):
         save(self.db_table_name,(self.client_name, self.client_message))

    def get_from_db():
        return get('Testimonials')
    
    def delete_message(id):
         delete("Testimonials", id)

Project.create_db_table()
Message.create_db_table()
Testimony.create_db_table()