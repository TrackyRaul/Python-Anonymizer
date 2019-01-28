from random import choice


class String():
    def __init__(self, name, filename):
        self.filename = filename
        self.replacements = []
        self.name = name

        self.__load_data_from_file()
        self.__replace()


    def __load_data_from_file(self):
        try:
            with open(self.filename,"r",encoding="UTF-8") as file:
                for line in file.readlines():
                    line = line.split(",")
                    self.replacements.extend(line)
        except Exception as ex:
            print(ex)


    def __replace(self):
        replacement = choice(self.replacements)

        if self.name != replacement:
            self.name = replacement
        else:
            __replace()
    
    
    def get_name(self):
        return self.name