from Entry import *
from configurator import *
import re
import String,Date,FiscalCode


conf = configure("config.json")

class Table():
    def __init__(self):
        self.header = []
        self.entries = []
        self.data_types = {}
        self.file_name = conf.file.source
        self.mode = conf.mode

        self.__load_file_data()

    def __load_file_data(self):
        header = []
        rows = []
        try:
            with open(self.file_name,"r") as file:
                h = True
                for line in file:
                    line = line.replace("\n","")
                    line = line.split(conf.file.separator)
                    if h:
                        header.append(line)
                        h = False
                    else:
                        rows.append(line)



        except Exception as e:
            print(e)

        if(header != [] and rows != []):
            header = self.__filter_header(header,rows)[0]
            rows = self.__filter_header(header,rows)[1]
        else:
            raise Exception("Failed to load data!")

        self.header = header
        self.__auto_data_types(header,rows)


    def __filter_header(self,header,rows):
        filtered_header = []
        filtered_rows = []
        filtered_rows_position = []

        for i in range(len(header)):
            if header[i] in conf.fields_list:
                filtered_header.append(header[i])
                filtered_rows_position.append(i)
        
        for row in rows:
            new_row = []
            for i in range(len(row)):
                if(i in filtered_rows_position):
                    new_row.append(row[i])

        return (filtered_header,filtered_rows)


    def __auto_data_types(self,header,rows):
        """Set data types based on configuration file"""
        sample_row = rows[0]
        for i in range(len(header)):
            for type in conf.gbl.data_types:
                pattern = re.compile(getattr(conf.gbl,type).structure)
                if pattern.match(sample_row[i]):
                    self.data_types[header[i]] = globals()[type]
                    break


    def __create_entries(self,header,rows):
        entries = []
        for row in rows:
            original_value = {}
            for i in range(len(header)):
                original_value[header[i]] = row[i] 

            entry = Entry()
            setattr(entry,"ORIGINAL",original_value)
            for i in range(len(header)):
                object = self.data_types[header[i]](row[i])
                setattr(entry,header[i],object)
            entries.append(entry)
        
        self.entries = entries


        
    def anonymize(self):
        for entry in self.entries:
            entry.anonymize()