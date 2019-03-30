# coding: utf-8
from sqlalchemy import Column, ForeignKey, Integer, Numeric, Text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from appdir import db

Base = declarative_base()
metadata = Base.metadata


class BankAccountType(Base):
    __tablename__ = 'bankAccountType'

    accountType = Column(Text, primary_key=True)
    accountInterestRate = Column(Numeric, nullable=False)


class LoanType(Base):
    __tablename__ = 'loanType'

    loanCategory = Column(Text, primary_key=True)
    interestRate = Column(Numeric, nullable=False)


class Patron(Base):
    __tablename__ = 'patron'

    Id = Column(Integer, primary_key=True)
    patronFirstName = Column(Text, nullable=False)
    patronLastName = Column(Text, nullable=False)
    patronEmail = Column(Text, nullable=False)
    password = Column(Text, nullable=False)


class BankAccount(Base):
    __tablename__ = 'bankAccount'

    id = Column(Integer, primary_key=True)
    accountName = Column(Text, nullable=False)
    accountBalance = Column(Text, nullable=False)
    insurance = Column(Integer, nullable=False)
    accountType = Column(ForeignKey('bankAccountType.accountType'), nullable=False)

    bankAccountType = relationship('BankAccountType')


class Loan(Base):
    __tablename__ = 'loans'

    Id = Column(Integer, primary_key=True)
    loanPayment = Column(Numeric, nullable=False)
    loanBalance = Column(Numeric, nullable=False)
    startDate = Column(Text, nullable=False)
    endDate = Column(Text, nullable=False)
    loanCategory = Column(ForeignKey('loanType.loanCategory'), nullable=False)

    loanType = relationship('LoanType')
