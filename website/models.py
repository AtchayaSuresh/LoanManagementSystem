from operator import add
from . import db
from flask_login import UserMixin
#from sqlalchemy.sql import func

# users=db.Table('User',
# db.Column('lender_id',db.String(5),db.ForeignKey('lender.id')),
# db.Column('borrower_id',db.String(5),db.ForeignKey('borrower.id')),
# db.Column('amount',db.Float)
# )

class Users(db.Model,UserMixin):
    id= db.Column(db.Integer, primary_key = True)
    lender_id=db.Column(db.String(5),db.ForeignKey('lender.id'))
    borrower_id=db.Column(db.String(5),db.ForeignKey('borrower.id'))
    amount=db.Column(db.Float)
# class Note(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     data = db.Column(db.String(10000))
#     date = db.Column(db.DateTime(timezone=True), default=func.now())
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

# def get_user(id):
#     user = Lender.query.filter_by(id=id).first()
#     if user:
#         return user
#     return Borrower.query.filter_by(id=id).first()

class Lender(db.Model, UserMixin):
    id=db.Column(db.String(5),primary_key=True)
    name = db.Column(db.String(150))

    phoneNo = db.Column(db.String(10), unique=True)
    panNo = db.Column(db.String(20))
    gstNo = db.Column(db.String(20))
    companyName = db.Column(db.String(200))

    address = db.Column(db.String(500))
    addressProof  = db.Column(db.String(20))
    idProof = db.Column(db.String(20))
    password = db.Column(db.String(20))
    accountType = db.Column(db.String(15))
    
    # borrowers =  db.relationship('Borrower',secondary=users, backref=db.backref('lenders', lazy= 'dynamic'))
    #lenders = db.relationship('Lender')
    #notes = db.relationship('Note')

class Borrower(db.Model,UserMixin):
    id = db.Column(db.String(5),primary_key=True)
    address = db.Column(db.String(500))
    phoneNo = db.Column(db.String(10), unique=True)

    firstName = db.Column(db.String(150))
    lastName = db.Column(db.String(150))
    password = db.Column(db.String(20))

    amountBorrowed = db.Column(db.Float)
    addressProof = db.Column(db.String(20))
    idProof = db.Column(db.String(20))
    accountType = db.Column(db.String(15))

    # lender_id = db.Column(db.String(5), db.ForeignKey('lender.id'))
    transactions = db.relationship('Transaction')

class Transaction(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    date = db.Column(db.String(20))
    amount = db.Column(db.Float)
    type= db.Column(db.String(5))
    borrower_id = db.Column(db.String(5),db.ForeignKey('borrower.id'))
    lender_id = db.Column(db.String(5),db.ForeignKey('lender.id'))