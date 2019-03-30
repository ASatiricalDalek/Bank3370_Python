# coding: utf-8
from sqlalchemy import Column, ForeignKey, Integer, Numeric, Text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from appdir import db


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


class Patron(db.Model):
    __tablename__ = 'patron'

    Id = db.Column(db.Integer, primary_key=True)
    patronFirstName = db.Column(db.Text, nullable=False)
    patronLastName = db.Column(db.Text, nullable=False)
    patronEmail = db.Column(db.Text, nullable=False)
    password = db.Column(db.Text, nullable=False)

    def __repr__(self):
        # How this class is printed
        return '<User Email {}>'.format(self.patronEmail)


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

    Id = db.Column(db.Integer, primary_key=True)
    loanPayment = db.Column(db.Numeric, nullable=False)
    loanBalance = db.Column(db.Numeric, nullable=False)
    startDate = db.Column(db.Text, nullable=False)
    endDate = db.Column(db.Text, nullable=False)
    loanCategory = db.Column(db.Text, db.ForeignKey('loanType.loanCategory'), nullable=False)

    loanType = relationship('LoanType')

    def __repr__(self):
        # How this class is printed
        return '<Loan ID {}>'.format(self.Id)

class patronBankAccounts(db.Model):
    __tablename__ = 'patronBankAccounts'

    id_patron = db.Column(db.Integer, db.ForeignKey('patron.Id'), primary_key=True)
    id_account = db.Column(db.Integer, db.ForeignKey('bankAccount.id'), primary_key=True)

class patronLoanAccounts(db.Model):
    __tablename__ = 'patronLoanAccounts'

    id_patron = db.Column(db.Integer, db.ForeignKey('patron.Id'), primary_key=True)
    id_account = db.Column(db.Integer, db.ForeignKey('loans.Id'), primary_key=True)