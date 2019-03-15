import configurator
conf = configurator.configure("config.json")

class FiscalCode():
    def __init__(self,field_name,original_value):
        self.field_name = field_name
        self.value = None
        self.original_value = original_value
        self.name = None
        self.surname = None
        self.fiscal_code = None
        self.sex = None
        self.date = None



    def anonymize(self,requirements):
        """Anonymize fiscal code"""
        req = requirements
        
        #Check if configuration is available in the config
        if hasattr(conf.fields,self.field_name):
            self.name = req[getattr(conf.fields,self.field_name).name]
            self.surname = req[getattr(conf.fields,self.field_name).surename]
            self.sex = req[getattr(conf.fields,self.field_name).sex]
            self.date = req[getattr(conf.fields,self.field_name).birthdate]

            if(self.name == None or self.surname == None or self.sex == None or self.date == None):
                raise Exception("Invalid data given to fiscalcode class to process.")
        else:
            raise Exception("Specific configuration needed for this class to work.")



    def __generate_code(self):
            """ Generate fiscal code based on given data"""
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
            self.fiscal_code += str(self.date.year)[-2:]

            # Associate month and letter
            months = ["A", "B", "C", "D", "E", "H", "L", "M", "P", "R", "S", "T"]
            self.fiscal_code += months[self.date.month - 1]

            # Add day, plus 40 if female
            if self.sex == "FEMALE":
                self.fiscal_code += str(self.date.day + 40)
            elif self.date.day < 10:
                self.fiscal_code += "0" + str(self.date.day)
            else:
                self.fiscal_code += str(self.date.day)

            # Add some other characters to rappresent 
            self.fiscal_code += "X"
            for i in range(3):
                self.fiscal_code += str(i)
            self.fiscal_code += "X"


    def get_code(self):
        return self.fiscal_code