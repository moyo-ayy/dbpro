import bcrypt
from datetime import datetime
from getpass import getpass
import psycopg2
from prettytable import PrettyTable
import random
import re

def insertUser():
    # Initialize variables
    username = input("Enter your username: ")
    type = ""
    password = ""

    cur.execute("SELECT username FROM users WHERE username = %s",(username,))
    usernameExists = cur.fetchall()
    while usernameExists != []:

        print("This username is taken! Please try a different one!")
        username = input("Enter your username: ")
        cur.execute("SELECT username FROM users WHERE username = %s",(username,))
        usernameExists = cur.fetchall()

    print("What type of user are you?: ")
    print("1. Fan")
    print("2. Team Organizer")
    print("3. Game Organizer")

    choice = input("Enter your choice: ")

    if choice == "1":
        type = "fan"
    elif choice == "2":
        type = "club owner"
    elif choice == "3":
        type = "game organizer"
    else:
        print("Invalid input!")
        return

    password = getpass("Enter your password: ")
    confirmPassword = getpass( "Confirm password: " )
    if password != confirmPassword:
        print()
        print("Confirmation password does not match!")
        return
    password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    cur.execute("INSERT INTO users (username, type, password) VALUES (%s,%s,%s)",(username,type,password))
    con.commit()

    print()
    print( "User successfully created!" )

def viewAllUsers():
    cur.execute("SELECT name, type FROM users ORDER BY username")
    games = cur.fetchall()

    table = PrettyTable()
    table.field_names = ["name", "type"]

    for row in games:
        table.add_row(row)

    print(table)
    
def loginUser():
    username = input("Enter your username: ")
    password = getpass("Enter your password: ")
    
    cur.execute("SELECT * FROM users where username = %s",(username,))
    userInfo = cur.fetchone()
    
    if userInfo == None:
        print()
        print("Username does not exist!")
        return

    actualPassword = bytes.fromhex(userInfo[2][2:])

    # Check if the entered password matches the stored hashed password
    if bcrypt.checkpw(password.encode('utf-8'), actualPassword):
        print("\nLogin successful!")
        cur.execute("SELECT type FROM users where username = %s",(username,))
        userType = cur.fetchone()
        userType = userType[0]
        userType = userType.strip()
        userType = userType.lower()
        userType = re.sub("[^a-z]", "", userType)
        return userType
    else:
        print("\nPassword is incorrect!")
        return

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

    # Initialize other statistics with input validation
    stats = ["pace", "shooting", "passing", "dribbling", "defending", "physicality"]
    player_stats = {}

    randomizeStats = input("Do you wish to randomize stats? (y/n): ")
    
    
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

    print()
    print( "Player successfully created!" )

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

    leftTeamName = input("Enter the Left Team Name: ")
    leftTeamName = leftTeamName.strip()
    cur.execute("SELECT tid FROM teams WHERE name = %s",(leftTeamName,))
    leftTeamID = cur.fetchall()
    #after getting the tid, do input validation and fetch the players
    if leftTeamID == []:
        print("This team does not exist")
        return

    rightTeamName = input("Enter the Right Team Name: ")
    rightTeamName = rightTeamName.strip()
    cur.execute("SELECT tid FROM teams WHERE name = %s",(rightTeamName,))
    rightTeamID = cur.fetchall()
    #after getting the tid, do input validation and fetch the players
    if leftTeamID == []:
        print("This team does not exist")
        return

    # Generate a random 9-digit game ID
    game_id = random.randint(10**8, (10**9)-1)

    # Actual data insertion
    cur.execute("INSERT INTO games (date, location, leftteamscore, rightteamscore, gid, leftteam, rightteam) VALUES (%s, %s, %s, %s, %s, %s, %s)", (date, location, leftteamscore, rightteamscore, game_id, leftTeamID[0][0], rightTeamID[0][0]))
    con.commit()

    print()
    print( "Game successfully created!" )

# view all games in the games table
def viewAllGames():
    cur.execute("SELECT date, location, leftteamscore, rightteamscore, t1.name AS leftTeamName, t2.name as rightTeamName FROM games g JOIN \
        teams t1 ON leftteam = t1.tid JOIN teams t2 ON rightteam = t2.tid ORDER BY date")
    games = cur.fetchall()

    table = PrettyTable()
    table.field_names = ["date", "location", "leftteamscore", "rightteamscore", "leftteamname", "rightteamname"]

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

    print()
    print( "Team successfully created!" )

