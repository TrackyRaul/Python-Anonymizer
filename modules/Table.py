import re
import sys
from config import configurator
from modules.Entry import *
from modules.String import *
from modules.Date import *
from modules.FiscalCode import *
from modules.Mail import *


conf = configurator.configure("./config/config.json")


class Table():

    def __init__(self, infname, outfname, separator=","):
        """Attributes"""
        self.entries = []
        self.header = []
        self.column_types = {}
        self.in_file_name = infname
        self.out_file_name = outfname
        self.file_separator = separator
        self.glb_info = conf.gbl


    def start(self):
        # Load data from file
        self.header = self.__load_file()[0]
        self.rows = self.__load_file()[1]
        # Filter header and rows based on header specified in configuration file
        filtered_info = self.__filter_info(self.header, self.rows)
        self.header = filtered_info[0]
        self.rows = filtered_info[1]

        # Set header column types
        self.column_types = self.__get_column_types(self.header, self.rows)

        # Generate entries objects
        self.entries = self.__create_entries(
            self.header, self.rows, self.column_types)

        self.__anonymize()

        #Write to file
        temp_rows = [x.print(self.file_separator) for x in self.entries]
        self.__write_to_file(",".join(self.header),
                             temp_rows, self.out_file_name)


    def __load_file(self):
        """Load data from files"""
        rows = []
        header = []
        try:
            with open(self.in_file_name, "r") as file:
                h = True
                for line in file:
                    line = line.replace("\n", "")
                    line = line.split(self.file_separator)
                    if h:
                        header = line
                        h = False
                    else:
                        rows.append(line)
        except Exception as ex:
            print(ex)
        return (header, rows)


    def __write_to_file(self, header, rows, filename):
        """Write data to file"""
        try:
            with open(filename, "w") as file:
                content = header + "\n"
                for row in rows:
                    content += row + "\n"

                file.write(content)
        except Exception as ex:
            print(ex)


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


    def __get_column_types(self, header, rows):
        """Read from configuration the types or calculate them based on regex"""
        types = {}
        for i in range(len(header)):
            typed = False
            if self.__exist_column_conf(header[i]):
                # Check if field has type attribute
                if hasattr(getattr(conf.fields, header[i]), type):
                    # Create a class reference based on stated type in configuration file
                    types[header[i]] = globals()[getattr(
                        conf.fields, header[i]).type]
                    typed = True

            if not typed:
                # Give type based on regex in conf file
                types[header[i]] = self.__get_type_from_regex(
                    header[i], rows[0][i])

        # Check if the difference between the keys of types dict and header is an empty list
        if len([x for x in list(types.keys()) if x in header]) == 0:
            # If the difference is not empty some columns don't have a type
            raise Exception("Not all columns have type declared properly!")

        return types


    def __exist_column_conf(self, column):
        """Check if field has costum configuration"""
        return_value = False
        if hasattr(conf.fields, column):
            return_value = True


    def __get_type_from_regex(self, column, sample_row_value):
        """Given a string get the type of the string based on regex"""
        return_type = None
        for type in conf.gbl.data_types:
            # Get pattern from configuration file
            pattern = re.compile(getattr(conf.gbl, type).structure)
            if pattern.match(sample_row_value):
                # Check for all available types if one matches
                return_type = globals()[type]
                break
        if return_type == None:
            # Check if the type was not given
            raise Exception(f"Type could not be found for {column}")
        return return_type


    def __create_entries(self, header, rows, types):
        entries = []
        # Consider each row
        for row in rows:
            # Save the original content
            temp_entry = Entry()
            for i in range(len(header)):
                # Create an instance of class defined of type defined in the types dict
                # As a parameter set the original value of the cell
                setattr(temp_entry, header[i],
                        types[header[i]](header[i], row[i]))

            entries.append(temp_entry)
        return entries

    
    def progress(self, count, total, suffix=''):
        bar_len = 60
        filled_len = int(round(bar_len * count / float(total)))
        percents = round(100.0 * count / float(total), 1)
        bar = '=' * filled_len + '>' + '-' * (bar_len - filled_len)
        sys.stdout.write('[%s] %s%s%s\r' % (bar, percents, '%', suffix))
        sys.stdout.flush()


    def __anonymize(self):
        """Anonymize each entry"""
        progress_counter = 0
        for entry in self.entries:
            entry.anonymize()
            progress_counter += 1
            # print progress bar
            self.progress(progress_counter, len(self.entries), str("   " + str(progress_counter) + "/" + str(len(self.entries))))
        print()
