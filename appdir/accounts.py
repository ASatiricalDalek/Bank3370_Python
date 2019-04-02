from appdir.models import Patron, BankAccountType, BankAccount, PatronBankAccounts

def getPatronAccounts(user):

    patronsAccounts=PatronBankAccounts.query.filter_by(id_patron=user).all()
    namedAccounts = []
    for account in patronsAccounts:
        acc = BankAccount.query.filter_by(id=account.id_bankAccount).all()
        tempAccount = BankAccount()
        tempAccount.id = acc[0].id
        tempAccount.accountName = acc[0].accountName
        tempAccount.accountBalance = acc[0].accountBalance
        tempAccount.insurance = acc[0].insurance
        tempAccount.accountType = acc[0].accountType
        namedAccounts.append(tempAccount)

    return namedAccounts
