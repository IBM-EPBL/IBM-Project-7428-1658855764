from flask import Flask,render_template,request,session,redirect
import ibm_db
import jinja2
import re
from markupsafe import escape
from flask_mail import Mail, Message
import smtplib

conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=ea286ace-86c7-4d5b-8580-3fbfa46b1c66.bs2io90l08kqb1od8lcg.databases.appdomain.cloud;PORT=31505;SECURITY=SSL;SSLServerCertificate=env/DigiCertGlobalRootCA.crt;UID=ysy09691;PWD=wRGtNb3HWCEu0j4T",'','')

global total

global t_food 

global t_entertainment 

global t_business 

global t_rent

global t_EMI

global t_other 


    
print(conn)
print("connection successful...")
app = Flask(__name__)

app.secret_key = 'a'




#HOME--PAGE
@app.route("/")
def home():
   
     
    return render_template("home.html")
 

@app.route('/signup',methods=['GET','POST'])
def signup():
    if request.method=='POST':
        username=request.form['username']
        email=request.form['email']
        password=request.form['password']
        phoneno=request.form['phoneno']
        gender=request.form['sex']
        age=request.form['age']
        job=request.form['job']
        sql="SELECT * FROM SIGNUP WHERE NAME=?"
        stmt=ibm_db.prepare(conn,sql)
        ibm_db.bind_param(stmt,1,username)
        ibm_db.execute(stmt)
        account=ibm_db.fetch_assoc(stmt)
        if account:
            print(username)
            return render_template('signup.html',msg="this name is already inserted")
           
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'name must contain only characters and numbers !'
        else:
            insert_sql="INSERT INTO SIGNUP VALUES (?,?,?,?,?,?,?)"
            prep_stmt=ibm_db.prepare(conn,insert_sql)
            ibm_db.bind_param(prep_stmt,1,username)
            ibm_db.bind_param(prep_stmt,2,email)
            ibm_db.bind_param(prep_stmt,3,password)
            ibm_db.bind_param(prep_stmt,4,phoneno)
            ibm_db.bind_param(prep_stmt,5,gender)
            ibm_db.bind_param(prep_stmt,6,age)
            ibm_db.bind_param(prep_stmt,7,job)
            ibm_db.execute(prep_stmt)
            msg = 'You have successfully registered !'
            return render_template('home.html',msg=msg)
    
    elif request.method=='GET':
        return render_template("signup.html")

@app.route("/signin")
def signin():
    return render_template("login.html")


@app.route('/login',methods=['GET','POST'])
def login():
    global userid
    msg = ''
    if request.method=='POST':
        email=request.form['Email']
        password=request.form['password']
        sql = "SELECT * FROM SIGNUP WHERE EMAIL=? AND PASSWORD=?"
        stmt = ibm_db.prepare(conn,sql)
        ibm_db.bind_param(stmt,1,email)
        ibm_db.bind_param(stmt,2,password)
        ibm_db.execute(stmt)
        dic = ibm_db.fetch_assoc(stmt)
        
        print(dic)
        if dic:
            session['loggedin'] = True
            session['id'] = dic['NAME']
            userid=  dic['NAME']
            session['username'] = dic['EMAIL']
            print(session['id'])
            print(session['username'])
            print(userid)
           
            return render_template("homepage.html")
        else:
            msg = 'Incorrect username / password !'
    return render_template("login.html", msg = msg)

@app.route("/add")
def adding():
    return render_template("add.html")

@app.route("/addexpense",methods=['GET','POST'])
def add():
    
    date = request.form['date']
    expensename = request.form['expensename']
    amount = request.form['amount']
    paymode = request.form['paymode']
    category = request.form['category']

    insert_sql="INSERT INTO DAILYEXPENSE (USERNAME,DATE,EXPENSENAME,EXPENSEAMOUNT,PAYMENTMODE,CATEGORY) VALUES (?,?,?,?,?,?)"
    prep_stmt=ibm_db.prepare(conn,insert_sql)
    
    ibm_db.bind_param(prep_stmt,1,session['id'])
    ibm_db.bind_param(prep_stmt,2,date)
    ibm_db.bind_param(prep_stmt,3,expensename)
    ibm_db.bind_param(prep_stmt,4,amount)
    ibm_db.bind_param(prep_stmt,5,paymode)
    ibm_db.bind_param(prep_stmt,6,category)
   
    ibm_db.execute(prep_stmt)
    # limit=f"SELECT EXPENSEAMOUNT FROM DAILYEXPENSE WHERE USERNAME='{escape(session['id'])}'"
    # dic= ibm_db.fetch_tuple(prep_stmt)
    # stmt1= ibm_db.exec_immediate(conn,sql)
    # print(dic)
    # print(dic[4])
    return redirect("/display")
   