#create a manager
def insertManager():
    # Initialize variables
    name = input("Enter the new coach's name: ")

    #Automate player_id
    cur.execute("SELECT mid FROM managers ORDER BY mid DESC")
    mids = cur.fetchall()
    if mids == []:
        manager_id = 1
    else:
        manager_id = mids[0][0] + 1

    teamName = input("Enter the team that the coach coaches: ")
    teamName = teamName.strip()
    cur.execute("SELECT tid FROM teams WHERE name = %s",(teamName,))
    tid = cur.fetchall()
    #after getting the tid, do input validation and fetch the players
    if tid == []:
        print("\nThis team does not exist!")
        return

    cur.execute("SELECT tid FROM managers WHERE tid = %s",(tid))
    if (cur.fetchone()):
        print("\nThis team already has a coach!")
        return
    
    cur.execute("INSERT INTO managers (name, tid, mid) VALUES (%s,%s,%s)",(name,tid[0][0],manager_id))

    print("\nCoach successfully created!")

    con.commit()


# view all team names in the teams table
def viewAllTeams():
    cur.execute("SELECT name FROM teams ORDER BY name")
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
    cur.execute("SELECT tid FROM teams WHERE name = %s",(teamName,))
    team = cur.fetchall()
    #after getting the tid, do input validation and fetch the players
    if team == []:
        print()
        print("This team does not exist!")
        return
    cur.execute("SELECT p.name, pf.position FROM playsFor pf NATURAL JOIN players p WHERE pf.tid = %s",(team[0][0],))
    players = cur.fetchall()

    table = PrettyTable()
    table.field_names = [ "name", "position"]

    for row in players:
        table.add_row(row)

    print(table)

# view all players in the players table
def viewAllPlayers():
    cur.execute("SELECT name FROM players ORDER BY name")
    teams = cur.fetchall()

    table = PrettyTable()
    table.field_names = ["name"]

    for row in teams:
        table.add_row(row)

    print(table)

def viewAllManagers():
    cur.execute("SELECT m.name,t.name FROM managers m JOIN teams t ON m.tid = t.tid")
    managers = cur.fetchall()

    table = PrettyTable()
    table.field_names = ["Name", "Team Name"]

    for row in managers:
        table.add_row(row)
    
    print(table)

def displayPlayer():
    playerName = input("Enter the name of the player you would like to view: ")
    playerName = playerName.strip()
    cur.execute("SELECT * FROM players WHERE name = %s",(playerName,))
    player = cur.fetchone()
    if player == None:
        print()
        print("This player does not exist!")
        return
    table = PrettyTable()
    table.field_names = ["name", "pace", "shooting", "passing", "dribbling", "defending", "physicality", "overall"]
    table.add_row(player[0:-1])
    print(table)

def addPlayerToTeam():
    playerName = input( "Which player are you assigning to a team?: " )
    playerName = playerName.strip()

    # check if player exists in players table
    cur.execute( "SELECT * FROM players WHERE name = %s", (playerName,) )
    player = cur.fetchone()
    if player == None:
        print()
        print("This player does not exist!")
        return
    playerid = player[8]
    
    # check if player already plays for some team
    cur.execute( "SELECT * FROM playsfor WHERE pid = %s", (playerid,) )
    alreadyPlays = cur.fetchone()
    if alreadyPlays != None:
        print()
        print( "This player already plays for a team!" )
        return
    
    teamName = input( "Which team is this player playing for?: " )
    teamName = teamName.strip()

    # check if team exists in teams table
    cur.execute( "SELECT * FROM teams WHERE name = %s", (teamName,) )
    team = cur.fetchone()
    if team == None:
        print()
        print("This team does not exist!")
        return
    teamid = team[6]
    
    position = input( "What position is this player going to play?: " )
    position = position.strip()

    cur.execute( "INSERT INTO playsfor (pid, tid, position) VALUES (%s, %s, %s)", (playerid, teamid, position) )
    con.commit()

    print()
    print( "Player successfully added to team!" )

