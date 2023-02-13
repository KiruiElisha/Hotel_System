from flask import Flask,render_template,request,redirect,session
import pymysql
from cryptography.fernet import Fernet
from datetime import timedelta


def app_key():
    key = Fernet.generate_key()
    with open("key.key", "wb") as key_file:
        key_file.write(key)

def load_key():
    return open("key.key", "rb").read()

key = load_key()
f = Fernet(key)

app = Flask(__name__)

app.secret_key = 'RO&&NO$%£ELIS"""HA%%123**45678'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta (minutes = 2)

app.config.update(
    SESSION_COOKIE_SECURE=True,
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE='Lax'

)
@app.route('/', methods=['POST','GET'])
def index():
    if "username" in session:

        if request.method=='POST':
            idNumber = int(request.form['idNumber'])
            username = str(request.form['username'])
            password = str(request.form['password'])
            email = str(request.form['email'])
            location= str(request.form['location'])
            phone = str(request.form['phone'])
            #connecting to the database




            connection= makeConnection()
            cursor=connection.cursor()

            sql = "insert into registration(idNumber,username,password,email,location,phone)values(%s,%s,%s,%s,%s,%s)"

            try:
                #this code will be executed if server is found
                cursor.execute(sql,(idNumber,username,password,email,location,phone))

                connection.commit()
                if cursor.rowcount == 1:
                    return render_template("registration.html", msg="Registration Successful")

                else:
                    return render_template("registration.html", msg="username already in use")


            except:
                connection.rollback()
            return render_template("registration.html",msg="Registration Failed! Server not found")
        else:
            return render_template("registration.html")
    else:
        return redirect("/login")

@app.route('/checkin', methods=['POST','GET'])
def checkin():
    if "username" in session:

        if request.method=='POST':
            fname = str(request.form['fname'])
            email = str(request.form['email'])
            phone = str(request.form['phone'])
            nationality = str(request.form['nationality'])
            address = str(request.form['address'])
            checkin_date = str(request.form['checkin_date'])
            checkin_time = str(request.form['checkin_time'])
            room_no = str(request.form['room_no'])
            checkout_date = str(request.form['checkout_date'])

            connection = makeConnection()
            cursor=connection.cursor()
            sql= "insert into check_in(fname,email,phone,nationality,address,checkin_date,checkin_time,room_no,checkout_date)values(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            try:
                #this code will be executed if server is found
                cursor.execute(sql,(fname,email,phone,nationality,address,checkin_date,checkin_time,room_no,checkout_date))
                connection.commit()
                return render_template("checkin.html", msg="checkin Successful")
            except:
                connection.rollback()
                return render_template("checkin.html",msg="checkin fail! Server not found")
        else:
            return render_template("checkin.html")
    else:
        return redirect("/login")

@app.route('/view_registration')
def view_registration():
    if "username" in session:

        con = makeConnection()
        cur = con.cursor()
        sql = "select * from registration "
        cur.execute(sql)
        if cur.rowcount < 1:
            return render_template("view_registration.html", msg="No records found")
        else:
            return render_template("view_registration.html", rows=cur.fetchall())
    else:
        return redirect("/login")

@app.route('/view_checkin')
def view_checkin():
    if "username" in session:

        con=makeConnection()
        cur=con.cursor()
        sql="select * from check_in "
        cur.execute(sql)
        if cur.rowcount<1:
            return render_template("view_checkin.html",msg="No records found")
        else:
            return render_template("view_checkin.html",rows=cur.fetchall())
    else:
        return redirect("/login")



@app.route('/search',methods=['POST','GET'])
def search():
    if "username" in session:

        if request.method=="POST":
            phone=int(request.form['phone'])
            con=makeConnection()
            cur = con.cursor()
            sql="select * from check_in where phone=%s"

            cur.execute(sql,(phone))
            if cur.rowcount==0:
                return  render_template("search.html",msg="No user was found")
            elif cur.rowcount==1:
                #session['phone']=phone
                return render_template("search.html",rows=cur.fetchall())

            elif cur.rowcount>1:
                return render_template("search.html",msg="Multiple users found: can't proceed")
        else:
            return render_template("search.html")
    else:
        return redirect("/login")
@app.route('/login', methods=['POST','GET'])
def login():
    if request.method=="POST":
        username=str(request.form['username'])
        password = str(request.form['password'])
        con=makeConnection()
        cur = con.cursor()
        sql="select username, password from registration where username=%s and password=%s"
        cur.execute(sql,(username,password))
        if cur.rowcount==0:
            return  render_template("login.html",msg="No user was found by that name")
        elif cur.rowcount==1:
            session['username']=username
            session.permanent=True
            return redirect('/')
        elif cur.rowcount>1:
            return render_template("login.html",msg="Multiple users found: can't proceed")
    else:
        return render_template("login.html")



def makeConnection():
    return pymysql.connect(host='127.0.0.1',user='root',passwd='root',db='hotel_management_systemm')


# def makeConnection():
#     return pymysql.connect("127.0.0.1","root","","")


if __name__ =="__main__":
    app.run(debug=True)