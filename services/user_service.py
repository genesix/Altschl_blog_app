import csv

fieldnames = ['id', 'firstname', 'lastname', 'username', 'email', 'password']
fieldnames_logged = ['username', 'password']


#function to read users from csv to a list in memory
def read_users():
    users = []
    with open("database/users.csv", mode="r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            users.append(row)
    return users

#function to read logged in users from csv to a list in memory
def read_logged_users():
    users = {}
    with open("database/logged_in.csv", mode="r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            users[row['username']] = row['password']
    return users


# function to write the header in the users.csv file
def write_header():
    with open('database/users.csv', 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames)
        writer.writeheader()

# function to write the header in the logged_in.csv file
def write_logged_in_header():
    with open('database/logged_in.csv', 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames_logged)
        writer.writeheader()

#function to write users to users.csv file
users_dict = {}
def write_user(firstname: str, lastname: str, username: str, email: str, password: str):
    with open('database/users.csv', 'a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames)
        # if file.tell() == 0:
        #     writer.writeheader()
        users_dict[username] = password
        writer.writerow({
            'id': len(users_dict),
            'firstname': firstname.capitalize(),
            'lastname': lastname.capitalize(),
            'username': username.lower(),
            'email': email.lower(),
            'password': password
        })

#function to write logged in users into a csv file - logged_in.csv
def logged_in(username: str, password: str):
    with open('database/logged_in.csv', 'a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames_logged)
        # if file.tell() == 0:
        #     writer.writeheader()
        writer.writerow({
            'username': username,
            'password': password
            })

def logout(username):
    logged_in_users = read_logged_users()
    if username in logged_in_users:
        del logged_in_users[username]
    print(logged_in_users)
    with open('database/logged_in.csv', 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames_logged)
        if file.tell() == 0:
            writer.writeheader()
        for user in logged_in_users:
            writer.writerow(user.items())
    
            
    