# @app.route("/sendgrid")
# def sengrid():



@app.route("/display")
def history():
    expense = []
    sql = f"SELECT * FROM DAILYEXPENSE WHERE USERNAME='{session['id']}'" 

    stmt1= ibm_db.exec_immediate(conn,sql)
    print(stmt1)
   
    dictionary = ibm_db.fetch_both(stmt1)
    print(dictionary)
    print(session["username"],session['id'])
    while dictionary != False:
     expense.append(dictionary)
     dictionary = ibm_db.fetch_both(stmt1)
    expense1=[]
    sql1=f"SELECT * FROM DAILYEXPENSE WHERE USERNAME = '{escape(session['id'])}'"
    stmt= ibm_db.exec_immediate(conn,sql1)
    dictionary1 = ibm_db.fetch_both(stmt)
    print(dictionary1)
    while dictionary1!=False:
         expense1.append(dictionary1)
         dictionary1= ibm_db.fetch_both(stmt)
    print(expense1)
    total=0
    t_food=0
    t_entertainment=0
    t_business=0
    t_rent=0
    t_EMI=0
    t_other=0
 
    for x in expense1:
          print(x["EXPENSEAMOUNT"])
          total =total+ int(x["EXPENSEAMOUNT"])
          if x["CATEGORY"] == "food":
              t_food=t_food+int(x["EXPENSEAMOUNT"])
            
          elif x["CATEGORY"] == "entertainment":
              t_entertainment  += int(x["EXPENSEAMOUNT"])
        
          elif x["CATEGORY"] == "business":
              t_business  +=int(x["EXPENSEAMOUNT"])
          elif x["CATEGORY"]  == "rent":
              t_rent  += int(x["EXPENSEAMOUNT"])
           
          elif x["CATEGORY"] == "EMI":
              t_EMI  += int(x["EXPENSEAMOUNT"])
         
          elif x["CATEGORY"]  == "other":
              t_other  += int(x["EXPENSEAMOUNT"])
            
    print(total)
    sql2="SELECT MONTHAMOUNT FROM  LIMITS  ORDER BY LIMITID DESC LIMIT 1"
    stmt = ibm_db.exec_immediate(conn, sql2)
    limit = ibm_db.fetch_tuple(stmt)
    alert=int(limit[0])-total
    print(alert)
    if alert<=0:
        sender_email="jayaprakash291029@gmail.com"
        rec_email=session['username']
        password='xtbrhwpqbdbxyjir'
        message='ALERT MESSAGE FROM EXPENSE TRACKER !PLEASE CHECK  YOUR DAILY EXPENSE YOUR DAILY EXPENSE IS CROSS YOUR MONTHLY LIMIT. UPDATE YOUR MONTHLY LIMIT AND AVOID YOUR UNWANTED DAILY EXPENSE'
        # soup=BeautifulSoup(html_data,'html.parser')      
        print(message)
        server=smtplib.SMTP('smtp.gmail.com',587)
        server.starttls()
        server.login(sender_email,password)
        print("login successfully")
        server.sendmail(sender_email,rec_email,message)
        print("emaail has been sende successfully")
   

    if expense:
        # return redirect("/sendgrid/{{expense}}")
        return render_template("display.html",expense=expense, total = total ,
                           t_food = t_food,t_entertainment =  t_entertainment,
                           t_business = t_business,  t_rent =  t_rent, 
                           t_EMI =  t_EMI,  t_other = t_other)

