class Mail():

    def __init__(self, name, surname, mail):
        self.name = name
        self.surname = surname
        self.domain = self.__get_domain_from_mail(mail)
        self.mail = self.__generate_mail()

    def __get_domain_from_mail(self, mail):
        return mail[mail.rfind('@') + 1 : ]

    def __generate_mail(self):
        #self.new_mail += f"{self.name}.{self.surname}@{self.domain}"
        return "{}.{}@{}".format(self.name, self.surname, self.domain)
    
    def get_mail(self):
        return self.mail