# remove a player from a team
def removePlayerFromTeam():
    playerName = input( "Which player are you removing from a team?: " )
    playerName = playerName.strip()

    # check if player exists in players table
    cur.execute( "SELECT * FROM players WHERE name = %s", (playerName,) )
    player = cur.fetchone()
    if player == None:
        print()
        print("This player does not exist!")
        return
    playerid = player[8]
    
    # check if player already plays for some team
    cur.execute( "SELECT * FROM playsfor WHERE pid = %s", (playerid,) )
    alreadyPlays = cur.fetchone()
    if alreadyPlays == None:
        print()
        print( "This player already does not play for any team!" )
        return

    cur.execute( "DELETE FROM playsfor WHERE pid = %s", (playerid,) )
    con.commit()

    print()
    print( "Player successfully removed from team!" )

def removePlayer():
    playerName = input( "Which player are you removing from a team?: " )
    playerName = playerName.strip()

    # check if player exists in players table
    cur.execute( "SELECT * FROM players WHERE name = %s", (playerName,) )
    player = cur.fetchone()
    if player == None:
        print()
        print("This player does not exist!")
        return

    cur.execute( "DELETE FROM players WHERE name = %s", (playerName,) )
    con.commit()

    print()
    print( "Player successfully deleted!" )
    
def removeTeam():
    teamName = input( "Which team are you deleting?: " )
    teamName = teamName.strip()

    # check if team exists in teams table
    cur.execute( "SELECT * FROM teams WHERE name = %s", (teamName,) )
    team = cur.fetchone()
    if team == None:
        print()
        print("This team does not exist!")
        return

    cur.execute( "DELETE FROM teams WHERE name = %s", (teamName,) )
    con.commit()

    print()
    print( "Team successfully deleted!" )

def removeGame():
    gameLocation = input( "Enter the location of the game you would like to delete: " )
    gameLocation = gameLocation.strip()
    gameLocation = gameLocation.lower()
    
    # check if any games were played in this location
    cur.execute( "SELECT * FROM games WHERE LOWER(location) = %s", (gameLocation,) )
    game = cur.fetchall()
    if game == []:
        print()
        print( "No games were ever played in this location!" )
        return
    elif len(game) == 1:
        cur.execute( "DELETE FROM games WHERE LOWER(location) = %s", (gameLocation,) )
        con.commit()

        print()
        print( "Game successfully deleted!" )
        return

    gameYear = input( "What year did this game take place?: " )
    gameYear = gameYear.strip()

    # check if any games were played in this location in this year
    cur.execute( "SELECT * FROM games WHERE LOWER(location) = %s AND DATE_PART('year', date) = %s", (gameLocation, gameYear,)  )
    game = cur.fetchall()
    if game == []:
        print()
        print( "No games were ever played in this location and in this year!" )
        return
    elif len(game) == 1:
        cur.execute( "DELETE FROM games WHERE LOWER(location) = %s AND DATE_PART('year', date) = %s", (gameLocation, gameYear,)  )
        con.commit()

        print()
        print( "Game successfully deleted!" )
        return

    gameMonth = input( "What month did this game take place?: " )
    gameMonth = gameMonth.strip()

    # check if any games were played in this location in this year and month
    cur.execute( "SELECT * FROM games WHERE LOWER(location) = %s AND DATE_PART('year', date) = %s AND DATE_PART('month', date) = %s", (gameLocation, gameYear, gameMonth,)  )
    game = cur.fetchall()
    if game == []:
        print()
        print( "No games were ever played in this location and in this year and month!" )
        return
    elif len(game) == 1:
        cur.execute( "DELETE FROM games WHERE LOWER(location) = %s AND DATE_PART('year', date) = %s AND DATE_PART('month', date) = %s", (gameLocation, gameYear, gameMonth,)  )
        con.commit()

        print()
        print( "Game successfully deleted!" )
        return

    gameDay = input( "What day did this game take place?: " )
    gameDay = gameDay.strip()

    # check if any games were played in this location in this year and month
    cur.execute( "SELECT * FROM games WHERE LOWER(location) = %s AND DATE_PART('year', date) = %s AND DATE_PART('month', date) = %s AND DATE_PART('day', date) = %s", (gameLocation, gameYear, gameMonth, gameDay,)  )
    game = cur.fetchall()
    if game == []:
        print()
        print( "No games were ever played in this location and in this year and month and day!" )
        return
    elif len(game) == 1:
        cur.execute( "DELETE FROM games WHERE LOWER(location) = %s AND DATE_PART('year', date) = %s AND DATE_PART('month', date) = %s AND DATE_PART('day', date) = %s", (gameLocation, gameYear, gameMonth, gameDay,)  )
        con.commit()

        print()
        print( "Game successfully deleted!" )

