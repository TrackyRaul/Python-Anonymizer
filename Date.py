from random import randint

class Date():

    def __init__(self):
        self.day = randint(1, 28)
        self.month = randint(1, 12)
        self.year = randint(1970, 2500)
        if self.day < 10:
            self.str_date = f"0{self.day}/"
        else:
            self.str_date = f"{self.day}/"
        if self.month < 10:
            self.str_date += f"0{self.month}/"
        else:
            self.str_date += f"{self.month}/"
        self.str_date += f"{self.year}"
