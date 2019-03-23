from config import configurator
import re


conf = configurator.configure("./config/config.json")

class Mail():
    def __init__(self,field_name,original_value):
        self.field_name = field_name
        self.value = original_value
        self.original_value = original_value
        self.original_elements = {}

        #Original mail elements
        self.original_elements["domain"] = self.original_value.split("@")[1]
        self.original_elements["name"] = self.original_value.split("@")[0]
    
    def anonymize(self,requirements):
        """Anonymize fiscal code"""
        req = requirements
        structure = getattr(conf.fields,self.field_name).structure

        #Check if a domain configuration is present and consider it if the original value is not specified
        if(hasattr(getattr(conf.fields,self.field_name),"domain") and "$ORIGINAL"not in structure):
            self.original_elements["domain"] = getattr(conf.fields,self.field_name).domain


        #Check if configuration is available in the config
        if hasattr(conf.fields,self.field_name):
            for elem in list(req.keys()):
                #Consider each element in the keys list
                if("$ORIGINAL" not in elem):
                    #Change the parts that don't use the orignal value
                    temp_str = req[elem].value
                    structure = structure.replace(elem,temp_str.lower())
                elif("domain" in structure):
                    #Check if keyword domain is present
                    structure = structure.replace("domain",self.original_elements["domain"])
                else:
                    structure = structure.replace(elem,self.original_elements["domain"])
        else:
            raise Exception("Specific configuration needed for this class(mail) to work.")
        
        self.value = structure