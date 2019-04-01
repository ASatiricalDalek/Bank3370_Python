from appdir.models import Patron, BankAccountType, BankAccount, PatronBankAccounts



def getPatronAccounts(user):

    patronsAccounts=PatronBankAccounts.query.filter_by(id_patron=user).all()
    bankAccounts=[bankID for (patronID, bankID) in patronsAccounts if patronID == user]

    namedAccounts = []

    for account in bankAccounts:
        acc = BankAccount.query.filter_by(id=account).all()
        namedAccounts.append(acc)

    return namedAccounts
