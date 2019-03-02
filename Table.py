from Entry import *
from configurator import *

conf = configure("config.json")

class Table():
    def __init__(self):
        self.header = []
        self.raw_rows = []
        self.entries = []

    def load_csv_table(self,filename):
        try:
            with open(filename,"r") as file:
                header = True
                for line in file:
                    line = line.replace("\n","")
                    line = line.split(",")
                    if (header == True):
                        self.header.extend(line)
                        header = False
                    else:
                        self.raw_rows.append(line)
        except Exception as ex:
            print(ex)
        
    def create_entries(self):
        if (len(self.header) != 0 and len(self.raw_rows) != 0):
            for row in self.raw_rows:
                entry = Entry(self.header)
                print(entry.__dict__)
                entry.insert_entry_data(row)
                self.entries.append(entry)
            
        
        
        else:
            raise Exception("Raw data not loaded")
        