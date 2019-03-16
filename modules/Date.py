import configurator
import re
import random
conf = configurator.configure("config.json")


class Date():
    def __init__(self, field_name, original_value):
        self.field_name = field_name
        self.value = original_value
        self.original_value = original_value
        self.year = 2019
        self.month = 12
        self.day = 10
        self.value = self.original_value
        self.__update_date_value()

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
        pattern = pattern.replace("r", "")
        nvalue = value
        if "+-" in pattern or "-+" in pattern:
            temp_pattern = pattern.replace("+-", "")
            temp_pattern = pattern.replace("-+", "")
            value_interval = re.findall("\((.*?)\)", temp_pattern)
            if len(value_interval) != 1:
                raise Exception("Date random anonymize error!")

            value_interval = [int(x) for x in value_interval[0].split(",")]

            coin_toss = random.choice([0, 1])

            if coin_toss == 1:
                nvalue += random.randint(value_interval[0], value_interval[1])
            else:
                nvalue -= random.randint(value_interval[0], value_interval[1])

        elif "+" in pattern:
            temp_pattern = pattern.replace("+")
            value_interval = re.findall("\((.*?)\)", temp_pattern)
            if len(value_interval) != 1:
                raise Exception("Date random anonymize error!")
            value_interval = value_interval.split(",")

            nvalue += random.randint(value_interval[0], value_interval[1])

        elif "-" in pattern:
            temp_pattern = pattern.replace("-")
            value_interval = re.findall("\((.*?)\)", temp_pattern)
            if len(value_interval) != 1:
                raise Exception("Date random anonymize error!")
            value_interval = value_interval.split(",")

            nvalue -= random.randint(value_interval[0], value_interval[1])
        else:
            raise Exception("No valid pattern found in date anonymization!")

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
        ref_date = requirements[(getattr(conf.fields, self.field_name).req)[0]]
        ref_date = ref_date.split("/")
        if len(ref_date) != 3:
            raise Exception("Date passed in requirements not valid!")
        ref_day = int(ref_date[0])
        ref_month = int(ref_date[0])
        ref_year = int(ref_date[2])

        if "r" in getattr(conf.fields, self.field_name).day:

            self.day = self.random_anonymize(ref_day, getattr(
                conf.fields, self.field_name).day) % 32

        if "r" in getattr(conf.fields, self.field_name).month:

            self.month = self.random_anonymize(ref_month, getattr(
                conf.fields, self.field_name).month) % 13
        if "r" in getattr(conf.fields, self.field_name).year:
            self.day = self.random_anonymize(ref_day, getattr(
                conf.fields, self.field_name).year) % 3000

        self.__update_date_value()