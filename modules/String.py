import configurator
import random
conf = configurator.configure("config.json")


class String():
    def __init__(self,field_name,original_value):
        self.field_name = field_name
        self.value = None
        self.original_value = original_value
        self.replacement_file_name = getattr(conf.fields,self.field_name).replacement_file


    def anonymize(self,requirements):
        random_value = ""
        values = []
        req = requirements

        with open(self.replacement_file_name,"r") as file:
            for line in file:
                line = line.replace("\n","")
                line = line.split(getattr(conf.fields,self.field_name).separator)
                values.extend(line)
                
        while random_value == self.original_value or random_value == "":
            random_value = random.choice(line)

        self.value = random_value



