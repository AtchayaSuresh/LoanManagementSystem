import re
import types
from flask import Blueprint, render_template, request, flash, redirect, url_for
from werkzeug import useragents
from .models import Borrower,Lender,Transaction
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user


auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        id = request.form.get('id')
        password = request.form.get('password')

        lender = Lender.query.filter_by(id=id).first()
        if lender:
            if check_password_hash(lender.password, password):
                flash('Logged in successfully!', category='success')
                login_user(lender, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            borrower = Borrower.query.filter_by(id=id).first()
            if borrower:
                if check_password_hash(borrower.password, password):
                    flash('Logged in successfully!',category='success')
                    login_user(borrower,remember=True)
                    return redirect(url_for('views.home'))
                else:
                    flash('Incorrect password, try again.',category='error')
            flash('Lender does not exist.', category='error')

    return render_template("login.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        print(request)
        name = request.form.get('name')
        phoneNo = request.form.get('phoneNo')
        panNo = request.form.get('panNo')
        gstNo = request.form.get('gstNo')
        companyName = request.form.get('companyName')
        address = request.form.get('address')
        addressProof = request.form.get('addressProof')
        idProof = request.form.get('idProof')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        lender = Lender.query.filter_by(phoneNo=phoneNo).first()
        if lender:
            flash('Lender already exists.', category='error')
        elif len(phoneNo) < 8:
            flash('Enter Valid Phone Number', category='error')
        elif len(name) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            import random
            id = random.randint(1,99999)
            while Lender.query.filter_by(id=id).first() or Borrower.query.filter_by(id=id).first():
                id = random.randint(1,99999)
            id=str(id)
            id=((5-len(id))*'0')+id
            new_lender = Lender(id=id, name=name,phoneNo=phoneNo,panNo=panNo,
            gstNo=gstNo, companyName=companyName, address=address, addressProof= addressProof,
            idProof=idProof, password=generate_password_hash(
                password1, method='sha256'),accountType='Lender')
            db.session.add(new_lender)
            db.session.commit()
            login_user(new_lender, remember=True)
            flash('Account created! Your Lender ID is '+str(id)+
            '. Use this ID to login into your account', category='success')
            return redirect(url_for('views.home'))

    return render_template("sign_up.html", user=current_user)


@auth.route('/create-borrower',methods=['GET','POST'])
@login_required
def createBorrower():
    if request.method == 'POST':
        firstName = request.form.get('firstName')
        lastName = request.form.get('lastName')
        phoneNo = request.form.get('phoneNo')
        amountBorrowed = request.form.get('amountBorrowed')
        address = request.form.get('address')
        addressProof = request.form.get('addressProof')
        idProof = request.form.get('idProof')

        borrower = Borrower.query.filter_by(phoneNo=phoneNo).first()
        if borrower:
            flash('Borrower already exists.', category='error')
        elif len(phoneNo) < 7:
            flash('Enter Valid Phone Number', category='error')
        elif len(firstName) < 2:
            flash('First name must be greater than 1 character.', category='error')
        else:
            import random
            id = random.randint(1,99999)
            while Lender.query.filter_by(id=id).first() or Borrower.query.filter_by(id=id).first():
                id = random.randint(1,99999)
            id=str(id)
            id=((5-len(id))*'0')+id
            newBorrower = Borrower(id=id,firstName=firstName,lastName=lastName, phoneNo=phoneNo,
            amountBorrowed=amountBorrowed,address = address, addressProof = addressProof,
            idProof = idProof, accountType='Borrower',password=generate_password_hash(
                phoneNo, method='sha256') ,lender_id = current_user.id)
            db.session.add(newBorrower)
            db.session.commit()
            flash('Account created!', category='success')
            return redirect(url_for("views.borrowersList"))
    return render_template("createBorrower.html", user=current_user)

@auth.route('/borrower-page', methods=['GET', 'POST'])
@login_required
def borrower_page():
    return render_template("borrower_page.html",user= request.args['user'])

@auth.route('/transaction',methods=['GET','POST'])
@login_required
def transaction():
    user=Borrower.query.get(request.args['user'])
    if request.method=='POST':
        date = request.form.get('date')
        amount = request.form.get('amount')
        type = request.form.get('type')

        transaction = Transaction(date=date, amount=amount, type= type, borrower_id=request.args['user'])
        db.session.add(transaction)
        db.session.commit()
        flash('Transaction Added!',category =' success')
        return render_template("transactionsList.html",user=user)
    return render_template("transaction.html",user=user)