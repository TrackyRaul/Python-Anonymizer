


if __name__ == "__main__":
    '''
    prova = ["a","b","c"]
    e = Entry(prova)
    e.insert_entry_data(["a","b","c"])
    '''
    nome = String("Samuele", "nomi.csv")
    cognome = String("Pozzani", "cognomi.csv")
    data = Date()
    sex = "male"
    code = FiscalCode(cognome, nome, data, sex)
    print(code.fiscal_code)
    print(cognome.name)
    print(nome.name)
    