import psycopg2
import random
from prettytable import PrettyTable
from datetime import datetime

def insertPlayer():
    # Initialize variables
    name = input("Enter player name: ")

    #Automate player_id
    cur.execute("SELECT pid FROM PLAYERS ORDER BY pid DESC")
    pids = cur.fetchall()
    if pids == []:
        player_id = 1
    else:
        player_id = pids[0][0] + 1
    # player_id = random.randint(10**8, (10**9)-1)

    # Initialize other statistics with input validation
    stats = ["pace", "shooting", "passing", "dribbling", "defending", "physicality"]
    player_stats = {}

    randomizeStats = input("Do you wish to randomize stats (y/n): ")
    
    
    for stat in stats:
        #normal stats input loop
        if randomizeStats != "y":
            value = input(f"Enter the player's {stat} rating: ")
            while not value.isdigit() or int(value) > 100 or int(value) < 0:
                print(f"{stat} must be an integer less than 100")
                value = input(f"Enter {stat} (integer): ")
            value = int(value)
        #randomize stats from 60-100
        else:
            value = random.randint(60, 100)

        #store the stat
        player_stats[stat] = value

    # Calculate the overall as the average of other stats
    overall = sum(player_stats.values()) / len(player_stats)

    #Actual commit statement
    cur.execute("INSERT INTO players (name,pid,pace,shooting,passing,dribbling,defending,physicality,overall) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)",(name,player_id,player_stats["pace"],player_stats["shooting"],player_stats["passing"],player_stats["dribbling"],player_stats["defending"],player_stats["physicality"],overall))
    con.commit()

def insertGame():
    # Input for game data

    #date declaration
    date = ""

    #date input validation
    while True:
        date_str = input("Enter the date of the game (YYYY-MM-DD HH:MM:SS): ")
        try:
            date = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
            break
        except ValueError:
            print("Invalid date format. Please use the format YYYY-MM-DD HH:MM:SS.")

    #location variable
    location = input("Enter the location: ")

    #left and right team score initilaization and validation
    leftteamscore = (input("Enter the left team score: "))
    while not leftteamscore.isdigit():
        print(f"Score must be an integer")
        leftteamscore = input(f"Enter the left team score: ")
    leftteamscore = int(leftteamscore)
    rightteamscore = (input("Enter the right team score: "))
    while not rightteamscore.isdigit():
        print(f"Score must be an integer")
        rightteamscore = input(f"Enter the right team score: ")
    rightteamscore = int(rightteamscore)
    
    # Generate a random 9-digit game ID
    game_id = random.randint(10**8, (10**9)-1)

    # Actual data insertion
    cur.execute("INSERT INTO games (date, location, leftteamscore, rightteamscore, gid) VALUES (%s, %s, %s, %s, %s)", (date, location, leftteamscore, rightteamscore, game_id))
    con.commit()

# view all games in the games table
def viewAllGames():
    cur.execute("SELECT date, location, leftteamscore, rightteamscore FROM games")
    games = cur.fetchall()

    table = PrettyTable()
    table.field_names = ["date", "location", "leftteamscore", "rightteamscore"]

    for row in games:
        table.add_row(row)

    print(table)

def insertTeam():
    name = input("Enter team name: ")
    league = input("Enter team league: ")

    #Automate team_id
    team_id = random.randint(10**8, (10**9)-1)

    #add check to make sure randomized tid id not already in team! / not urgent

    # Initialize other statistics with input validation
    stats = ["atkrating", "mdrating", "dfrating"]
    team_stats = {}

    randomizeStats = input("Do you wish to randomize stats (y/n): ")
    
    
    for stat in stats:
        #normal stats input loop
        if randomizeStats != "y":
            value = input(f"Enter the teams's {stat} rating: ")
            while not value.isdigit() or int(value) > 100 or int(value) < 0:
                print(f"{stat} must be an integer less than 100")
                value = input(f"Enter {stat} (integer): ")
            value = int(value)
        #randomize stats from 70-100
        else:
            value = random.randint(70, 100)

        #store the stat
        team_stats[stat] = value

    # Calculate the overall as the average of other stats
    overall = sum(team_stats.values()) / len(team_stats)

    #Actual commit statement
    cur.execute("INSERT INTO teams (name,league,atkrating,mdrating,dfrating,overall,tid) VALUES (%s,%s,%s,%s,%s,%s,%s)",(name,league,team_stats["atkrating"],team_stats["mdrating"],team_stats["dfrating"],overall,team_id))
    con.commit()

# view all team names in the teams table
def viewAllTeams():
    cur.execute("SELECT name FROM teams")
    teams = cur.fetchall()

    table = PrettyTable()
    table.field_names = ["name"]

    for row in teams:
        table.add_row(row)

    print(table)

#search for a team's players
def displayTeam():
    teamName = input("Enter the Team Name: ")
    teamName = teamName.strip()
    cur.execute("SELECT tid FROM teams WHERE name ILIKE %s",(teamName,))
    team = cur.fetchall()
    #after getting the tid, do input validation and fetch the players
    if team == []:
        print("This team does not exist")
        return
    cur.execute("SELECT p.pid, p.name, pf.position FROM playsFor pf NATURAL JOIN players p WHERE pf.tid = %s",(team[0][0],))
    players = cur.fetchall()

    table = PrettyTable()
    table.field_names = ["pid", "name", "position"]

    for row in players:
        table.add_row(row)

    print(table)

# view all players in the players table
def viewAllPlayers():
    cur.execute("SELECT name FROM players")
    teams = cur.fetchall()

    table = PrettyTable()
    table.field_names = ["name"]

    for row in teams:
        table.add_row(row)

    print(table)

def displayPlayer():
    playerName = input("Enter the Player's Name: ")
    playerName = playerName.strip()
    cur.execute("SELECT * FROM players WHERE name ILIKE %s",(playerName,))
    player = cur.fetchone()
    if player == None:
        print("This player does not exist")
        return
    table = PrettyTable()
    table.field_names = ["name", "pace", "shooting", "passing", "dribbling", "defending", "physicality", "overall"]
    table.add_row(player[0:-1])
    print(table)

def addPlayerToTeam():
    playerName = input( "Enter the player's name: " )
    playerName = playerName.strip()
    teamName = input( "Enter the team name: " )
    teamName = teamName.strip()
    
# database connection request. change fields according to your local machine's corresponding value
con = psycopg2.connect(
database="dbproj",
user="postgres",
password="password",
host="localhost",
port= '5432'
)

cur = con.cursor()

# postgres super user menu
while True:
    print("")
    print("Welcome back to FIFAgres! What would you like to do?")
    print("")
    print("1. Create a player")
    print("2. Create a team")
    print("3. Create a game")
    print("4. View all games")
    print("5. View all teams")
    print("6. Display a team's roster")
    print("7. View all players")
    print("8. Display a player's information")
    print("9. Add player to team")
    print("0. Exit")
    print("")
    choice = input("Enter your choice: ")

    if choice == "1":
        insertPlayer()
    elif choice == "2":
        insertTeam()
    elif choice == "3":
        insertGame()
    elif choice == "4":
        viewAllGames()
    elif choice == "5":
        viewAllTeams()
    elif choice == "6":
        displayTeam()
    elif choice == "7":
        viewAllPlayers()
    elif choice == "8":
        displayPlayer()
    elif choice == "9":
        addPlayerToTeam()
    elif choice == "0":
        print("")
        print("Thank you for using FIFAgres! Have a nice day!")
        print("")
        con.close()
        break
    else:
        print("")
        print("Invalid input! Please select from one of the inputs below.")