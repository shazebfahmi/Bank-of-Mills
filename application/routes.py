from application import app
from flask import Flask,redirect,url_for,flash,render_template,request,session
from flask_mysqldb import MySQL 
import MySQLdb
import MySQLdb.cursors
import time
from datetime import datetime
import re
import requests

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


@app.route('/customer_status',methods=['GET', 'POST'])
def customer_status():
	if('loggedin' not in session):
		return redirect(url_for('login'))
	if (request.method == 'POST'):
		return redirect(url_for('customer_status'))
	cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
	cursor.execute('SELECT C.customer_ssn, C.customer_id, S.message, S.last_updated,S.status FROM customer C,customer_status S WHERE C.customer_id = S.customer_id AND S.status=1;')
	values = cursor.fetchall()
	return render_template('customer_status.html',values=values)

@app.route('/create_account', methods=['GET', 'POST'])
def c_account():
	msg = ''
	if request.method == 'POST' and 'customer_id' in request.form and 'account_type' in request.form and 'amount' in request.form:
		cid = int(request.form['customer_id'])
		acc_type = str(request.form['account_type'])
		amount = int(request.form['amount'])
		last_updated = str(datetime.utcnow())
		details = 'account created successfully'
		status = int('1')
		try:
			cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
			cursor.execute('SELECT count(*) FROM account WHERE customer_id = %s AND account_type = %s and status = 1', (cid,acc_type))
			res = cursor.fetchone()
			cursor.execute('SELECT count(*) FROM customer_status WHERE customer_id = %s AND status = 1', (cid,))
			res2 = cursor.fetchone()
			if res['count(*)'] == 1:
				raise Exception('fail')
			elif res2['count(*)'] != 1:
				raise Exception('nocus')
			else:
				cursor.execute('INSERT INTO account (customer_id, account_type, balance, message, last_updated, status) VALUES (%s, %s, %s, %s, %s, %s)', (cid, acc_type, amount, details, last_updated, status))
				cursor.execute('SELECT account_id FROM account WHERE customer_id = %s and account_type = %s', (cid, acc_type))
				res = cursor.fetchone()
				aid = res['account_id']
				cursor.execute('INSERT INTO transactions (customer_id, account_id, description, acc_type, amount) VALUES (%s, %s, %s, %s, %s)', (cid, aid, 'deposit', acc_type, amount))
				mysql.connection.commit()
				flash('Account created successfully','success')
				return redirect(url_for('home'))
		except Exception as e:
			print('Failed to insert into account' + str(e))
			if str(e).find('foreign key constraint fails') != -1: 
				msg = 'Customer ID does not exist'
			elif str(e) == 'fail':
				msg = 'You already have a ' + acc_type + ' account'
			elif str(e) == 'nocus':
				msg = 'Customer does not exist!'
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
		InputAge=str(InputAge)
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
			timestamp = datetime.utcnow()
			cur.execute("SELECT customer_id from customer where customer_ssn=" + InputSSN)
			res = cur.fetchone()
			cust_id = res["customer_id"]
			cur.execute("INSERT INTO customer_status(customer_id, message, last_updated, status) VALUES (%s, %s, %s, %s)",
						(cust_id, mess, timestamp, stat))
			mysql.connection.commit()
			flash('Customer created successfully', 'success')
			cur.close()
			return redirect(url_for('login'))
		except Exception as e:
			msg = "Please enter a valid Customer SSN ID"

	if 'loggedin' in session and session['type'] == 'executive':
			return render_template('create_customer.html', username=session['username'], emp_type=session['type'],
								   msg=msg)
	return redirect(url_for('login'))


######## CUSTOMER UPDATE ########
@app.route('/update_search')
def update_search():
	if 'loggedin' in session and session['type'] == 'executive':
		return render_template('update_search.html')
	return redirect(url_for('login'))
