#importing packages
from flask import Flask,render_template,request,redirect,url_for,session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re

app = Flask(__name__)
app.secret_key = 'Muthu_shreya_NIT-T_Hackathon'
#configuration of MYSQL db - connection
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'

app.config['MYSQL_PASSWORD'] = 'MuthuPandas9'

app.config['MYSQL_DB'] = 'EVMUTHU'

mysql = MySQL(app)

@app.route('/')

@app.route('/ev_submission',methods=['POST','GET'])

def ev_submission():
    
    msg= ''

    if request.method == 'POST':
        print("Here-0")
        address = request.form['address']
        c_type = request.form['C_Type']
        price = request.form['Price']
        print("Here-1")
        print(address,c_type,price)

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        
        cursor.execute('INSERT INTO muthu_ev VALUES (NULL, % s, % s, % s)', (address, c_type, price, ))
        
        mysql.connection.commit()
        
        msg = 'The details submitted succesfully!!!'

    return render_template('ev_Submission.html',msg = msg)
    #print("Hi Hello")

if __name__ == "__main__":
    app.run(debug=True)