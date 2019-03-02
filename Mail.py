from String import *
import re
from configurator import *
conf = configure("config.json")


class Mail():
    def __init__(self, req):
        self.data = req
        self.structure = ""
        self.mail

    def __set_structure(self):
        if(hasattr(conf.fields,type(self).__name__)):
            if(hasattr(getattr(conf.fields,type(self).__name__),"structure")):
                self.structure = getattr(conf.fields,type(self).__name__).structure
            else:
                raise Exception("Mail class has no strcture defined in config")
        else:
            raise Exception("Mail class not found ins config")

    def __parse_ref(self,ref):
        nref = ref
        pattern = re.compile("^(\$[a-zA-Z]*)")
        m = re.search(pattern,ref)
        
        while m:
            m = re.search(pattern,ref)
            placeholder = ""
            if m:
                found = m.group(1)
                if(found.replace("$","") == "ORIGINAL"):
                    placeholder = self.data[found.replace("$","")].split("@")[-1]
                else:
                    placeholder = self.data[found.replace("$","")]
                nref = nref.replace(found,placeholder)


        self.mail = nref
