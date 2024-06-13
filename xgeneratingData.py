import sqlite3
import csv, random 
import os
from datetime import timedelta,datetime



def add_data():

    customer_ids = {}
    platforms = ['PlayStations','Xbox', 'Nintendo']
    genres = ['Actions','Adventures','Shooter','Puzzle']

    cust_path ='data/customer_data.txt'
    game_copies_path = 'data/game_copies.txt'
    rental_path = 'data/rental_history.txt'
    game_info_path = 'data/game_info.txt'


    if not os.path.exists(game_info_path):
        with open(game_info_path,'w') as f:
            f.write('Game Id;Platform;Genre;Title;Purchase Price;Purchase Date') #\t provides 4 spaces anyway i used ;
            for i in range(1,250):
                game_id = i
                platform = random.choice(platforms)
                genre = random.choice(genres)
                title = 'Game_{}_{}'.format(i,genre) #f"Game_{i}"
                purchase_price = random.randint(20,70) #round(random.uniform(20,70),2) 
                purchase_date = (datetime.now()-timedelta(days=random.randint(100,1000))).strftime('%d-%m-%y')
                no_of_copies = random.randint(3,11)  #return any integer from a to b inclusive.
                f.write(f'\n{game_id};{platform};{genre};{title};{purchase_price};{purchase_date}')



    if not os.path.exists(cust_path):
        with open(cust_path,'w') as cust:

            cust.write(f'Customer Id;Subscription Status;Rental Limit')
            for i in range(1000,1131):
                cust_id = f"Cust_{i}"
                subscription_status = random.choices(['Active','Not Active'],[85,15])[0] # Python selects a random element from a non-empty sequence, such as a list, tuple, or string. it would result it in errror if there was no square bracket since it expects a single sequence as its arguments
                if subscription_status == 'Active':
                    rental_limit = random.randint(7,11) 
                    customer_ids[cust_id]= rental_limit
                else: rental_limit = 0
                cust.write(f'\n{cust_id};{subscription_status};{rental_limit}')


    if not os.path.exists(game_copies_path):
        with open(game_copies_path, 'w') as game_copies:
            game_copies.write('Game Id;Copy Id;Availability Status')


            if not os.path.exists(rental_path):
                     with open(rental_path, 'w') as rental:
                        rental.write('Rental Id;Game Id;Copy Id;Rental Date;Return Date;Customer Id')
                        count=0

                        for i in range(1,250):

                            no_of_copy = random.randint(1,7)

                            for j in range(1,no_of_copy):
                                copy_id = f'Copy_{j}'
                                game_id = f'Game_{i}'
                                rental_id = f'Rental_{count}'
                                availability_status = random.choices(['Available','Not Available'],[70,30])[0] #The random.choice() function in Python doesn't accept a second argument as weights when providing the choices as a list. It only accepts a single argument, which is the list of choices. If you want to specify weights for the choices, you should use random.choices() instead.
                               
                                game_copies.write(f'\n{game_id};{copy_id};{availability_status}')

                                
                                if availability_status == 'Not Available':
                                    
                                    print('why')
                                    count = count+1
                                    customer_id = random.choice(list(customer_ids.keys()))
                                    rental_date = (datetime.now()-timedelta(days=random.randint(20,200))).strftime('%d-%m-%y')
                                    return_date = (datetime.strptime(rental_date,'%d-%m-%y') + timedelta(days=random.randint(1,40))).strftime('%d-%m-%y')#conversion is necessary cause we are performing arthmetic operation with datetime object
                                    
                                    if random.choice([True,False]):
                                        return_date = ' '
                                    
                                    rental.write(f'\n{rental_id};{game_id};{copy_id};{rental_date};{return_date};{customer_id}')


if __name__ == "__main__":
    add_data()