import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import pickle

loan=pd.read_csv('./loanData.csv')

loan['paid_off_time'] = loan['paid_off_time'].apply(lambda x: 0 if x == ' ' else x)
loan['past_due_days'] = loan['past_due_days'].apply(lambda x: 0 if x == ' ' else x)

loan['paid_off_time'].fillna(0, inplace = True)
loan['past_due_days'].fillna(0, inplace = True)

from sklearn.preprocessing import LabelEncoder
le=LabelEncoder()
loan['Gender']=le.fit_transform(loan['Gender'])
loan['education']=le.fit_transform(loan['education'])
loan['loan_status']=le.fit_transform(loan['loan_status'])

from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix,accuracy_score,classification_report
x_train,x_test,y_train,y_test=train_test_split(loan.drop(
    ['effective_date','due_date','paid_off_time','Loan_ID','loan_status'],axis=1),
    loan['loan_status'],test_size=0.25,random_state=0)

lrr=LogisticRegression().fit(x_train,y_train)

pickle.dump(lrr,open('loan.pkl','wb'))