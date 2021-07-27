from flask import Blueprint, render_template, request,jsonify, redirect,url_for,flash
from flask_login import login_required, current_user
import numpy as np
from . import db
import pickle
import json
from .models import Borrower, Lender, Transaction, Users

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    return render_template("home.html", user=current_user)

@views.route('/loan-prediction', methods=['GET', 'POST'])
@login_required
def loanPrediction():
    if request.method == 'POST':
        from . import mlModel
        model=pickle.load(open('loan.pkl','rb'))
        features = [int(x) for x in request.form.values()]
        final = [np.array(features)]
        prediction=model.predict_proba(final)
        print(prediction)
        output = '{0:.{1}f}'.format(prediction[0][1],2)
        
        if output>str(0.5):
            return render_template("loanPrediction.html", 
            pred='Loan can be granted. The probability of loan repayment is {}'.format(output)
            ,user=current_user)
        else:
            return render_template("loanPrediction.html",
            pred='Loan cannot be granted. The probability of loan repayment is {}'.format(output)
            ,user=current_user)
    return render_template("loanPrediction.html",user=current_user)

@views.route('/borrowers-list', methods=['GET', 'POST'])
@login_required
def borrowersList():
    return render_template("borrowersList.html", user=current_user, users= Users.query.filter_by(lender_id=current_user.id),
    borrowers= Borrower.query.all())

@views.route('/lenders-list', methods=['GET', 'POST'])
@login_required
def lendersList():
    return render_template("lendersList.html", user=current_user, users= Users.query.filter_by(borrower_id= current_user.id)
    ,lenders= Lender.query.all())

@views.route('/transactions-list', methods=['GET', 'POST'])
@login_required
def transactionsList():
    print(request.args['user'])
    return render_template("transactionsList.html",user=Borrower.query.get(request.args['user']))

@views.route('/delete-borrower', methods=['POST'])
def deleteBorrower():
    borrower = json.loads(request.data)
    borrowerId = borrower['borrowerId']
    borrower = Borrower.query.get(borrowerId)
    if borrower:
        print(borrower.lender_id,current_user.id)
        if borrower.lender_id == current_user.id:
            db.session.delete(borrower)
            db.session.commit()

    return jsonify({})

@views.route('/delete-transaction', methods=['POST'])
def deleteTransaction():
    transaction = json.loads(request.data)
    transactionId = transaction['transactionId']
    userId = transaction['userId']
    transaction = Transaction.query.get(transactionId)
    if transaction:
        if transaction.borrower_id == str(userId):
            print(transaction.borrower_id, userId)
            db.session.delete(transaction)
            db.session.commit()

    return jsonify({})
