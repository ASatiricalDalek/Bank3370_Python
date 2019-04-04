from flask import render_template, flash, redirect, url_for, request
from appdir import app, db
from appdir.forms import *
from math import floor, pow
from flask_login import current_user, login_user, logout_user, login_required
from appdir.models import *
from werkzeug.urls import url_parse # used to redirect users to the page they were at before they logged in

# routes contains the logic for all of our pages


@app.route('/')
@app.route('/index')
def index():
    x = getPatronAccounts(current_user.get_id())
    return render_template('home.html', title='Home', bankaccounts=x)



@app.route('/login', methods=['GET', 'POST'])
def login():
    # If the current user is logged in, they don't need to see this form; send them home
    # current_user is a var from flask_login that contains the current user
    # check if that user is authenticated (function defined in models.py; comes from Flask_login)
    # Not logged in users will return false to is_authenticated
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    # Only runs if the method is POST, and the form validates
    if form.validate_on_submit():
        # Retrieve the first record from the db w/ email matching the form entry (should be only 1)
        patron = Patron.query.filter_by(patronEmail = form.email.data).first()
        # if the patron doesn't exist, or the password is wrong
        if patron is None or not patron.checkPassword(form.password.data):
            # display message (see base.html)
            flash('Invalid email address of password')
            return redirect(url_for('index'))
        # Flask-login provides this function; keeps the current_user variable set to this user
        login_user(patron, remember=form.remember_me.data)
        # Next page is set when a user tries to enter a authBlocked page, and is redirected to login instead
        nextPage = request.args.get('next')
        if not nextPage or url_parse(nextPage).netloc != '': # This ensures the URL actually exists in the application
            # if there is no next page set (IE the user went right to login) set nextPage to home
            nextPage = url_for('index')
        return redirect(nextPage)
    # Returned if the above is false, IE the method is GET, therefore the form hasn't been submitted
    # Or the form is invalid
    return render_template('login.html', title="Sign In", form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/accounts/<id>', methods=['GET', 'POST'])
@login_required
def accounts(id):
    form = NewAccountType()
    if form.validate_on_submit():
        accountType = form.accountChoice.data
        if accountType == "Checking":
            flash("Checking Account Selected")
            return redirect(url_for('newCheckingAccount', id=current_user.get_id()))
        elif accountType == "Savings":
            flash("Savings Account Selected")
            return redirect(url_for('newSavingsAccount', id=current_user.get_id()))
        elif accountType == "Retirement":
            return redirect(url_for('newRetirementAccount', id=current_user.get_id()))
            flash("Retirement Account Selected")
        else:
            flash(accountType + " Selected")
        return redirect(url_for('accounts', id=current_user.get_id()))
    else:
        thisPatronsAccounts = PatronBankAccounts()

        listOfAccounts = thisPatronsAccounts.query.filter_by(id_patron=current_user.get_id()).all()
        # Using this list of all the account IDs, query the bankAccount table to find all this patron's accounts
    return render_template('accounts.html', form=form)


@app.route('/loans/<id>', methods=['GET', 'POST'])
@login_required
def loans(id):
    form = NewLoansType()
    if form.validate_on_submit():
        loanType = form.loansChoice.data
        if loanType == "Auto Loans":
            flash("Auto Loans Selected")
            return redirect(url_for('newAutoLoan', id=current_user.get_id()))
        elif loanType == "Student Loans":
            flash("Student Loans Selected")
            return redirect(url_for('newStudentLoan', id=current_user.get_id()))
        elif loanType == "Home Loans":
            flash("Home Loans Selected")
            return redirect(url_for('newHomeLoan', id=current_user.get_id()))
        else:
            flash(loanType + " Selected")
        return redirect(url_for('accounts', id=current_user.get_id()))

    return render_template('loans.html', form=form)


@app.route('/accounts/<id>/new_account', methods=['GET', 'POST'])
@login_required
def newCheckingAccount(id):
    form = CreateCheckingAccountForm()
    if form.validate_on_submit():
        newAccount = BankAccount()
        newAccountRelation = PatronBankAccounts()

        newAccount.accountType = "Checking"
        newAccount.accountBalance = 0
        newAccount.accountName = form.accountName.data
        if (form.insurance.data):
            newAccount.insurance = 1
        else:
            newAccount.insurance = 0

        # Provisionally adds this account to the DB so it gets a unique ID
        db.session.add(newAccount)
        db.session.flush()

        # Use that unique ID, and the current user's sessions ID to create the relationship
        newAccountRelation.id_bankAccount = newAccount.id
        newAccountRelation.id_patron = current_user.get_id()

        db.session.add(newAccountRelation)
        db.session.commit()

        flash("Checking account successfully created!")
        return redirect(url_for('accounts', id=current_user.get_id()))

    return render_template('newCheckingAccount.html', title='Open a Checking Account', form=form)


@app.route('/loans/<id>/newAutoLoan', methods=['GET', 'POST'])
@login_required
def newAutoLoan(id):
    form = CreateAutoLoanForm()
    if form.validate_on_submit():
        newAutoLoan = Loan()
        newLoanRelation = PatronLoanAccounts()

        newAutoLoan.loanCategory = "Student"
        newAutoLoan.loanBalance = 0
        newAutoLoan.loanPayment = 0
        newAutoLoan.startDate = "04/03/2019"
        newAutoLoan.endDate = "Never"

        # Provisionally adds this account to the DB so it gets a unique ID
        db.session.add(newAutoLoan)
        db.session.flush()
        id = current_user.get_id()
        # Use that unique ID, and the current user's sessions ID to create the relationship
        newLoanRelation.id_loan = newAutoLoan.id
        newLoanRelation.id_patron = id

        db.session.add(newLoanRelation)
        db.session.commit()

        flash("Auto loan successfully requested!")
        return redirect(url_for('accounts', id=current_user.get_id()))
    flash(id)
    return render_template('newAutoLoan.html', title='Open a Auto Loan', form=form)


@app.route('/loans/<id>/newStudentLoan', methods=['GET', 'POST'])
@login_required
def newStudentLoan(id):
    form = CreateStudentLoanForm()
    if form.validate_on_submit():
        newStudentLoan = Loan()
        newLoanRelation = PatronLoanAccounts()

        newStudentLoan.loanCategory = "Student"
        newStudentLoan.loanBalance = 0
        newStudentLoan.loanPayment = 0
        newStudentLoan.startDate = "04/03/2019"
        newStudentLoan.endDate = "Never"

        # Provisionally adds this account to the DB so it gets a unique ID
        db.session.add(newStudentLoan)
        db.session.flush()
        id = current_user.get_id()
        # Use that unique ID, and the current user's sessions ID to create the relationship
        newLoanRelation.id_loan = newStudentLoan.id
        newLoanRelation.id_patron = id

        db.session.add(newLoanRelation)
        db.session.commit()

        flash("Student loan successfully requested!")
        return redirect(url_for('loans', id=current_user.get_id()))
    flash(id)
    return render_template('newStudentLoan.html', title='Open a Student Loan', form=form)


@app.route('/loans/<id>/newHomeLoan', methods=['GET', 'POST'])
@login_required
def newHomeLoan(id):
    form = CreateHomeLoanForm()
    if form.validate_on_submit():
        newHomeLoan = LoanType()
        newLoanRelation = PatronLoanAccounts()

        newHomeLoan.loanCategory = "Home"
        newHomeLoan.loanBalance = 0
        newHomeLoan.loanPayment = 0
        newHomeLoan.startDate = "04/03/2019"
        newHomeLoan.endDate = "Never"

        # Provisionally adds this account to the DB so it gets a unique ID
        db.session.add(newHomeLoan)
        db.session.flush()
        id = current_user.get_id()

        # Use that unique ID, and the current user's sessions ID to create the relationship
        newLoanRelation.id_loan = newHomeLoan.id
        newLoanRelation.id_patron = id

        db.session.add(newLoanRelation)
        db.session.commit()

        flash("Home loan successfully requested!")
        return redirect(url_for('loans', id=current_user.get_id()))
    flash(id)
    return render_template('newHomeLoan.html', title='Open a Home Loan', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        patron = Patron()
        patron.patronFirstName = form.firstName.data
        patron.patronLastName = form.lastName.data
        patron.patronEmail = form.email.data
        patron.setPassword(form.password.data)
        db.session.add(patron)
        db.session.commit()
        flash("Congratulations " + form.firstName.data + " you are now a registered user")
        return redirect(url_for('login'))
    return(render_template('register.html', title='Register', form=form))

@app.route('/accounts/<id>/deposit', methods=['GET', 'POST'])
@login_required
def dep(id):

    form = MakeDeposit()
    x = getPatronAccounts(current_user.get_id())
    # this will be a list of tuples to be used as a data source for our account listing
    newList = []
    for account in x:
        # data source expects a value and display member, so pass ID and account name of the object
        newList.append((account.accountName, account.accountName))
    form.accountChoice.choices = newList

    if form.validate_on_submit():
        value = form.accountChoice.data
        accountToDep = BankAccount.query.filter_by(accountName= value).first()
        depAmount = form.amount.data
        depAmount= (floor(depAmount*100)/100)  # drops decimal places after hundredths without rounding
        if depAmount<=0:
            flash("Please enter positive numerical amounts only.")
            return render_template('deposit.html', title='Deposit', form=form)
        else:
            accountToDep.accountBalance += depAmount
            db.session.commit()
            flash("Deposit of $" + str(depAmount) + " to " + value + " was successful!")
            return redirect(url_for('index'))
    else:
        return render_template('deposit.html', title='Deposit', form=form)

    # value = dict(form.accountChoice.choices).get(form.accountChoice.data)

    # value = dict(form.accountChoice.choices).get(form.accountChoice.data)
    # valueCheck= BankAccount.query.filter_by(accountName= 'Robs Checking').first()
    # valueCheck.accountBalance +=200
    # value=valueCheck.accountBalance
    # db.session.commit()


@app.route('/accounts/<id>/transfer', methods=['GET', 'POST'])
@login_required
def tran(id):
    form = MakeTransfer()
    x = getPatronAccounts(current_user.get_id())
    # this will be a list of tuples to be used as a data source for our account listing
    newList = []
    for account in x:
        # data source expects a value and display member, so pass ID and account name of the object
        newList.append((account.accountName, account.accountName))
    form.originaccount.choices = newList
    form.destaccount.choices = newList

    # user attempts to perform a transfer
    if form.validate_on_submit():
        oacc = form.originaccount.data
        dacc = form.destaccount.data
        fromacc = BankAccount.query.filter_by(accountName=oacc).first()
        toacc = BankAccount.query.filter_by(accountName=dacc).first()

        tamt = form.tamount.data
        tamt = (floor(tamt*100)/100)  # drops decimal places after hundredths without rounding

        # If users origin account has insufficient funds, the transfer will fail
        if fromacc.accountBalance<tamt:
            flash("Insufficient funds in "+oacc+" to complete transfer. Please try again.")
            return render_template('transfer.html', title='Transfer', form=form)
        # if user tries to transfer to and from the same account, transfer will will
        elif fromacc == toacc:
            flash("Please select unique origin and destination accounts.")
            return render_template('transfer.html', title='Transfer', form=form)
        elif tamt<=0:
            flash("Please enter positive numerical amounts only.")
            return render_template('transfer.html', title='Transfer', form=form)
        # user has entered valid parameters
        else:
            fromacc.accountBalance -= tamt
            toacc.accountBalance += tamt

            db.session.commit()
            flash("Transfer from "+oacc+" to "+dacc+" of $"+str(tamt)+" was successful!")
            return redirect(url_for('index'))
    # user is load form for the first time
    else:
        return render_template('transfer.html', title='Transfer', form=form)


@app.route('/creditScore', methods=['GET', 'POST'])
def creditScore():
    form = CreditScoreForm()
    if form.validate_on_submit():
        averageAge = form.averageAge.data
        hardInquiries = form.hardInquiries.data
        creditUtilization = form.creditUtilization.data
        latePay = form.latePay.data
        totalAccounts = form.totalAccounts.data
        derogatoryMarks = form.derogatoryMarks.data

        if (averageAge < 0 or hardInquiries < 0 or creditUtilization < 0 or latePay < 0 or totalAccounts <0 or derogatoryMarks <0):
            flash("Please enter positive numeric values")
            return render_template('creditScore.html', title='Credit Score', form=form)

        if (derogatoryMarks < 1 and totalAccounts > 8 and hardInquiries < 3 and latePay < 1 and creditUtilization < 10 and
                    averageAge>24):
            creditScore=800
        else:
            creditScore=600
        flash("Congratulations your Credit Score is " + str(creditScore))
        return render_template('creditScore.html', title='Credit Score', form=form, creditScore=creditScore)
    return render_template('creditScore.html', title='Credit Score', form=form)


@app.route('/estimateInterest/<id>', methods=['GET', 'POST'])
@login_required
def estimateInterest(id):
    form = EstimateInterestForm()
    if form.validate_on_submit():
        account = form.accountType.data
        startingfunds = form.startingFunds.data
        months = form.monthsOfInterest.data
        accountinfo = BankAccountType.query.filter_by(accountType=account).first()
        interestrate = accountinfo.accountInterestRate
        if(startingfunds<0 or months<0):
            flash("Please enter positive numeric values")
            return render_template('estimateInterest.html', title='Estimate Interest', form=form)
        else:
            powermath = pow((1+interestrate), months)
            estimateinterest = startingfunds*powermath
            flash("Congratulations your Estimated Interest return is $" + str(round(estimateinterest,2)))
            return render_template('estimateInterest.html', title='Estimate Interest', form=form, estimateinterest=estimateinterest)
    return render_template('estimateInterest.html', title='Estimate Interest', form=form)


@app.route('/accounts/<id>/new_Savings_account', methods=['GET', 'POST'])
@login_required
def newSavingsAccount(id):
    form = CreateSavingsAccountForm()
    if form.validate_on_submit():
        newAccount = BankAccount()
        newAccountRelation = PatronBankAccounts()

        newAccount.accountType = "Savings"
        newAccount.accountBalance = 0
        newAccount.accountName = form.accountName.data
        if (form.insurance.data):
            newAccount.insurance = 1
        else:
            newAccount.insurance = 0

        # Provisionally adds this account to the DB so it gets a unique ID
        db.session.add(newAccount)
        db.session.flush()

        # Use that unique ID, and the current user's sessions ID to create the relationship
        newAccountRelation.id_bankAccount = newAccount.id
        newAccountRelation.id_patron = current_user.get_id()

        db.session.add(newAccountRelation)
        db.session.commit()

        flash("Savings account successfully created!")
        return redirect(url_for('accounts', id=current_user.get_id()) )

    return render_template('newSavingsAccount.html', title='Open a Savings Account' ,form=form)


@app.route('/accounts/<id>/new_Retirement_account', methods=['GET', 'POST'])
@login_required
def newRetirementAccount(id):
    form = CreateSavingsAccountForm()
    if form.validate_on_submit():
        newAccount = BankAccount()
        newAccountRelation = PatronBankAccounts()

        newAccount.accountType = "Retirement"
        newAccount.accountBalance = 0
        newAccount.accountName = form.accountName.data
        if (form.insurance.data):
            newAccount.insurance = 1
        else:
            newAccount.insurance = 0

        # Provisionally adds this account to the DB so it gets a unique ID
        db.session.add(newAccount)
        db.session.flush()

        # Use that unique ID, and the current user's sessions ID to create the relationship
        newAccountRelation.id_bankAccount = newAccount.id
        newAccountRelation.id_patron = current_user.get_id()

        db.session.add(newAccountRelation)
        db.session.commit()

        flash("Retirement account successfully created!")
        return redirect(url_for('accounts', id=current_user.get_id()) )

    return render_template('newRetirementAccount.html', title='Open a Retirement Account' ,form=form)