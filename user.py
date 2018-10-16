class UserInput():

    def __init__(self,email,series):
        self.email=email
        self.series=series

    @property
    def get_Email(self):
        return self.email

    def set_Email(self, email):
        self.email = email

    @property
    def get_Series(self):
        return self.series

    def set_Series(self, series):
        self.series=series

    