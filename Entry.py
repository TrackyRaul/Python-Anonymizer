import re

class Entry(object):
    def __init__(self, column_names):
        for name in column_names:
            if(name not in self.__dict__.keys()):
                setattr(self,name,None)
            else:
                raise Exception(f"{name} is a duplicate! An entry can't have two attributes with the same name.")


    def insert_entry_data(self,row_value):

        attributes_names = list(self.__dict__.keys())
        if(len(row_value) != len(attributes_names)):
            raise Exception("The number of elements given doesn't coincide with the number of attributes in the Entry object!")
        for i in range(len(attributes_names)):
            setattr(self,attributes_names[i],row_value[i])
    

    def __objectify(self,value):
        
        '''
        return_value = None
        mail_pattern = re.compile("^([a-zA-Z0-9_\-\.]+)@([a-zA-Z]+).([a-zA-Z]+)$")
        fiscal_code_pattern = re.compile("^([A-Z]){6}[0-9]{2}[A-Z]{1}[0-9]{2}[A-Z]{1}[0-9]{3}[A-Z]{1}$")
        date_pattern = re.compile("^[0-9]{2}/[0-9]{2}/[0-9]{4}$")
        string_pattern = re.compile("^[a-zA-Z]+$")
        '''
        