@app.route("/update",methods=['GET','POST'])
def update():
	if(request.method=='POST' and ('SSN' in request.form or 'CUSTOMER_ID' in request.form)) :
		ssn=request.form['SSN']
		Id=request.form['CUSTOMER_ID']
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('SELECT * FROM customer WHERE customer_id = %s or customer_ssn=%s', (Id,ssn))
		details = cursor.fetchone()
		if(details is None):
			flash("Could not find an account with given details!","danger")
			return redirect('/update_search')
		cursor.execute('SELECT status FROM customer_status WHERE customer_id = %s ', (details['customer_id'],))
		details2=cursor.fetchone()
		if(details2['status']!=1):
			flash("Customer no longer exists exists!","danger")
			return redirect('/update_search')
	if request.method=='POST' and ('new_name' in request.form or 'new_age' in request.form or 'new_address' in request.form) :
		n_name=request.form['new_name']
		n_addr=request.form['new_address']
		n_age=request.form['new_age']
		Id=request.form['ID']
		timestamp = timestamp = datetime.utcnow()
		print(timestamp)
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute("UPDATE customer SET name = %s,address=%s,age=%s WHERE customer_id=%s",(n_name,n_addr,n_age,Id,))
		cursor.execute("UPDATE customer_status SET message=%s WHERE customer_id=%s",("customer update complete",Id,))
		cursor.execute("UPDATE customer_status SET message=%s WHERE last_updated=%s",(timestamp,Id,))
		cursor.execute("COMMIT")
		flash("Successfully Updated","success")
		return redirect(url_for('login'))
	if 'loggedin' in session and session['type']=='executive':
		return render_template("update.html",details=details)
	return redirect(url_for('login'))


	
######## ACCOUNT STATUS ####### 
@app.route('/account_status',methods=['GET','POST'])
def account_status():
	cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
	cursor.execute("SELECT * FROM account")
	details_raw=list(cursor.fetchall())
	details=[]
	for i in details_raw:
		if(i['status']==1):
			details.append(i)
	if request.method=='POST' and 'refresh' in request.form :
		return redirect('/account_status')
	if 'loggedin' in session and session['type']=='executive':
		return render_template("account_status.html",details=details)
	return redirect(url_for('login'))
	


##### CUSTOMER SEARCH ######### 
@app.route('/customer_search')
def customer_search():
	if 'loggedin' in session and session['type']=='executive':
		return render_template('customer_search.html')
	return redirect(url_for('login'))
@app.route('/customer_detail',methods=['GET','POST'])
def customer_detail():
	if request.method=='POST' and ('SSN' in request.form or 'CUSTOMER_ID' in request.form) :
		ssn=request.form['SSN']
		Id=request.form['CUSTOMER_ID']
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('SELECT * FROM customer WHERE customer_id = %s or customer_ssn=%s', (Id,ssn))
		customer_detail1 = cursor.fetchone()
		if(customer_detail1 is None):
			flash("No user available with given SSN ID/Customer ID","danger")
			return redirect('/customer_search')
		cust_id=customer_detail1['customer_id']
		cursor.execute('SELECT * FROM customer_status WHERE customer_id = %s', (cust_id,))
		customer_detail2=cursor.fetchone()
		if(customer_detail2['status']!=1):
			flash("Customer no longer exists exists","danger")
			return redirect('/customer_search')
		if 'loggedin' in session and session['type']=='executive':
			return render_template("customer_detail.html",customer_detail1=customer_detail1 ,customer_detail2=customer_detail2)
		return redirect(url_for('login'))
		
	