def removeManager():
    name = input( "What is the name of the coach you wish to delete?: " )
    name = name.strip()

    # check if team exists in teams table
    cur.execute( "SELECT * FROM managers WHERE name = %s", (name,) )
    manager = cur.fetchone()
    if manager == None:
        print()
        print("This coach does not exist!")
        return

    cur.execute( "DELETE FROM managers WHERE name = %s", (name,) )
    con.commit()

    print()
    print( "Coach successfully deleted!" )

def updatePlayer():
    # asks for which player to update
    playerName = input("Enter the name of the player you would like to update: ")
    playerName = playerName.strip()
    cur.execute("SELECT * FROM players WHERE name = %s",(playerName,))
    player = cur.fetchone()
    if player == None:
        print()
        print("This player does not exist!")
        return
    
    #asks for which attribute of that player to update
    playerAttribute = input("Which attribute of your selected player would you like to update?: ")
    playerAttribute = playerAttribute.strip()
    playerAttribute = playerAttribute.lower()
    if playerAttribute != "name" and playerAttribute != "pace" and playerAttribute != "shooting" and playerAttribute != "passing" and playerAttribute != "dribbling" and playerAttribute != "defending" and playerAttribute != "physicality" and playerAttribute != "overall":
        print()
        print("This is not an attribute of a player!")
        return
    
    newAttributeValue = input("What is the new value of this attribute?: ")
    newAttributeValue = newAttributeValue.strip()

    # uses single quotes around newAttributeValue for name only because it is a string, all other attributes are integers
    if playerAttribute == "name":
        cur.execute("UPDATE players SET {} = '{}' WHERE name = '{}'".format(playerAttribute, newAttributeValue, playerName,) )
    else:
        cur.execute("UPDATE players SET {} = {} WHERE name = '{}'".format(playerAttribute, newAttributeValue, playerName,) )

    con.commit()

    print()
    print( "Player successfully updated!" )

def updateTeam():
    #asks for which team to update
    teamName = input("Enter the name of the team you would like to update: ")
    teamName = teamName.strip()
    cur.execute("SELECT * FROM teams WHERE name = %s", (teamName,) )
    team = cur.fetchone()
    if team == None:
        print()
        print("This team does not exist!")
        return
    
    #asks for which attribute of that team to update
    teamAttribute = input("Which attribute of your selected team would you like to update?: ")
    teamAttribute = teamAttribute.strip()
    teamAttribute = teamAttribute.lower()
    if teamAttribute != "name" and teamAttribute != "league" and teamAttribute != "atkrating"  and teamAttribute != "mdrating" and teamAttribute != "dfrating" and teamAttribute != "overall":
        print()
        print( "This is not an attribute of a team!" )
        return
    
    newAttributeValue = input("What is the new value of this attribute?: ")
    newAttributeValue = newAttributeValue.strip()

    if teamAttribute == "name":
        cur.execute("UPDATE teams SET {} = '{}' WHERE name = '{}'".format(teamAttribute, newAttributeValue, teamName,) )
    else:
        cur.execute("UPDATE teams SET {} = {} WHERE name = '{}'".format(teamAttribute, newAttributeValue, teamName,) )

    con.commit()

    print()
    print( "Player successfully updated!" )

