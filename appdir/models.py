# coding: utf-8
from sqlalchemy import Column, ForeignKey, Integer, Numeric, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from appdir import db, login
from werkzeug.security import generate_password_hash, check_password_hash # Used for hashing PWs
from flask_login import UserMixin  # Used for adding login features to the patron class


class BankAccountType(db.Model):
    __tablename__ = 'bankAccountType'

    accountType = db.Column(db.Text, primary_key=True)
    accountInterestRate = db.Column(db.Numeric, nullable=False)

    def __repr__(self):
        # How this class is printed
        return '<Bank Account Type {}>'.format(self.accountType)


class LoanType(db.Model):
    __tablename__ = 'loanType'

    loanCategory = db.Column(db.Text, primary_key=True)
    interestRate = db.Column(db.Numeric, nullable=False)

    def __repr__(self):
        # How this class is printed
        return '<Loan Category (type) {}>'.format(self.loanCategory)


# adding UserMixin comes from flask_login to add requirements to this class to work with that library
class Patron(UserMixin, db.Model):
    __tablename__ = 'patron'

    id = db.Column(db.Integer, primary_key=True)
    patronFirstName = db.Column(db.Text, nullable=False)
    patronLastName = db.Column(db.Text, nullable=False)
    patronEmail = db.Column(db.Text, nullable=False)
    password = db.Column(db.Text, nullable=False)

    def __repr__(self):
        # How this class is printed
        return '<User Email {}>'.format(self.patronEmail)

    # Functions for hashing and then reading the passwords
    def setPassword(self, password):
        self.password = generate_password_hash(password)

    def checkPassword(self, password):
        return check_password_hash(self.password, password)


class BankAccount(db.Model):
    __tablename__ = 'bankAccount'

    id = db.Column(db.Integer, primary_key=True)
    accountName = db.Column(db.Text, nullable=False)
    accountBalance = db.Column(db.Text, nullable=False)
    insurance = db.Column(db.Integer, nullable=False)
    accountType = db.Column(db.ForeignKey('bankAccountType.accountType'), nullable=False)

    bankAccountType = relationship('BankAccountType')

    def __repr__(self):
        # How this class is printed
        return '<Bank Account Name {}>'.format(self.accountName)


class Loan(db.Model):
    __tablename__ = 'loans'

    id = db.Column(db.Integer, primary_key=True)
    loanPayment = db.Column(db.Numeric, nullable=False)
    loanBalance = db.Column(db.Numeric, nullable=False)
    startDate = db.Column(db.Text, nullable=False)
    endDate = db.Column(db.Text, nullable=False)
    loanCategory = db.Column(db.Text, db.ForeignKey('loanType.loanCategory'), nullable=False)

    loanType = relationship('LoanType')

    def __repr__(self):
        # How this class is printed
        return '<Loan ID {}>'.format(self.id)


class patronBankAccounts(db.Model):
    __tablename__ = 'patronBankAccounts'

    id_patron = db.Column(db.Integer, db.ForeignKey('patron.id'), primary_key=True)
    id_account = db.Column(db.Integer, db.ForeignKey('bankAccount.id'), primary_key=True)


class patronLoanAccounts(db.Model):
    __tablename__ = 'patronLoanAccounts'

    id_patron = db.Column(db.Integer, db.ForeignKey('patron.id'), primary_key=True)
    id_account = db.Column(db.Integer, db.ForeignKey('loans.id'), primary_key=True)


@login.user_loader
def loadUser(id):
    return Patron.query.get(int(id))