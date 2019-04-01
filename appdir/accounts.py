from appdir.models import Patron, BankAccountType, BankAccount, PatronBankAccounts



def getPatronAccounts(user):

    patronsAccounts=PatronBankAccounts.query.filter_by(id_patron=user).all()
    namedAccounts = []

    for account in patronsAccounts:
        acc = BankAccount.query.filter_by(id=account.id_bankAccount).all()
        namedAccounts.append(acc)

    return namedAccounts
