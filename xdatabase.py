
import sqlite3
import csv, random 
import os
from datetime import timedelta,datetime


def creatingTables():
    con = sqlite3.connect('RentalGamesDatabase.db') #The returned Connection object con represents the connection to the on-disk database.


    c = con.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS Games(
              game_id INTEGER PRIMARY KEY,
              title TEXT,
              platform TEXT,
              genre TEXT,
              purchase_price REAL,
              purchase_date TEXT)''')

    c.execute('''CREATE TABLE IF NOT EXISTS Game_Copies(
              game_id INTEGER,
              copy_id INTEGER,
              availability_status TEXT,
              PRIMARY KEY(copy_id,game_id),
              FOREIGN KEY(game_id) REFERENCES Games(game_id))''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS Customer(
              customer_id INTEGER PRIMARY KEY,
              subsciption_status TEXT,
              rental_limit INTEGER)''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS Rentals(
              rental_id INTEGER PRIMARY KEY,
              game_id INTEGER,
              copy_id INTEGER,
              customer_id INTEGER,
              rental_date TEXT,
              return_date TEXT,
              FOREIGN KEY (game_id) REFERENCES Games(game_id),
              FOREIGN KEY (copy_id) REFERENCES Game_Copies(copy_id),
              FOREIGN KEY (customer_id) REFERENCES Customers(customer_id))''') #multiline so triple quotes
    
    con.commit()
    c.execute("SELECT name from sqlite_master WHERE type = 'table';")
    tables = c.fetchall()
    con.close()
    return tables


def insert_rental_data(file_path):

    con = sqlite3.connect('RentalGamesDatabase.db')
    c = con.cursor()


    with open(file_path, 'r') as file:
        reader = csv.DictReader(file, delimiter=';')

        for row in reader:
            #print(row){'Rental Id': 'Rental_224', 'Game Id': 'Game_248', 'Copy Id': 'Copy_3', 'Rental Date': '04-03-24', 'Return Date': ' ', 'Customer Id': 'Cust_1127', '': ''} 
            rental_id = row['Rental Id'].split('_')[1]
            game_id = row['Game Id'].split('_')[1]
            copy_id = row['Copy Id'].split('_')[1]
            rental_date = row['Rental Date']
            return_date = row['Return Date'] if row['Return Date'] else None
            customer_id = row['Customer Id'].split('_')[1]    

            c.execute('''INSERT INTO Rentals(rental_id, game_id, copy_id, customer_id,rental_date, return_date)
                      VALUES (?,?,?,?,?,?)''', (rental_id,game_id,copy_id,customer_id,rental_date,return_date))
            
    
    con.commit()
    con.close()

def insert_customer_data(file_path):
    
    con = sqlite3.connect('RentalGamesDatabase.db')
    c = con.cursor()
  
    customer_data = []

    with open(file_path,'r') as file:
        reader = csv.DictReader(file, delimiter=';') 

        for row in reader:
           # print(row) #{'Customer Id': 'Cust_1129', 'Subscription Status': 'Active', 'Rental Limit': '10', '': ''}
           customer_id = row['Customer Id'].split('_')[1]
           subscription_status = row['Subscription Status']
           rental_limit = row['Rental Limit'] 

           customer_data.append((customer_id,subscription_status, rental_limit))

        c.executemany("INSERT INTO Customer(customer_id, subsciption_status, rental_limit) VALUES (?,?,?)",
                      customer_data)     
        con.commit()
        con.close()   


def insert_game_copies_data(file_path):

    con = sqlite3.connect('RentalGamesDatabase.db')
    c = con.cursor()

    with open(file_path,'r') as file:
        reader = csv.DictReader(file, delimiter=';')

        for row in reader:
            print(row) #{'Game Id': 'Copy_5', 'Copy Id': 'Game_249', 'Availability Status': 'Available', '': ''}
            game_id = row['Game Id'].split('_')[1]
            copy_id = row['Copy Id'].split('_')[1]
            availability_status = row['Availability Status']
            c.execute('INSERT INTO Game_Copies(game_id,copy_id,availability_status) VALUES(:game_id,:copy_id,:availability_status)',
                       {'game_id': game_id, 'copy_id': copy_id, 'availability_status': availability_status}) #{'rentid': rental_id, 'gameid': game_id, 'copyid': copy_id, 'cid': customer_id, 'rdate': rental_date, 'redate': return_date}: will you remmener why you used this ahha its chatgpt if you odnt rmememebr This is a dictionary containing key-value pairs where the keys match the named placeholders in the SQL query, and the values are the actual values you want to insert into the database.
    
    con.commit()
    con.close()

           

def insert_game_info_data(file_path):
    con = sqlite3.connect('RentalGamesDatabase.db')
    c = con.cursor()

    with open(file_path,'r') as file:
        reader = csv.DictReader(file,delimiter = ';')

        for row in reader:
            #print(row) #{'Game Id': '50', 'Platform': 'Xbox', 'Genre': 'Adventures', 'Title': 'Game_50', 'Purchase Price': '43', 'Purchase Date': '18-02-22', '': ''}
            game_id = row['Game Id']
            platform = row['Platform']
            genre = row['Genre']
            title = row['Title']
            purchase_price = row['Purchase Price']
            purchase_date = row['Purchase Date']

            c.execute('INSERT INTO Games VALUES(?,?,?,?,?,?)', 
                      (game_id,title,platform,genre,purchase_price,purchase_date))
        
    con.commit()
    con.close()


if __name__ == "__main__":
    '''tables = creatingTables()
    print("tables in the databases")
    for table in tables:
        print(table)'''

    rental_path = 'data/rental_history.txt'
    customer_path = 'data/customer_data.txt'
    game_copies_path = 'data/game_copies.txt'
    game_info_path = 'data/game_info.txt' 

    #insert_rental_data(rental_path)
    #insert_customer_data(customer_path)
    #insert_game_copies_data(game_copies_path)
    insert_game_info_data(game_info_path)