####delete customer page####
@app.route('/delete_customer',methods=['GET','POST'])
def delete_customer():
	if('loggedin' not in session):
		return redirect(url_for('login'))
	if('loggedin' in session and session['type'] != 'executive'):
		return redirect(url_for('home'))
	checked = False
	details = None
	msg= ""
	if  request.method =='POST' and request.form['btn']=='back':
		return redirect('home')
	if  request.method =='POST' and request.form['btn']=='d':
		print("deleted query deetcted")
		try:
			cursor2 = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
			id2 = request.form['customer_id']
			print("Hello this was customer id",id2)
			
			#print("\n queru=y is : "+query)
			timestamp = datetime.utcnow()
			print("after timestamp")
			cursor2.execute("UPDATE customer_status set status = 0,message='customer deleted successfully', last_updated = %s  where customer_id = %s",(timestamp,id2))
			cursor2.execute("update account set status = 0,message='account deleted successfully *',last_updated = %s where customer_id = %s ",(timestamp,id2))
			print("delete query executed")
			cursor2.execute("COMMIT")
			print('delete query committed')
			flash('Customer and all related accounts deleted successfully','success')
			cursor2.close()
			
		except:
			print("in except of delete   ")
		return render_template('delete_customer.html',checked = checked,details = details,msg =msg ) 	
		
	if  request.method =='POST' and 'customer_id' in  request.form:
		print('post detected and customer id was ', request.form['customer_id'] )
		print('post detected and  btn id was ', request.form['btn'] )
		id = request.form['customer_id']
		try:
			cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
			query = "SELECT c.customer_id,c.customer_ssn,c.name, c.age, c.address,c.city, c.state FROM customer c, customer_status cs where c.customer_id = cs.customer_id and cs.status = 1 and c.customer_id ="+ id
			cursor.execute(query)
			print('query executed')
			details = cursor.fetchone()
			cursor.close()
			if(details is None):
				print('deyail is none')
				x = 'Could not search for the customer :'+  id
				msg =x
				#flash(x,'success')
				return render_template('delete_customer.html',checked = checked,msg=msg)
			checked = True
			#print(type(details),details)
			
		except Exception as e:
			print("in except of retrieve  :" +str(e))
			msg = "Could not search for the customer"
	
	
	return render_template('delete_customer.html',checked = checked,details =details,msg=msg)

@app.route('/delete_account',methods=['GET','POST'])
def delete_account():
	msg=""
	if request.method=='POST' and ('account_id' in request.form) :
		account_id=request.form['account_id']
		try:
			cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
			cursor.execute('SELECT * FROM account WHERE account_id = %s and status=1 ', (account_id,))
			details = cursor.fetchone()
			acc_id = details['account_id']
			cust_id = details['customer_id']
			acc_type = details['account_type']
			bal = details['balance']
			message = details['message']
			acc_created = details['account_created']
			last_updated = details['last_updated']
			status = details['status']
			mysql.connection.commit()
			cursor.close()

			return render_template('del_acc_details.html', acc_id=acc_id, cust_id=cust_id, acc_type=acc_type, bal=bal,
											   message=message, acc_created=acc_created, last_updated=last_updated, status=status)
		except Exception as e:
			msg="Please enter valid Account Id"

	if 'loggedin' in session and session['type'] == 'executive':
		return render_template('delete_account.html', username=session['username'], emp_type=session['type'], msg=msg)

	return redirect(url_for('login'))

@app.route('/del_acc_details',methods=['GET','POST'])
def delete_account_details():
	msg = ""
	if request.method == 'POST' and ('acc_id' in request.form ):
		account_id = request.form['acc_id']

		try:
			cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
			cursor.execute('UPDATE account SET status=0 WHERE account_id = %s ', (account_id,))
			cursor.execute('UPDATE account SET message="account deleted successfully" WHERE account_id = %s ', (account_id,))
			mysql.connection.commit()
			flash('Customer account deleted successfully', 'success')
			cursor.close()
			return redirect(url_for('home'))
		except Exception as e:
			msg="Could not delete, Please try again later!"

	if 'loggedin' in session and session['type'] == 'executive':
		return render_template('del_acc_details.html', username=session['username'], emp_type=session['type'], msg=msg)
	return redirect(url_for('login'))


@app.route('/search_account')
def search_account():
	if 'loggedin' in session and session['type'] == 'cashier':
		return render_template('search_account.html', username=session['username'], emp_type=session['type'])
	else:
		return redirect(url_for('login'))


