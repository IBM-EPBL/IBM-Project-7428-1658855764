
from flask import Flask,render_template,request
import ibm_db

conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=ea286ace-86c7-4d5b-8580-3fbfa46b1c66.bs2io90l08kqb1od8lcg.databases.appdomain.cloud;PORT=31505;SECURITY=SSL;SSLServerCertificate=./DigiCertGlobalRootCA.crt;UID=ysy09691;PWD=wRGtNb3HWCEu0j4T",'','')

print(conn)
print("connection successful...")
app = Flask(__name__)

#HOME--PAGE


@app.route("/")
def home():
    return render_template("home.html")


#SIGN--UP--OR--REGISTER
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
        else:
            print(username)
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
            return render_template('home.html',msg="user data inserted successfully")
    
    elif request.method=='GET':
        return render_template("signup.html")

@app.route("/signin")
def signin():
    return render_template("login.html")


@app.route('/login',methods=['GET','POST'])
def login():
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
            return render_template("homepage.html")
        else:
            return render_template("login.html")
    elif request.method=='GET':
        return render_template("login.html")
if __name__=="__main__":
    app.run(host='0.0.0.0',port=5000,debug=True)