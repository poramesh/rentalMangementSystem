''' A Python module containing functions that prompt the
store manager for the ID of the game(s) they wish to return. It should
provide either an appropriate error message or a confirmation message.'''

'''The store manager should be able to return games by providing the game's ID(and copy id for this logic3).
The database should be updated accordingly. If the ID is invalid, or the game is
already available, the program should return an error message. '''

from datetime import timedelta,datetime
import sqlite3


def return_record(game_id,copy_id):

    con = sqlite3.connect('RentalGamesDatabase.db')
    con.row_factory = sqlite3.Row
    c = con.cursor()

    c.execute('SELECT * FROM Rentals WHERE game_id = ? AND copy_id = ?', (game_id,copy_id))

    error = None

    rental_data = c.fetchone()
    if rental_data:
        rental_data_dict = dict(rental_data)
        print(rental_data_dict)
        print(rental_data)
        if rental_data_dict['return_date'] == ' ':
            return_date = datetime.now().strftime('%d-%m-%y')
            c.execute("UPDATE Rentals SET return_date = ? WHERE game_id =? AND copy_id =?", (return_date,game_id,copy_id))
            con.commit()
            print(f'return date has been set to:{return_date}')
        else: 
            error = "The game has already been returned"
    else: 
        error ="There is no existing record with the entered Id"

    con.close()
    return error


def update_availability_status(game_id, copy_id):

    con = sqlite3.connect('RentalGamesDatabase.db')
    con.row_factory = sqlite3.Row
    c = con.cursor()
    c.execute('UPDATE Game_Copies SET availability_status = "Available"  WHERE game_id = ? AND copy_id = ?', (game_id,copy_id))
    
    con.commit()
    con.close()


if __name__ == "__main__":
    game_id = input("enter the game id to be returned: ")
    copy_id = input("enter the copy id to be returned: ")
    returned_value = return_record(game_id,copy_id)

    if returned_value is None:
        print('Succesfully returned the record')
        update_availability_status(game_id,copy_id)
        print("updated the availability status.")
    else: print(returned_value)