@app.route('/display_search_account',methods=['GET','POST'])
def display_search_account():
	if request.method == 'GET' and 'account_id' in request.args:
		account_id = request.args['account_id']
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('SELECT * FROM account A,customer C WHERE A.customer_id=C.customer_id AND account_id = %s AND status=1',(account_id,))
		values_account = cursor.fetchone()
		if (values_account):
			return render_template('display_search_account.html', values_account=values_account)
		return redirect(url_for('search_account'))
	if 'loggedin' in session and session['type'] == 'cashier':
		if (request.method=='POST' and 'account_select' in request.form):
			account_id = request.form['account_select']
			cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
			cursor.execute('SELECT * FROM account A,customer C WHERE A.customer_id = C.customer_id AND A.account_id = %s', (account_id,))
			values_account_select = cursor.fetchone()
			cust_id = values_account_select['customer_id']
			cursor.execute('SELECT * FROM account A,customer C,customer_status S WHERE A.customer_id = C.customer_id AND C.customer_id = S.customer_id AND A.customer_id = %s AND S.status=1 AND A.status=1', (cust_id,))
			values_customer = cursor.fetchall()
			return render_template('display_search_account.html',values_account_select = values_account_select,values_customer = values_customer)
		elif request.method == 'POST' and ('customer_id' or 'customer_ssn' or 'account_id' in request.form):
			customer_id = request.form['customer_id']
			customer_ssn = request.form['customer_ssn']
			account_id = request.form['account_id']
			cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
			if(account_id == '' and customer_id == '' and customer_ssn == ''):
				flash('Please enter either of the search terms!','danger')
				return redirect(url_for('search_account'))
			if(account_id == '' and customer_id == ''):
				cursor.execute('SELECT C.customer_id,C.name FROM customer C,customer_status S WHERE C.customer_ssn = %s AND C.customer_id=S.customer_id AND S.status=1;', (customer_ssn,))
				values = cursor.fetchone()
				if(values):
					customer_id = values['customer_id']
				else:
					flash('No results found for the search criteria','danger')
					return redirect(url_for('search_account'))
			if(account_id == ''):
				cursor.execute('SELECT * FROM account A,customer C,customer_status S WHERE A.customer_id = C.customer_id AND C.customer_id = S.customer_id AND A.customer_id = %s AND S.status=1 AND A.status=1', (customer_id,))
				values_customer = cursor.fetchall()
				if(values_customer):
					return render_template('display_search_account.html',values_customer = values_customer)
				else:
					flash('No results found for the search criteria', 'danger')
					return redirect(url_for('search_account'))
			else:
				cursor.execute('SELECT * FROM account A,customer C WHERE A.customer_id=C.customer_id AND account_id = %s AND status=1', (account_id,))
				values_account = cursor.fetchone()
				if(values_account):
					return render_template('display_search_account.html',values_account = values_account)
				else:
					flash('No results found for the search criteria', 'danger')
					return redirect(url_for('search_account'))
		else:
			return redirect(url_for('search_account'))
	else:
		redirect(url_for('login'))

@app.route('/deposit_money',methods=['GET','POST'])
def deposit_money():
	msg = ''
	if request.method == 'POST' and 'd_amount' in request.form:
		cust_id = request.form['cid']
		acc_id = request.form['aid']
		acc_type = request.form['a_type']
		bal = request.form['balance']
		amt = request.form['d_amount']
		ts = datetime.utcnow()
		try:
			t_amt = int(amt) + int(bal)
			cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
			cursor.execute('INSERT INTO transactions (customer_id, account_id, description, acc_type, amount) VALUES (%s, %s, %s, %s, %s)', (cust_id, acc_id, 'deposit', acc_type, amt))
			cursor.execute('UPDATE account SET balance = %s, message = %s, last_updated = %s WHERE account_id = %s and status = 1', (t_amt, 'amount deposited successfully', ts, acc_id))
			mysql.connection.commit()
			flash('Amount deposited successfully','success')
			return redirect(url_for('display_search_account',account_id=acc_id))
		except Exception as e:
			msg = 'could not deposit money...Please try again'
	if 'loggedin' in session and session['type']=='cashier' and ('cid' and 'aid' and 'name' and 'a_type' and 'balance' in request.form):
		data = []
		data.append(request.form['cid'])
		data.append(request.form['aid'])
		data.append(request.form['name'])
		data.append(request.form['a_type'])
		data.append(request.form['balance'])
		return render_template('deposit_money.html', username=session['username'],emp_type=session['type'], msg=msg, data=data)
	return redirect(url_for('login'))