def updateGame():
    #asks for which game to update
    gameLocation = input("Enter the location of the game you would like to update: ")
    gameLocation = gameLocation.strip()
    gameLocation = gameLocation.lower()
    
    # check if any games were played in this location
    cur.execute("SELECT * FROM games WHERE LOWER(location) = %s", (gameLocation,) )
    game = cur.fetchall()
    if game == []:
        print()
        print("No games were ever played in this location!")
        return
    elif len(game) == 1:
        #asks for which attribute of that game to update
        gameAttribute = input("Which attribute of your selected game would you like to update?: ")
        gameAttribute = gameAttribute.strip()
        gameAttribute = gameAttribute.lower()
        if gameAttribute != "date" and gameAttribute != "location" and gameAttribute != "leftteamscore"  and gameAttribute != "rightteamscore":
            print()
            print( "This is not an attribute of a game!" )
            return
        
        newAttributeValue = input("What is the new value of this attribute?: ")
        newAttributeValue = newAttributeValue.strip()

        if gameAttribute == "date" or gameAttribute == "location":
            cur.execute("UPDATE games SET {} = '{}' WHERE LOWER(location) = '{}'".format(gameAttribute, newAttributeValue, gameLocation,) )
        else:
            cur.execute("UPDATE games SET {} = {} WHERE LOWER(location) = '{}'".format(gameAttribute, newAttributeValue, gameLocation,) )

        con.commit()

        print()
        print( "Game successfully updated!" )
        return

    gameYear = input( "What year did this game take place?: " )
    gameYear = gameYear.strip()

    # check if any games were played in this location in this year
    cur.execute( "SELECT * FROM games WHERE LOWER(location) = %s AND DATE_PART('year', date) = %s", (gameLocation, gameYear,)  )
    game = cur.fetchall()
    if game == []:
        print()
        print( "No games were ever played in this location and in this year!" )
        return
    elif len(game) == 1:
        #asks for which attribute of that game to update
        gameAttribute = input("Which attribute of your selected game would you like to update?: ")
        gameAttribute = gameAttribute.strip()
        gameAttribute = gameAttribute.lower()
        if gameAttribute != "date" and gameAttribute != "location" and gameAttribute != "leftteamscore"  and gameAttribute != "rightteamscore":
            print()
            print( "This is not an attribute of a game!" )
            return
        
        newAttributeValue = input("What is the new value of this attribute?: ")
        newAttributeValue = newAttributeValue.strip()

        if gameAttribute == "date" or gameAttribute == "location":
            cur.execute("UPDATE games SET {} = '{}' WHERE LOWER(location) = '{}' AND DATE_PART('year', date) = {}".format(gameAttribute, newAttributeValue, gameLocation, gameYear,) )
        else:
            cur.execute("UPDATE games SET {} = {} WHERE LOWER(location) = '{}' AND DATE_PART('year', date) = {}".format(gameAttribute, newAttributeValue, gameLocation, gameYear,) )

        con.commit()

        print()
        print( "Game successfully updated!" )
        return

    gameMonth = input( "What month did this game take place?: " )
    gameMonth = gameMonth.strip()

    # check if any games were played in this location in this year and month
    cur.execute( "SELECT * FROM games WHERE LOWER(location) = %s AND DATE_PART('year', date) = %s AND DATE_PART('month', date) = %s", (gameLocation, gameYear, gameMonth,)  )
    game = cur.fetchall()
    if game == []:
        print()
        print( "No games were ever played in this location and in this year and month!" )
        return
    elif len(game) == 1:
        #asks for which attribute of that game to update
        gameAttribute = input("Which attribute of your selected game would you like to update?: ")
        gameAttribute = gameAttribute.strip()
        gameAttribute = gameAttribute.lower()
        if gameAttribute != "date" and gameAttribute != "location" and gameAttribute != "leftteamscore"  and gameAttribute != "rightteamscore":
            print()
            print( "This is not an attribute of a game!" )
            return
        
        newAttributeValue = input("What is the new value of this attribute?: ")
        newAttributeValue = newAttributeValue.strip()

        if gameAttribute == "date" or gameAttribute == "location":
            cur.execute("UPDATE games SET {} = '{}' WHERE LOWER(location) = '{}' AND DATE_PART('year', date) = {} AND DATE_PART('month', date) = {}".format(gameAttribute, newAttributeValue, gameLocation, gameYear, gameMonth,) )
        else:
            cur.execute("UPDATE games SET {} = {} WHERE LOWER(location) = '{}' AND DATE_PART('year', date) = {} AND DATE_PART('month', date) = {}".format(gameAttribute, newAttributeValue, gameLocation, gameYear, gameMonth,) )

        con.commit()

        print()
        print( "Game successfully updated!" )
        return

    gameDay = input( "What day did this game take place?: " )
    gameDay = gameDay.strip()

    # check if any games were played in this location in this year and month
    cur.execute( "SELECT * FROM games WHERE LOWER(location) = %s AND DATE_PART('year', date) = %s AND DATE_PART('month', date) = %s AND DATE_PART('day', date) = %s", (gameLocation, gameYear, gameMonth, gameDay,)  )
    game = cur.fetchall()
    if game == []:
        print()
        print( "No games were ever played in this location and in this year and month and day!" )
        return
    elif len(game) == 1:
        #asks for which attribute of that game to update
        gameAttribute = input("Which attribute of your selected game would you like to update?: ")
        gameAttribute = gameAttribute.strip()
        gameAttribute = gameAttribute.lower()
        if gameAttribute != "date" and gameAttribute != "location" and gameAttribute != "leftteamscore"  and gameAttribute != "rightteamscore":
            print()
            print( "This is not an attribute of a game!" )
            return
        
        newAttributeValue = input("What is the new value of this attribute?: ")
        newAttributeValue = newAttributeValue.strip()

        if gameAttribute == "date" or gameAttribute == "location":
            cur.execute("UPDATE games SET {} = '{}' WHERE LOWER(location) = '{}' AND DATE_PART('year', date) = {} AND DATE_PART('month', date) = {} AND DATE_PART('day', date)".format(gameAttribute, newAttributeValue, gameLocation, gameYear, gameMonth, gameDay,) )
        else:
            cur.execute("UPDATE games SET {} = {} WHERE LOWER(location) = '{}' AND DATE_PART('year', date) = {} AND DATE_PART('month', date) = {} AND DATE_PART('day', date)".format(gameAttribute, newAttributeValue, gameLocation, gameYear, gameMonth, gameDay,) )
        con.commit()

        print()
        print( "Game successfully updated!" )

