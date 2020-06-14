from application import app
from flask import Flask,redirect,url_for,flash,render_template,request,session
from flask_mysqldb import MySQL
import MySQLdb.cursors

mysql = MySQL(app)
values = {}

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

@app.route('/customer_status',methods=['GET', 'POST'])
def customer_status():
	global values
	if('loggedin' not in session):
		return redirect(url_for('login'))
	cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
	if (request.method == 'POST' and 'cust_id' in request.form):
		cust_id = request.form['cust_id']
		cursor.execute('SELECT C.customer_ssn, C.customer_id, S.message, S.last_updated,S.status FROM customer C,customer_status S WHERE C.customer_id = S.customer_id AND S.customer_id ='+cust_id)
		new_values = cursor.fetchall()
		session['updated_status'] = new_values
		return redirect(url_for('customer_status'))
	if(values):
		return render_template('customer_status.html', values=values)
	cursor.execute('SELECT C.customer_ssn, C.customer_id, S.message, S.last_updated,S.status FROM customer C,customer_status S WHERE C.customer_id = S.customer_id')
	values = cursor.fetchall()
	return render_template('customer_status.html',values=values)