# @app.route("/sendgrid/<expense>")
# def sengrid(expense):
#       expense1=[]
#       sql1=f"SELECT * FROM DAILYEXPENSE WHERE USERNAME = '{escape(session['id'])}'"
#       stmt= ibm_db.exec_immediate(conn,sql1)
#       dictionary1 = ibm_db.fetch_both(stmt)
#       print(dictionary1)
#       while dictionary1!=False:
#          expense1.append(dictionary1)
#          dictionary1= ibm_db.fetch_both(stmt)
#       print(expense)
#       return render_template("display.html",expense=expense)
     
@app.route("/edit/<userid>", methods = ['POST', 'GET' ])
def edit(userid):
    edit=[]
    print(userid)
    userid=userid
    sql=f"SELECT * FROM DAILYEXPENSE WHERE  USERID ={userid}"
    
    stmt1= ibm_db.exec_immediate(conn,sql)
  
    print(stmt1)
    dic= ibm_db.fetch_tuple(stmt1)
    
    print(userid)
    print(edit)
    return render_template("edit.html",dic=dic,userid=dic[0])

@app.route('/update/<name>/<userid>',methods=['GET','POST'])
def update(name,userid):
    if request.method=='POST':
     
      print(userid)
      date = request.form['date']
      expensename = request.form['expensename']
      amount = request.form['expenseamount']
      paymode= request.form['paymentmode']
      category = request.form['category']
      sql = f"SELECT * FROM DAILYEXPENSE WHERE USERNAME='{escape(name)}'"
      print(sql)
      stmt = ibm_db.exec_immediate(conn, sql)
      student = ibm_db.fetch_row(stmt)
      print ("The Name is : ",  student)
      if student:
         sql= f"UPDATE DAILYEXPENSE SET DATE =? , EXPENSENAME =?, EXPENSEAMOUNT = ? , PAYMENTMODE =?, CATEGORY = ?  WHERE  USERID ={escape(userid)} "
         print(sql)
         stmt1=ibm_db.prepare(conn,sql)  
      
         ibm_db.bind_param(stmt1,1,date)
         ibm_db.bind_param(stmt1,2,expensename)
         ibm_db.bind_param(stmt1,3,amount)
         ibm_db.bind_param(stmt1,4,paymode)
         ibm_db.bind_param(stmt1,5,category)

      
         ibm_db.execute(stmt1)
      
         expense = []
         sql = "SELECT * FROM DAILYEXPENSE"
         stmt = ibm_db.exec_immediate(conn, sql)
         dictionary = ibm_db.fetch_both(stmt)
         while dictionary != False:
          expense.append(dictionary)
          dictionary = ibm_db.fetch_both(stmt)
         if expense:
            print(dictionary)
            return redirect("/display")
   
  
@app.route('/delete/<name>/<userid>')
def delete(name,userid):
  sql = f"SELECT * FROM DAILYEXPENSE WHERE USERNAME='{escape(name)}'"
  print(sql)
  stmt = ibm_db.exec_immediate(conn, sql)
  student = ibm_db.fetch_row(stmt)
  print ("The Name is : ",  student)
  if student:
    sql = f"DELETE FROM DAILYEXPENSE WHERE USERID={escape(userid)}"
    print(sql)
    stmt = ibm_db.exec_immediate(conn, sql)

    expense = []
    sql = "SELECT * FROM DAILYEXPENSE"
    stmt = ibm_db.exec_immediate(conn, sql)
    dictionary = ibm_db.fetch_both(stmt)
    while dictionary != False:
      expense.append(dictionary)
      dictionary = ibm_db.fetch_both(stmt)
    if expense:
      return redirect("/display")

@app.route("/limit")
def limit():
    
    return redirect("/limitln")

@app.route("/limit1",methods=['GET','POST'])
def setlimit():
      if request.method=='POST':
        #  limit=[]
         limitamount = request.form['limitamount']
         
         month = request.form['month']
         sql="INSERT INTO LIMITS (USERNAME,MONTHAMOUNT,MONTH) VALUES (?,?,?) "
         print(sql)
         stmt1=ibm_db.prepare(conn,sql)  
      
         ibm_db.bind_param(stmt1,1,session['id'])
         ibm_db.bind_param(stmt1,2,limitamount)
         ibm_db.bind_param(stmt1,3,month)
         ibm_db.execute(stmt1)
         print('successfully inserted')
         return redirect("/limitln")
        