# database connection request. change fields according to your local machine's corresponding value
con = psycopg2.connect(
    database="dbproj",
    user="postgres",
    password="password",
    host="localhost",
    port= '5432'
)

cur = con.cursor()

currentUser = []

userType = "notYetLoggedIn"

# postgres super user menu
def postgresSuperUserMenu():
    print("")
    print("Players:")
    print("1. View all players")
    print("2. Display a player's information")
    print("3. Create a player")
    print("4. Update a player")
    print("5. Delete a player")
    print("")
    print("Teams:")
    print("6. View all teams")
    print("7. Display a team's roster")
    print("8. Create a team")
    print("9. Add player to team")
    print("10. Remove player from team")
    print("11. Update a team")
    print("12. Delete a team")
    print("")
    print("Games:")
    print("13. View all games")
    print("14. Create a game")
    print("15: Update a game")
    print("16. Delete a game")
    print("")
    print("Coaches:")
    print("17. View all coaches")
    print("18. Create a coach")
    print("19. Delete a coach")
    print("")
    print("Users:")
    print("20. View all users")
    print("21. Create a user")
    print("22. Login a user")
    print("")
    print("0. Exit")
    
    print("")
    choice = input("Enter your choice: ")

    if choice == "1":
        viewAllPlayers()
    elif choice == "2":
        displayPlayer()
    elif choice == "3":
        insertPlayer()
    elif choice == "4":
        updatePlayer()
    elif choice == "5":
        removePlayer()
    elif choice == "6":
        viewAllTeams()
    elif choice == "7":
        displayTeam()
    elif choice == "8":
        insertTeam()
    elif choice == "9":
        addPlayerToTeam()
    elif choice == "10":
        removePlayerFromTeam()
    elif choice == "11":
        updateTeam()
    elif choice == "12":
        removeTeam()
    elif choice == "13":
        viewAllGames()
    elif choice == "14":
        insertGame()
    elif choice == "15":
        updateGame()
    elif choice == "16":
        removeGame()
    elif choice == "17":
        viewAllManagers()
    elif choice == "18":
        insertManager()
    elif choice == "19":
        removeManager()
    elif choice == "20":
        viewAllUsers()
    elif choice == "21":
        insertUser()
    elif choice == "22":
        loginUser()
    elif choice == "0":
        print("")
        print("Thank you for using FIFAgres! Have a nice day!")
        print("")
        con.close()
        return 0
    else:
        print("")
        print("Invalid input! Please select from one of the inputs below.")

