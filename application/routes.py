from application import app
from flask import Flask,redirect,url_for,flash,render_template,request,session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import time
import re

mysql = MySQL(app)

@app.route('/', methods=['GET', 'POST'])
def login():
	msg = ''
	if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
		username = request.form['username']
		password = request.form['password']
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('SELECT * FROM employee WHERE user_id = %s AND password = %s', (username, password,))
		account = cursor.fetchone()
		if (account):
			session['loggedin'] = True
			session['username'] = account['user_id']
			session['type'] = account['emp_type']
			return redirect(url_for('home'))
		else:
			msg = 'Incorrect username/password!'
	if 'loggedin' in session:
		return redirect(url_for('home'))
	return render_template('index.html', title='Sign In',msg = msg)

@app.route('/logout')
def logout():
	session.pop('loggedin', None)
	session.pop('username', None)
	session.pop('type', None)
	return redirect(url_for('login'))

@app.route('/home')
def home():
	if 'loggedin' in session and session['type']=='executive':
		return render_template('home1.html', username=session['username'],emp_type=session['type'])
	elif 'loggedin' in session and session['type']=='cashier':
		return render_template('home2.html', username=session['username'],emp_type=session['type'])
	return redirect(url_for('login'))
	

@app.route('/create_account', methods=['GET', 'POST'])
def c_account():
	msg = ''
	if request.method == 'POST' and 'customer_id' in request.form and 'account_type' in request.form and 'amount' in request.form:
		cid = int(request.form['customer_id'])
		acc_type = str(request.form['account_type'])
		amount = int(request.form['amount'])
		t = time.localtime(time.time())
		last_updated = str("%d-%d-%d %d:%d:%d" %(t.tm_year, t.tm_mon, t.tm_mday, t.tm_hour, t.tm_min, t.tm_sec))
		details = 'account created successfully'
		status = int('1')
		try:
			cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
			cursor.execute('SELECT count(*) FROM account WHERE customer_id = %s AND account_type = %s', (cid,acc_type))
			res = cursor.fetchone()
			if res['count(*)'] == 1:
				raise Exception('fail')
			else:
				cursor.execute('INSERT INTO account (customer_id, account_type, balance, message, last_updated, status) VALUES (%s, %s, %s, %s, %s, %s)', (cid, acc_type, amount, details, last_updated, status))
				mysql.connection.commit()
				flash('Account created successfully','success')
		except Exception as e:
			print('Failed to insert into account' + str(e))
			if str(e).find('foreign key constraint fails') != -1: 
				msg = 'Customer ID does not exist'
			elif str(e) == 'fail':
				msg = 'You already have ' + acc_type + ' account'
			else:
				msg = 'Could not create account...Please try again'
	if 'loggedin' in session and session['type']=='executive':
		return render_template('create_account.html', username=session['username'],emp_type=session['type'], msg=msg)
	return redirect(url_for('login'))


@app.route('/create_customer', methods=['GET', 'POST'])
def create_customer():
	msg=""
	if request.method == 'POST' and 'InputSSN' in request.form and 'InputName' in request.form:
		details = request.form
		InputSSN = details['InputSSN']
		InputName = details['InputName']
		InputAge = details['InputAge']
		InputAddress1 = details['InputAddress1']
		InputAddress2 = details['InputAddress2']
		InputAddress = InputAddress1 + " " + InputAddress2
		InputCity = details['InputCity']
		InputState = details['InputState']
		mess = "customer created successfully"
		stat = "1"
		try:
			cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

			cur.execute(
				"INSERT INTO customer( customer_ssn, name, age, address, city, state) VALUES (%s, %s, %s, %s, %s, %s)",
				(InputSSN, InputName, InputAge, InputAddress, InputCity, InputState))
			timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
			cur.execute("SELECT customer_id from customer where customer_ssn=" + InputSSN)
			res = cur.fetchone()
			cust_id = res["customer_id"]
			cur.execute("INSERT INTO customer_status(customer_id, message, last_updated, status) VALUES (%s, %s, %s, %s)",
						(cust_id, mess, timestamp, stat))
			mysql.connection.commit()
			flash('Customer created successfully', 'success')
			cur.close()

		except Exception as e:
			msg = "Could not insert into the table and please do not enter the existing Customer SSN ID"


		if 'loggedin' in session and session['type'] == 'executive':
			return render_template('create_customer.html', username=session['username'], emp_type=session['type'],
								   msg=msg)
	return render_template('create_customer.html')


