class User:
    def __init__(self, name, surname, login, password, role="user"):
        self.name = name
        self.surname = surname
        self.login = login
        self.password = password
        self.role = role
        self._authorized = False

    def whois(self):
        print("Login: {}\nName: {}\nSurname: {}\nRole: {}".format(self.login, self.name, self.surname, self.role))

    def set_role(self, newRole):
        self.role = newRole

    def set_auth(self):
        self._authorized = True

    def get_auth(self):
        return self._authorized

    authorization = property(set_auth, get_auth)