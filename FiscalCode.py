class FiscalCode():

    def __init__(self, surname, name, date, sex):
        self.fiscal_code = ""
        self.surname = surname.upper()
        self.name = name.upper()
        self.date = date
        self.sex = sex.upper()
        self.__generate_code()


    def __generate_code(self):

        vouels = ["A", "E", "I", "O", "U"]
        coding = self.surname
        # Generate first 6 letters of surname and name 
        for i in range(2):
            for letter in coding:
                if len(self.fiscal_code) == 3 * (i+1):
                    break
                elif not letter in vouels:
                    self.fiscal_code += letter
            for letter in coding:
                if len(self.fiscal_code) == 3 * (i+1):
                    break
                elif letter in vouels:
                    self.fiscal_code += letter
            while len(self.fiscal_code) < 3 * (i+1):
                self.fiscal_code += "X"
            coding = self.name

        # Add last 2 digits of year
        self.fiscal_code += str(self.date.get_year())[-2:]

        # Associate month and letter
        months = ["A", "B", "C", "D", "E", "H", "L", "M", "P", "R", "S", "T"]
        self.fiscal_code += months[self.date.get_month() - 1]

        # Add day, plus 40 if female
        if self.sex == "FEMALE":
            self.fiscal_code += str(self.date.get_day() + 40)
        elif self.date.get_day() < 10:
            self.fiscal_code += "0" + str(self.date.get_day())
        else:
            self.fiscal_code += str(self.date.get_day())

        # Add some other characters to rappresent 
        self.fiscal_code += "X"
        for i in range(3):
            self.fiscal_code += str(i)
        self.fiscal_code += "X"


    def get_code(self):
        return self.fiscal_code
