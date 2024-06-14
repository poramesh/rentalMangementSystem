'''gameRent.py: A Python module containing functions that prompt the
store manager for the customer's ID and the ID of the game(s) they wish
to rent. After performing validity checks and the functionality described
kkhas been rented successfully'''

'''Customers should be identified using their unique ID numbers. For simplicity, we
use 4-digit integers (e.g., 1000-9999) for these IDs. Only customers with active
subscriptions, as verified by the provided subscriptionManager.pyc module, are
considered valid for renting games. Your program should distinguish between
valid and invalid IDs.'''


'''To rent a game, the store manager should provide a customer ID and the game's
ID number. Your program should then:

1. Validate the input and use the provided subscriptionManager.pyc to check
the customer's subscription status. Return an error message if either is not
valid.
2. Depending on the game's availability and the customer's subscription limit,
either allow the manager to rent the game by updating the related records
in the database or return an appropriate message indicating why the rental
cannot proceed.'''

import sqlite3
from xgameSearch import search_games_by_title
from datetime import timedelta,datetime



def customer_id_valid(id):
    if id>=1000 and id<=9999:
        print("The id is within the valid range")
        con = sqlite3.connect('RentalGamesDatabase.db')
        c = con.cursor()

        c.execute("SELECT * FROM Customer WHERE customer_id=?",(id,)) #Tuple Syntax for Single Parameter: When passing a single parameter to the execute method, it should be a tuple. This means you need a comma after id to form a tuple.
        result = c.fetchone()
        c.close()
        con.close()

        if result:
            print("the customer id is valid")
            return 1
        else: 
            print("the customer id not valid")
            return 0
    else: 
        print("the customer id is not in the range")
        return 0

def check_subscription_validity(id,status):
    with sqlite3.connect('RentalGamesDatabase.db') as con:

        c = con.cursor()

        query = "SELECT * FROM Customer where customer_id = ? and subsciption_status = ? "
        #query = "SELECT * FROM Customer WHERE customer_id = :id AND subscription_status = :status"
        #c.execute(query, {'id': id, 'status': status})
        c.execute(query,(id,status))
        result = c.fetchone()
    return result
   

def rent_the_copy(game_id):

    with sqlite3.connect("RentalGamesDatabase.db") as con:
         c = con.cursor()

         c.execute('SELECT * FROM Game_Copies WHERE game_id=:game_id AND availability_status=:Available',{'game_id': game_id,'Available':"Available"})
         result = c.fetchone()
         if result:
             game_id = result[0]
             copy_id = result[1]
             print(f'copy of the game_id: {game_id} is available and the copy_id is{copy_id}')

             c.execute('UPDATE Game_Copies SET availability_status = "Not Available" WHERE game_id = :game_id AND copy_id = :copy_id', {'game_id': game_id, 'copy_id': copy_id})
             con.commit()
             print(f"succesfully rented gameid: {game_id} and the copyid is : {copy_id} ")
         else: 
            print("there are no available copies to rent") 

         return result 
    

def insert_rental_record(cus_id, copy_id, game_id):

    with sqlite3.connect('RentalGamesDatabase.db') as con:
        c= con.cursor()
        rental_date = datetime.now().strftime('%d-%m-%y')
        return_date = None

        query = 'INSERT INTO Rentals (game_id, copy_id, customer_id, rental_date, return_date) VALUES (:game_id, :copy_id, :customer_id, :rental_date, :return_date)'
        c.execute(query,{'game_id':game_id, 'copy_id':copy_id, 'customer_id':cus_id,'rental_date':rental_date,'return_date':return_date})
        con.commit()
        print("succesfully inserted the record")

 


def rent_the_game(cus_id, title):

    games = search_games_by_title(title)
    if games:
        for game in games:
            print(game)
        
        game_id = input("enter the game_id you want to rent form the result: ")
        is_the_copy_rented = rent_the_copy(game_id)
        copy_id = is_the_copy_rented[1]
        if is_the_copy_rented:
            insert_rental_record(cus_id,copy_id,game_id)

    else: print("there are no games")

            



if __name__ == '__main__':

    customer_id = int(input("Enter the Customer_Id to rent the game: "))

    customer_id_valid = customer_id_valid(customer_id)
    if customer_id_valid == 1:
        subcription_active = check_subscription_validity(customer_id,status='Active')
        if(subcription_active):
            print("The subscription is active :)")
            title = input("Enter the title of the game to rent: ")
            rent_the_game(customer_id,title)
        else: print("The subscription is not active")
    