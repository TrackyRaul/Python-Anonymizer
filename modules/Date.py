from config import configurator
import re
import random


conf = configurator.configure("./config/config.json")


class Date():
    def __init__(self, field_name, original_value):
        self.field_name = field_name
        self.value = original_value
        self.original_value = original_value
        self.year = None
        self.month = None
        self.day = None
        #self.value = self.original_value
        # self.__update_date_value()

    def __update_date_parts(self):
        """Update single parts of date"""
        self.year = int(self.value.split("/")[2])
        self.month = int(self.value.split("/")[1])
        self.day = int(self.value.split("/")[0])

    def __update_date_value(self):
        """Update value based on parts"""
        day = self.day
        month = self.month
        year = self.year
        # Reformat string

        if day < 10:
            day = "0"+str(day)
        else:
            day = str(day)

        if month < 10:
            month = "0"+str(month)
        else:
            month = str(month)

        self.value = f"{day}/{month}/{year}"

    def random_anonymize(self, value, pattern):
        #Anonymize dates randomly based on a pattern
        pattern = pattern.replace("r", "")
        nvalue = value

        """Consider the case where you eather sum or substract a random number
        to the value of the date"""
        if "+-" in pattern or "-+" in pattern:
            temp_pattern = pattern.replace("+-", "")
            temp_pattern = pattern.replace("-+", "")
            value_interval = re.findall("\((.*?)\)", temp_pattern)
            if len(value_interval) != 1:
                raise Exception("Date random anonymize error!")

            value_interval = [int(x) for x in value_interval[0].split(",")]

            #Decide between sum or subraction
            coin_toss = random.choice([0, 1])

            if coin_toss == 1:
                nvalue += random.randint(value_interval[0], value_interval[1])
            else:
                nvalue -= random.randint(value_interval[0], value_interval[1])

        #Consider the case of the sum
        elif "+" in pattern:
            temp_pattern = pattern.replace("+", "")
            value_interval = re.findall("\((.*?)\)", temp_pattern)
            if len(value_interval) != 1:
                raise Exception("Date random anonymize error!")
            value_interval = value_interval[0].split(",")
            value_interval = [int(x) for x in value_interval]

            nvalue += random.randint(value_interval[0], value_interval[1])

        #Consider the case of the subtraction
        elif "-" in pattern:
            temp_pattern = pattern.replace("-", "")
            value_interval = re.findall("\((.*?)\)", temp_pattern)
            if len(value_interval) != 1:
                raise Exception("Date random anonymize error!")
            value_interval = value_interval[0].split(",")
            value_interval = [int(x) for x in value_interval]

            nvalue -= random.randint(value_interval[0], value_interval[1])

        #Set a random value between range
        else:
            value_interval = re.findall("\((.*?)\)", pattern)[0].split(",")
            value_interval = [int(x) for x in value_interval]
            nvalue = random.randint(value_interval[0], value_interval[1])

        return nvalue

    def check_conf_validity(self):
        """Check if configuration is valid for dates"""
        if hasattr(conf.fields, self.field_name):
            if not hasattr(getattr(conf.fields, self.field_name), "day") and \
                    hasattr(getattr(conf.fields, self.field_name), "month") and \
                    hasattr(getattr(conf.fields, self.field_name), "year"):
                raise Exception(
                    f"No correct configuration found for {self.field_name}")

        else:
            raise Exception("Date type needs specific configuration in types!")

    def anonymize(self, requirements):
        """Anonymize date based on configuration"""
        ref_date = requirements[(getattr(conf.fields, self.field_name).req)[0]]
        ref_date = ref_date.split("/")
        
        #Check if valid
        if len(ref_date) != 3:
            raise Exception("Date passed in requirements not valid!")
        ref_day = int(ref_date[0])
        ref_month = int(ref_date[1])
        ref_year = int(ref_date[2])

        #Check if it should be randomized
        if "r" in getattr(conf.fields, self.field_name).day:

            self.day = self.random_anonymize(ref_day, getattr(
                conf.fields, self.field_name).day)
            
            
        elif getattr(conf.fields, self.field_name).day == "":
            self.day = ref_day

        if self.day > 30:
                self.day %= 30

        if "r" in getattr(conf.fields, self.field_name).month:

            self.month = self.random_anonymize(ref_month, getattr(
                conf.fields, self.field_name).month)

            
        elif getattr(conf.fields, self.field_name).month == "":
            self.month = ref_month

        if self.month > 12:
                self.month %= 12

        if "r" in getattr(conf.fields, self.field_name).year:
            self.year = self.random_anonymize(ref_year, getattr(
                conf.fields, self.field_name).year)
        elif getattr(conf.fields, self.field_name).year == "":
            self.year = ref_year

        self.__update_date_value()
