from appdir.models import Patron, BankAccountType, BankAccount, PatronBankAccounts

def getPatronAccounts(user):

    # Query the association table to find what account IDs relate to the given patron ID
    patronsAccounts=PatronBankAccounts.query.filter_by(id_patron=user).all()
    # Empty list that we will load with objects
    namedAccounts = []
    for account in patronsAccounts:
        # Query the DB to get all the accounts from the Bank Account table by their ID, from the association table query
        acc = BankAccount.query.filter_by(id=account.id_bankAccount).all()
        # Create a new object and fill it with data from the acc query (only one result should be returned at a time)
        tempAccount = BankAccount()
        tempAccount.id = acc[0].id
        tempAccount.accountName = acc[0].accountName
        tempAccount.accountBalance = acc[0].accountBalance
        tempAccount.insurance = acc[0].insurance
        tempAccount.accountType = acc[0].accountType
        # add this new object to the end of the list
        namedAccounts.append(tempAccount)

    return namedAccounts