@app.route('/transfer_money',methods=['GET','POST'])
def transfer_money():
	msg=''
	if 'loggedin' in session and session['type'] == 'cashier':
		if request.form.get('btn') == 'transfer_btn':
			amount = request.form.get('amount')
			
			bal = request.form.get('balance')
			
			print("amount enterred = "+amount+" balance is : "+bal)
			if (int(bal) - int(amount)) < 1000:
				msg = 'Amount cannot be transfered, to maintain minimum balance (try smaller amount)'
				print("masg updated")
			
				
			#return render_template('transfer_money.html',msg=msg)
			
			
		
		cred = request.args.getlist('val')
		print(cred,type(cred))
		cust_id = cred[0]
		acc_id = cred[1]
		cus_name = cred[2]
		acc_type = cred[3]
		bal = cred[4]
		
		try:
			cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
			cursor.execute('SELECT account_id FROM account where status = 1 and customer_id = %s', (cust_id,))
			accs = cursor.fetchall()
			if len(accs)!=2:
				flash("Cannot transfer, since only one type of account exists, for this customer ",'success')
				return redirect(url_for('home'))
		except:
			print("diugfjkf")
			
		
		print(" Customer id = "+str(cust_id)+" Account id "+acc_id+"  account type" + acc_type+ " bal : "+bal)
		
			
		return render_template('transfer_money.html',cust_id=cust_id,acc_id=acc_id,cus_name=cus_name,acc_type=acc_type,bal=bal,msg=msg)
		
	else:
		return redirect(url_for('login'))


@app.route('/verify_balance_and_execute',methods=['GET','POST'])
def verify_balance_and_execute():

	if 'loggedin' in session and session['type'] == 'cashier':
		bal = request.form.get('balance')
		amt = request.form.get('amount')
		id =  request.form.get('cus_id')
		acc_id =  request.form.get('acc_id')
		name = request.form.get('name')
		stype = request.form.get('s_acc')
		dtype = request.form.get('d_acc')
		
		print("cus id in verify :"+id+" bal : "+bal+" amt "+amt+" acc id "+acc_id+" name : "+name+" s type "+stype+" dtype :"+dtype)
		if int(bal) - int(amt) < 1000:
			flash("Cannot transfer, try again with lesser amount",'success')
			return redirect(url_for('transfer_money',val=(id,acc_id,name,stype,bal) ) )
		else:
			ts = datetime.utcnow()
			try:
				cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
				cursor.execute('update account set balance = %s , message = "account debited successfully" , last_updated = %s where account_id = %s  and status =1',(str(int(bal)-int(amt)),ts,acc_id))
				cursor.execute('select balance,account_id from account where customer_id = %s and status=1 and account_type= %s ', (id,dtype))
				abal = cursor.fetchall()
				cbal = abal[0]['balance']
				dacc_id = abal[0]['account_id']
				print(cbal,type(cbal))
				print("destiation acc no : ",dacc_id)
				cursor.execute('update account set balance = %s , message = "account credited successfully" , last_updated = %s where account_type = %s and status =1',(str(cbal+int(amt)),ts,dtype))
				
				#for transactions table updation
				#one = "insert into transactions (customer_id,account_id,description,acc_type,time,amount)  values ('{0}','{1}','withdraw','{2}','{3}',{4})  ".format(id,acc_id,stype,ts,amt)
				
				#print(one)
				
				
				cursor.execute("insert into transactions (customer_id,account_id,description,acc_type,time,amount)  values (%s,%s,'withdraw',%s,%s,%s)  ",(id,acc_id,stype,ts,amt))
				
				cursor.execute("insert into transactions (customer_id,account_id,description,acc_type,time,amount)  values (%s,%s,'deposit',%s,%s,%s)  ",(id,dacc_id,dtype,ts,amt))
				
				
				
				#cursor.execute('update account set balance = %d , message = "amount recieved successfully" , last_updated = %s where account_id != %s and status = 1 ', (int(bal)+diff,ts,acc_id))
				#accs = cursor.fetchall()
				'''if len(accs)!=2:
					flash("Cannot transfer, ",'success')
					return redirect(url_for('home'))'''
					
				#print("cursor val size :",len(accs))
				mysql.connection.commit()
				flash('Amount transferred successfully','success')
				return redirect(url_for('login'))
			except Exception as e:
				print('Failed to transfer :  ' + str(e))
				msg = 'could not deposit money...Please try again'
		#print(type(bal),type(amt))
		
		
		
		
		return redirect(url_for('home'))
		
	else:
		return redirect(url_for('login'))



