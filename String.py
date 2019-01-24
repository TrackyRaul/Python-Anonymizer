from random import choice


class String():
    def __init__(self,name,filename):
        self.filename = filename
        self.replacements = []
        self.name = name

        self.__load_data_from_file()


    def __load_data_from_file(self):
        try:
            with open(self.filename,"r") as file:
                for line in file:
                    line = line.replace("\n","")
                    self.replacements.append(line)
        except Exception as ex:
            print(ex)


    def replace(self):
        replacement = choice(self.replacements)

        if(self.name != replacement):
            self.name = replacement
        else:
            replace()
        