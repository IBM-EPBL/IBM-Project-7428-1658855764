from flask import Flask,render_template,request
import ibm_db

conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=ea286ace-86c7-4d5b-8580-3fbfa46b1c66.bs2io90l08kqb1od8lcg.databases.appdomain.cloud;PORT=31505;SECURITY=SSL;SSLServerCertificate=D:\Education\Assignment\env\DigiCertGlobalRootCA.crt;UID=ysy09691;PWD=wRGtNb3HWCEu0j4T",'','')

print(conn)

print("connection successful...")
app = Flask(__name__)




@app.route('/')
def home():
    return render_template("home.html")

@app.route('/login',methods=['POST','GET'])
def login():
    if request.method=='POST':
        email = request.form['email']
        password = request.form['password']
        sql = "SELECT * FROM User WHERE EMAIL=? AND PASSWORD=?"
        stmt = ibm_db.prepare(conn,sql)
        ibm_db.bind_param(stmt,1,email)
        ibm_db.bind_param(stmt, 2, password)
        ibm_db.execute(stmt)
        dic = ibm_db.fetch_assoc(stmt)
        print(dic)
        if dic:
            return render_template('home.html')
        else:
            return render_template('login.html')
        
   
    elif request.method=='GET':
        return render_template('login.html')

@app.route('/signup',methods=['POST','GET'])
def signup():
    if request.method=='POST':
        name=request.form['username']
        password=request.form['password']
        email=request.form['email']
        rollno=request.form['roll_no']
               
        sql="SELECT * FROM USER WHERE ROLLNO=?"
        stmt=ibm_db.prepare(conn,sql)
        ibm_db.bind_param(stmt,1,rollno)
        ibm_db.execute(stmt)
        account=ibm_db.fetch_assoc(stmt)

        if account:
            print(rollno)
            return render_template('signup.html',msg="this data is already inserted")
        else:
            print(name)
            insert_sql="INSERT INTO USER VALUES (?,?,?,?)"
            prep_stmt=ibm_db.prepare(conn,insert_sql)
            ibm_db.bind_param(prep_stmt,1,name)
            ibm_db.bind_param(prep_stmt,2,email)
            ibm_db.bind_param(prep_stmt,3,password)
            ibm_db.bind_param(prep_stmt,4,rollno)
            ibm_db.execute( prep_stmt)
            return render_template('home.html',msg="user data inserted successfully")

    elif request.method=='GET':
        return render_template('signup.html')

   



if __name__=='__main__':
    app.run(debug = True)