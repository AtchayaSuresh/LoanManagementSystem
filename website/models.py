from operator import add
from . import db
from flask_login import UserMixin

class User(db.Model,UserMixin):
    id= db.Column(db.Integer, primary_key = True)
    lender_id=db.Column(db.String(5),db.ForeignKey('lender.id'))
    borrower_id=db.Column(db.String(5),db.ForeignKey('borrower.id'))
    principal=db.Column(db.Float)
    amount = db.Column(db.Float)
    interest = db.Column(db.Float)
    previousMonth = db.Column(db.Integer)

class Lender(db.Model, UserMixin):
    id=db.Column(db.String(5),primary_key=True)
    name = db.Column(db.String(150))

    phoneNo = db.Column(db.String(10), unique=True)
    panNo = db.Column(db.String(20))
    gstNo = db.Column(db.String(20))
    companyName = db.Column(db.String(200))

    address = db.Column(db.Text)
    addressProof  = db.Column(db.String(20))
    idProof = db.Column(db.String(20))
    password = db.Column(db.String(20))
    accountType = db.Column(db.String(15))
 
class Borrower(db.Model,UserMixin):
    id = db.Column(db.String(5),primary_key=True)
    address = db.Column(db.Text)
    phoneNo = db.Column(db.String(10), unique=True)

    firstName = db.Column(db.String(150))
    lastName = db.Column(db.String(150))
    password = db.Column(db.String(20))
    
    addressProof = db.Column(db.String(20))
    idProof = db.Column(db.String(20))
    accountType = db.Column(db.String(15))

    transactions = db.relationship('Transaction')

class Transaction(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    date = db.Column(db.Date)
    amount = db.Column(db.Float)
    type= db.Column(db.String(5))
    borrower_id = db.Column(db.String(5),db.ForeignKey('borrower.id'))
    lender_id = db.Column(db.String(5),db.ForeignKey('lender.id'))