import re
from configurator import *

conf = configure("config.json")

class Entry(object):

    def anonymize(self):
        req = []
        for field in list(self.__dict__.keys()):
            if hasattr(conf.fields,field):
                if hasattr(getattr(conf.fields,field),"req"):
                    req = getattr(conf.fields,field).req
                    req = self.__parse_ref(req)

            field.anonymize(req)
        
    def __parse_ref(self,ref):
        new_ref = {}
        for r in ref:
            r = r.replace("$","")
            new_ref[r] = getattr(self,r)


        return new_ref