@app.route("/limitln")
def limitln():
      sql="SELECT MONTHAMOUNT FROM  LIMITS  ORDER BY LIMITID DESC LIMIT 1"
      stmt = ibm_db.exec_immediate(conn, sql)
      limit = ibm_db.fetch_tuple(stmt)
      print("successfully executed")
      return render_template("limit.html",amount=limit[0])

@app.route("/today/<name>")
def today(name):
     
      print(name)
      texpense=[]
      expense=[]
      sql= f"SELECT DATE(date), SUM(EXPENSEAMOUNT) FROM DAILYEXPENSE WHERE USERNAME='{escape(name)}' AND DATE(DATE)=DATE(current timestamp)  GROUP BY DATE(date) ORDER BY DATE(date) "
      stmt1= ibm_db.exec_immediate(conn,sql)
      dictionary = ibm_db.fetch_both(stmt1)
      print(dictionary)
      while dictionary!=False:
        texpense.append(dictionary)
        dictionary = ibm_db.fetch_both(stmt1)
       
      print(texpense)
      sql1=f"SELECT * FROM DAILYEXPENSE WHERE USERNAME = '{escape(name)}'"
      stmt= ibm_db.exec_immediate(conn,sql1)
      dictionary1 = ibm_db.fetch_both(stmt)
      print(dictionary1)
      while dictionary1!=False:
         expense.append(dictionary1)
         dictionary1= ibm_db.fetch_both(stmt)
      print(expense)
      total=0
      t_food=0
      t_entertainment=0
      t_business=0
      t_rent=0
      t_EMI=0
      t_other=0
 
     
      for x in expense:
          print(x["EXPENSEAMOUNT"])
          total =total+ int(x["EXPENSEAMOUNT"])
          if x["CATEGORY"] == "food":
              t_food=t_food+int(x["EXPENSEAMOUNT"])
            
          elif x["CATEGORY"] == "entertainment":
              t_entertainment  += int(x["EXPENSEAMOUNT"])
        
          elif x["CATEGORY"] == "business":
              t_business  +=int(x["EXPENSEAMOUNT"])
          elif x["CATEGORY"]  == "rent":
              t_rent  += int(x["EXPENSEAMOUNT"])
           
          elif x["CATEGORY"] == "EMI":
              t_EMI  += int(x["EXPENSEAMOUNT"])
         
          elif x["CATEGORY"]  == "other":
              t_other  += int(x["EXPENSEAMOUNT"])
            
      print(total)
        
      print(t_food)
      print(t_entertainment)
      print(t_business)
      print(t_rent)
      print(t_EMI)
      print(t_other)
      print(texpense)
      print(expense)

     
      return render_template("today.html", texpense = texpense, expense = expense,  total = total ,
                           t_food = t_food,t_entertainment =  t_entertainment,
                           t_business = t_business,  t_rent =  t_rent, 
                           t_EMI =  t_EMI,  t_other =  t_other )

