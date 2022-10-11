
from flask import Flask,render_template,request
app=Flask(__name__)

#HOME--PAGE
@app.route("/home")
def home():
    return render_template("homepage.html")

@app.route("/")
def add():
    return render_template("home.html")


#SIGN--UP--OR--REGISTER
@app.route("/signup")
def signup():
    return render_template("signup.html")
@app.route('/register',methods=['GET','POST'])
def Register():
    if request.method=='POST':
        username=request.form['username']
        password=request.form['password']
        if username =='root' and password=='root':
          return render_template('login.html')
        else:
         return render_template('signup.html')
    else:
        return render_template('signup.html')


@app.route("/signin")
def signin():
    return render_template("login.html")


@app.route('/login',methods=['GET','POST'])
def login():
    if request.method=='POST':
        username=request.form['username']
        password=request.form['password']
        if username =='root' and password=='root':
          return render_template('home.html')
        else:
         return render_template('login.html')
    else:
        return render_template('login.html')


if __name__=="__main__":
    app.run(debug=True)