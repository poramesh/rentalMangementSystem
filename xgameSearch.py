'''Your program should include functionality to search for a game based on its title.
Given a search term (e.g., FIFA), your program should return a complete list of
games with all their associated information (namely, title, platform, genre, and
availability).'''


import sqlite3

def search_games_by_title(title):
    conn = sqlite3.connect('RentalGamesDatabase.db')
    c = conn.cursor()

    c.execute("SELECT * FROM Games WHERE title LIKE ?", ('%' + title + '%',)) #('%' + title + '%',): This is a tuple containing the parameter value to be substituted for the ? placeholder in the SQL query. The % characters are wildcard characters in SQL, meaning they match any sequence of characters. By placing them before and after the title variable, the query will match any title that contains the value of title.
    games_title = c.fetchall()

    conn.close()
    return games_title

if __name__ == '__main__':
    title = input("Enter search term: ")
    games = search_games_by_title(title)
    if games:
        print("Search Results:")
        for game in games:
            print(game)
    else:
        print("No games found.")