@app.route('/account_statement')
def account_statement():
	if('loggedin' in session and session['type'] == 'cashier'):
		return render_template('account_statement.html',username=session['username'],emp_type=session['type'])
	else:
		return redirect(url_for('login'))

@app.route('/display_statement',methods=['POST'])
def display_statement():
	if('loggedin' in session and session['type'] == 'cashier'):
		if(request.method == 'POST' and 'account_id' in request.form):
			cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
			account_id = request.form['account_id']
			radio_option = request.form['radio_options']
			if(radio_option == 'last'):
				if('num_transactions' not in request.form):
					flash("Please enter the number of transactions to be fetched.", 'danger')
					return redirect(url_for('account_statement'))
				count = request.form['num_transactions']
				val = 'SELECT * FROM transactions WHERE account_id = %s ORDER BY time DESC LIMIT %s ' % (account_id,count)
				# return render_template('display_statement.html', bla=val)
				cursor.execute(val)
				transactions = cursor.fetchall()
				if(transactions):
					return render_template('display_statement.html',transactions=transactions)
				else:
					flash("No transactions found.",'danger')
					return redirect(url_for('account_statement'))
			else:
				start_date = request.form['start_date']
				end_date = request.form['end_date']
				if(start_date == '' or end_date==''):
					flash("Please enter the start and end dates.", 'danger')
					return redirect(url_for('account_statement'))
				start_date+=' 00:00:01'
				end_date += ' 23:59:59'
				start_check = datetime.strptime(start_date,'%Y-%m-%d %H:%M:%S')
				end_check = datetime.strptime(end_date,'%Y-%m-%d %H:%M:%S')
				if(start_check > end_check):
					flash("Start date is greater than End date.", 'danger')
					return redirect(url_for('account_statement'))
				query = 'SELECT * FROM transactions WHERE (time BETWEEN "%s" AND "%s" AND account_id = %s) ORDER BY time DESC' % (start_date,end_date,account_id)
				cursor.execute(query)
				transactions = cursor.fetchall()
				if(transactions):
					return render_template('display_statement.html',transactions = transactions)
				else:
					flash("No transactions found between the specified dates", 'danger')
					return redirect(url_for('account_statement'))
		else:
			return redirect(url_for('login'))
	else:
		return redirect(url_for('login'))


@app.route('/withdraw_money',methods=['POST'])
def withdraw_money():
	msg = ''
	if request.method == 'POST' and 'w_amount' in request.form:
		cust_id = request.form['cid']
		acc_id = request.form['aid']
		acc_type = request.form['a_type']
		bal = request.form['balance']
		amt = request.form['w_amount']
		ts = datetime.utcnow()
		try:
			t_amt = int(bal) - int(amt)
			if(t_amt<=1000):
				msg="Please maintain a minimum balance of 1000"
			else:
				cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
				cursor.execute('INSERT INTO transactions (customer_id, account_id, description, acc_type, amount) VALUES (%s, %s, %s, %s, %s)',
					(cust_id, acc_id, 'withdraw', acc_type, amt))
				cursor.execute('UPDATE account SET balance = %s, message = %s, last_updated = %s WHERE account_id = %s and status = 1',
					(t_amt, 'amount withdrawn successfully', ts, acc_id))
				mysql.connection.commit()
				flash('Amount withdrawn successfully', 'success')
				return redirect(url_for('display_search_account',account_id=acc_id))
		except Exception as e:
			msg = 'could not withdraw money...Please try again'
	if 'loggedin' in session and session['type'] == 'cashier' and (
			'cid' and 'aid' and 'name' and 'a_type' and 'balance' in request.form):
		data = []
		data.append(request.form['cid'])
		data.append(request.form['aid'])
		data.append(request.form['name'])
		data.append(request.form['a_type'])
		data.append(request.form['balance'])
		return render_template('withdraw_money.html', username=session['username'], emp_type=session['type'], msg=msg,data=data)
	return redirect(url_for('login'))


