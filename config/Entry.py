import re
from config import configurator


conf = configurator.configure("./config/config.json")

class Entry():
    def __init__(self):
        pass


    def anonymize(self):
        """Consider each column and anonymize it"""
        for attr in conf.fields_list:
            requirements = self.__parse_req(attr)
            
            #Anonymize each attribute
            getattr(self,attr).anonymize(requirements)


    def __parse_req(self,attr):
        """Get from configuration file the required variables and values"""
        req = {}
        if hasattr(getattr(conf.fields,attr),"req"):
            
            req_ref = getattr(conf.fields,attr).req

            for i in range(len(req_ref)):
                #Check if the variable referenced is the original content or not
                pattern = re.compile("^\$ORIGINAL.[a-zA-Z]*")

                if(pattern.match(req_ref[i])):
 
                    #Set the value with the original value of the refferenced variable
                    req[req_ref[i]] = getattr(self,req_ref[i].replace("$","").split(".")[1]).original_value
                else:
                    #Set the value with the new value of the refferenced variable
                    req[req_ref[i]] = getattr(self,req_ref[i].replace("$",""))
        return req

    def print(self,separator = ","):
        """Print the entry as a string"""
        values = []
        #Get attributes and add the values to list
        for attr in conf.fields_list:
            values.append(getattr(self,attr).value)
        #Turn to string and print it
        values = separator.join(values)
        print(values)