def fanMenu():
    print("")
    print("1. View all players")
    print("2. Display a player's information")
    print("3. View all teams")
    print("4. Display a team's roster")
    print("5. View all coaches")
    print("6. View all games")
    print("")
    print("0. Exit")
    
    print("")
    choice = input("Enter your choice: ")

    if choice == "1":
        viewAllPlayers()
    elif choice == "2":
        displayPlayer()
    elif choice == "3":
        viewAllTeams()
    elif choice == "4":
        displayTeam()
    elif choice == "5":
        viewAllManagers()
    elif choice == "6":
        viewAllGames()
    elif choice == "0":
        print("")
        print("Thank you for using FIFAgres! Have a nice day!")
        print("")
        con.close()
        return 0
    else:
        print("")
        print("Invalid input! Please select from one of the inputs below.")

def clubOwnerMenu():
    print("")
    print("1. View all players")
    print("2. Display a player's information")
    print("3. View all teams")
    print("4. Display a team's roster")
    print("5. View all coaches")
    print("6. View all games")
    print("")
    print("7. Update a player")
    print("8. Add player to team")
    print("9. Remove player from team")
    print("10. Update a team")
    print("11. Create a coach")
    print("12. Delete a coach")
    print("")
    print("0. Exit")
    
    print("")
    choice = input("Enter your choice: ")

    if choice == "1":
        viewAllPlayers()
    elif choice == "2":
        displayPlayer()
    elif choice == "3":
        viewAllTeams()
    elif choice == "4":
        displayTeam()
    elif choice == "5":
        viewAllManagers()
    elif choice == "6":
        viewAllGames()
    elif choice == "7":
        updatePlayer()
    elif choice == "8":
        addPlayerToTeam()
    elif choice == "9":
        removePlayerFromTeam()
    elif choice == "10":
        updateTeam()
    elif choice == "11":
        insertManager()
    elif choice == "12":
        removeManager()
    elif choice == "0":
        print("")
        print("Thank you for using FIFAgres! Have a nice day!")
        print("")
        con.close()
        return 0
    else:
        print("")
        print("Invalid input! Please select from one of the inputs below.")

def gameOrganizerMenu():
    print("")
    print("1. View all players")
    print("2. Display a player's information")
    print("3. View all teams")
    print("4. Display a team's roster")
    print("5. View all coaches")
    print("6. View all games")
    print("")
    print("7. Create a game")
    print("8. Delete a game")
    print("9: Update a game")
    print("")
    print("0. Exit")
    
    print("")
    choice = input("Enter your choice: ")

    if choice == "1":
        viewAllPlayers()
    elif choice == "2":
        displayPlayer()
    elif choice == "3":
        viewAllTeams()
    elif choice == "4":
        displayTeam()
    elif choice == "5":
        viewAllManagers()
    elif choice == "6":
        viewAllGames()
    elif choice == "7":
        insertGame()
    elif choice == "8":
        removeGame()
    elif choice == "9":
        updateGame()
    elif choice == "0":
        print("")
        print("Thank you for using FIFAgres! Have a nice day!")
        print("")
        con.close()
        return 0
    else:
        print("")
        print("Invalid input! Please select from one of the inputs below.")

# actual program
print("")
print("Welcome to FIFAgres! Please log in!")
print("")

while True:
    if userType == "notYetLoggedIn":
        userType = loginUser()
        continue

    ret = 1

    if userType == "postgressuperuser":
        print("")
        print("Welcome back to FIFAgres! As a postgres superuser, what would you like to do?")
        while True:
            ret = postgresSuperUserMenu()
            if ret == 0:
                break
    elif userType == "fan":
        print("")
        print("Welcome back to FIFAgres! As a fan, what would you like to do?")
        while True:
            ret = fanMenu()
            if ret == 0:
                break
    elif userType == "clubowner":
        print("")
        print("Welcome back to FIFAgres! As a team organizer, what would you like to do?")
        while True:
            ret = clubOwnerMenu()
            if ret == 0:
                break
    elif userType == "gameorganizer":
        print("")
        print("Welcome back to FIFAgres! As a game organizer, what would you like to do?")
        while True:
            ret = gameOrganizerMenu()
            if ret == 0:
                break
    else:
        print()
        print( "Login failed! Please try again!" )
        print()
        userType = "notYetLoggedIn"

    if ret == 0:
        break