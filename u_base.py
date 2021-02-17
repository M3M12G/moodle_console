import db


class UserBase(object):
    """Base class that defines attributes and general methods for all user roles"""
    _file = db.DB("db/users.json")

    def __init__(self, email, first_name, surname, role):
        self._email = email
        self._first_name = first_name
        self._surname = surname
        self._role = role

    @staticmethod
    def get_db():
        return UserBase._file

    def whois(self):
        print("Role: {}\nEmail: {}\nFirst Name: {}\nSurname: {}".format(
            self._role,
            self._email,
            self._first_name,
            self._surname
        ))

    # returns user's email, used as an id
    def get_email(self):
        return self._email
