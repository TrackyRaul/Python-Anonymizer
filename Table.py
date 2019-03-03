import configurator
from modules import Mail, Date, FiscalCode, String
conf = configurator.configure("config.json")


class Table():
    def __init__(self):
        """Attributes"""
        self.entries = []
        self.header = []
        self.file_info = conf.file
        self.glb_info = conf.gbl
        """Load data from file"""
        self.header = self.__load_file()[0]
        self.rows = self.__load_file()[1]

        """Filter header and rows based on header specified in configuration file"""
        self.header = self.__filter_info(self.header, self.rows)[0]
        self.rows = self.__filter_info(self.header, self.rows)[1]

        # print(self.header,self.rows)

    def __load_file(self):
        """Load data from files"""
        rows = []
        header = []
        try:
            with open(self.file_info.source, "r") as file:
                h = True
                for line in file:
                    line = line.replace("\n", "")
                    line = line.split(self.file_info.separator)
                    if h:
                        header = line
                        h = False
                    else:
                        rows.append(line)
        except Exception as ex:
            print(ex)

        return (rows, header)

    def __filter_info(self, header, rows):
        """Filter header and rows based on configuration file"""
        ref_header = conf.fields_list
        new_header_indexes = []
        new_header = []
        new_rows = []
        for i in range(len(header)):
            if header[i] in ref_header:
                new_header_indexes.append(i)
                new_header.append(header[i])

        for row in rows:
            new_row = []
            for i in range(len(row)):
                if(i in new_header_indexes):
                    new_row.append(row[i])

            new_rows.append(new_row)

        return(new_header, new_rows)
