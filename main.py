import psycopg2

con = psycopg2.connect(
database="dbproj",
user="postgres",
password="adekunmi",
host="localhost",
port= '5432'
)

cursor = con.cursor()
cursor.execute("SELECT * FROM players")
res = cursor.fetchall()
print(res)

while True:
    print("\n\nMenu:")
    print("1. Create a player")
    print("2. Create a team")
    print("3. Create a game")
    print("4. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        print("slay")
    elif choice == "4":
        break
    else:
        print("Invalid input")
        continue
    