@app.route("/month/<name>")
def month(name):
      
      texpense=[]
      expense=[]
      sql= f"SELECT DATE(date), SUM(EXPENSEAMOUNT) FROM DAILYEXPENSE WHERE USERNAME='{escape(name)}' AND MONTH(DATE)=MONTH(current timestamp)  GROUP BY DATE(date) ORDER BY DATE(date) "
      stmt1= ibm_db.exec_immediate(conn,sql)
      dictionary = ibm_db.fetch_both(stmt1)
      print(dictionary)
      while dictionary!=False:
        texpense.append(dictionary)
        dictionary = ibm_db.fetch_both(stmt1)
       
      print(texpense)
      sql1=f"SELECT * FROM DAILYEXPENSE WHERE USERNAME = '{escape(name)}'"
      stmt= ibm_db.exec_immediate(conn,sql1)
      dictionary1 = ibm_db.fetch_both(stmt)
      print(dictionary1)
      while dictionary1!=False:
         expense.append(dictionary1)
         dictionary1= ibm_db.fetch_both(stmt)
      print(expense)
      total=0
      t_food=0
      t_entertainment=0
      t_business=0
      t_rent=0
      t_EMI=0
      t_other=0
 
     
      for x in expense:
          print(x["EXPENSEAMOUNT"])
          total =total+ int(x["EXPENSEAMOUNT"])
          if x["CATEGORY"] == "food":
              t_food=t_food+int(x["EXPENSEAMOUNT"])
            
          elif x["CATEGORY"] == "entertainment":
              t_entertainment  += int(x["EXPENSEAMOUNT"])
        
          elif x["CATEGORY"] == "business":
              t_business  +=int(x["EXPENSEAMOUNT"])
          elif x["CATEGORY"]  == "rent":
              t_rent  += int(x["EXPENSEAMOUNT"])
           
          elif x["CATEGORY"] == "EMI":
              t_EMI  += int(x["EXPENSEAMOUNT"])
         
          elif x["CATEGORY"]  == "other":
              t_other  += int(x["EXPENSEAMOUNT"])
            
      print(total)
        
      print(t_food)
      print(t_entertainment)
      print(t_business)
      print(t_rent)
      print(t_EMI)
      print(t_other)
      print(texpense)
      print(expense)

     
      return render_template("month.html", texpense = texpense, expense = expense,  total = total ,
                           t_food = t_food,t_entertainment =  t_entertainment,
                           t_business = t_business,  t_rent =  t_rent, 
                           t_EMI =  t_EMI,  t_other =  t_other )
      

@app.route("/year/<name>")
def year(name):
      print(name)
      texpense=[]
      expense=[]
      sql= f"SELECT DATE(date), SUM(EXPENSEAMOUNT) FROM DAILYEXPENSE WHERE USERNAME='{escape(name)}' AND YEAR(DATE)=YEAR(current timestamp)  GROUP BY DATE(date) ORDER BY DATE(date) "
      stmt1= ibm_db.exec_immediate(conn,sql)
     
      dictionary = ibm_db.fetch_both(stmt1)
      print(dictionary)
      while dictionary!=False:
        texpense.append(dictionary)
        dictionary = ibm_db.fetch_both(stmt1)
       
      print(texpense)
      sql1=f"SELECT * FROM DAILYEXPENSE WHERE USERNAME = '{escape(name)}'"
      stmt= ibm_db.exec_immediate(conn,sql1)
      dictionary1 = ibm_db.fetch_both(stmt)
      print(dictionary1)
      while dictionary1!=False:
         expense.append(dictionary1)
         dictionary1= ibm_db.fetch_both(stmt)
      print(expense)
      total=0
      t_food=0
      t_entertainment=0
      t_business=0
      t_rent=0
      t_EMI=0
      t_other=0
 
     
      for x in expense:
          print(x["EXPENSEAMOUNT"])
          total =total+ int(x["EXPENSEAMOUNT"])
          if x["CATEGORY"] == "food":
              t_food=t_food+int(x["EXPENSEAMOUNT"])
            
          elif x["CATEGORY"] == "entertainment":
              t_entertainment  += int(x["EXPENSEAMOUNT"])
        
          elif x["CATEGORY"] == "business":
              t_business  +=int(x["EXPENSEAMOUNT"])
          elif x["CATEGORY"]  == "rent":
              t_rent  += int(x["EXPENSEAMOUNT"])
           
          elif x["CATEGORY"] == "EMI":
              t_EMI  += int(x["EXPENSEAMOUNT"])
         
          elif x["CATEGORY"]  == "other":
              t_other  += int(x["EXPENSEAMOUNT"])
            
      print(total)
        
      print(t_food)
      print(t_entertainment)
      print(t_business)
      print(t_rent)
      print(t_EMI)
      print(t_other)
      print(texpense)
      print(expense)
       
     
      return render_template("year.html", texpense = texpense, expense = expense,  total = total ,
                           t_food = t_food,t_entertainment =  t_entertainment,
                           t_business = t_business,  t_rent =  t_rent, 
                           t_EMI =  t_EMI,  t_other =  t_other )
      
@app.route("/homepage",methods=['GET','POST'])
def homepage():
  
      return render_template("homepage.html")

@app.route('/logout')

def logout():
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('username', None)
   return render_template('home.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000,debug=True)