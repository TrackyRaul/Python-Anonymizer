


class String():
    def __init__(self,name,filename):
        self.filename = filename
        self.replacements = []
        self.name = ""

        self.__load_data_from_file(self.filename)

    def __load_data_from_file(self):
        try:
            with open(self.filename,"r") as file:
                for line in file:
                    line = line.replace("\n","")
                    self.replacements.append(line)
        except Exception as ex:
            print(ex)

    def replace(self):
        pass




class Mail():
    def __init__():
        pass

class Date():
    def __init__():
        pass


def main():
    s = String("test.csv")


if __name__ == "__main__":
    main()