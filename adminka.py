import db as database
import user as uclass

class UserAdminka(object):
    """Used for CRUD user class (creating student/teacher)"""

    def __init__(self):
        self._db = database.DB("db/users.json")

    # returns all existing users mapped to User class
    def get_all_users(self):
        users = []
        users_recs = self._db.read_db()
        for user in users_recs:
            if user["role"] == "admin":
                continue
            users.append(uclass.User(**user))
        return users

    def show_users(self):
        users = self.get_all_users()
        for u in users:
            u.whois()
            print("---------")

    def add_new_user(self):
        users = self._db.read_db()
        userToSave = {"login": input("Please, enter user login >")}

        if self.is_user_exists(userToSave["login"]):
            print("User with login - {} is already exists. please type again".format(userToSave["login"]))
            return

        userToSave["password"] = input("Please, type password >")
        userToSave["name"] = input("Please, type name of user >")
        userToSave["surname"] = input("Please, type surname of user >")
        userToSave["role"] = input("Please, type the role of user \nstudent\nteacher\n> ")
        print("Processing details...")
        users.append(userToSave)
        self._db.write_db(users)
        usr = uclass.User(**userToSave)
        print("New user is created {}".format(usr.whois()))

    def delete_user(self):
        login = input("Please, type the login of target user to delete >")
        exists = self.is_user_exists(login)
        if exists:
            users = self._db.read_db()
            for i in range(len(users)):
                if users[i]["login"] == login:
                    users.pop(i)
                    break
            self._db.write_db(users)
            print("User with login {} is deleted".format(login))
        else:
            print("No user exists with login - {}".format(login))

    def update_user_role(self):
        login = input("Please, type the login of target user to update >")
        exists = self.is_user_exists(login)
        if exists:
            newRole = input("Please, type new role\nstudent\nteacher\n>")
            users = self._db.read_db()
            for i in range(len(users)):
                if users[i]["login"] == login:
                    users[i]["role"] = newRole
                    break
            self._db.write_db(users)
            print("User with login {} is updated to - {}".format(login, newRole))
        else:
            print("No user exists with login - {}".format(login))

    def is_user_exists(self, login):
        users = self._db.read_db()
        for i in range(len(users)):
            if users[i]["login"] == login:
                return True
                break
        return False


userCrud = UserAdminka()
# userCrud.add_new_user()
userCrud.show_users()
# userCrud.delete_user()
#userCrud.update_user_role()
#userCrud.show_users()
