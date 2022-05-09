from base64 import b64encode
from datetime import timedelta
import html


from flask import Flask, render_template, request, redirect, session
import pymysql

app = Flask(__name__)  # starting a flask app
# Set session exipiry lifetime if not in use
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=5)

app.secret_key = 'opoojm_5#y2L"F4Q8z\n\xec]/'


# activate HTTP only/secure to true
# activate samesite to 'Lax'
# This reduce chances of a Sessions Fixation/Hijacking

app.config.update(
    SESSION_COOKIE_SECURE=False,  # For it to work locally
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE='Lax'
)
# Home page route


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup', methods=['POST', 'GET'])
def sign_in():
    if request.method == 'POST':
        username = str(request.form['username'])
        fullname = str(request.form['fullname'])
        email = str(request.form['email'])
        password = str(request.form['password'])
        password_again = str(request.form['password-again'])

        if password != password_again:
            return render_template('register-m.html', msg="Passwords do not match")
        else:
            conn = pymysql.connect(
                host='localhost',
                user='root',
                password="",
                db='webDoc',
            )
            sql = "INSERT INTO `users`(`username`, `fullname`, `email`, `password`) VALUES (%s, %s, %s, %s)"
            cursor = conn.cursor()
            cursor.execute(sql, (username, fullname, email, password))
            conn.commit()

            session['username'] = username
            session['role'] = "user"
            session.permanent = True
            return redirect('/')
        

    else:
        return redirect('/')

@app.route('/admin-dasboard')
def admin_dasboard():
    if session.get("role") == "admin":
        return render_template('admin-panel.html')
    else:
        return redirect('/')

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = str(request.form['username'])
        password = str(request.form['password'])

        passw_conn = pymysql.connect(
                host='localhost',
                user='root',
                password="",
                db='webDoc',
            )
        userPasswordFromDb = "SELECT password FROM users WHERE username =%s"
        pass_cursor = passw_conn.cursor()
        pass_cursor.execute(userPasswordFromDb, username)


        if pass_cursor.rowcount > 0:
            session['username'] = username
            session['role'] = "user"
            session.permanent = True
            return redirect('/')

        elif username == 'admin' and password == 'spacecadet':
            session['username'] = username
            session['role'] = "admin"
            session.permanent = True
            return redirect('/admin-dasboard')
            
        else:
           return render_template('index.html', msg="Invalid username or password")

    else:
        return redirect('/')

@app.route('/add-hospital')
def add_hospital():
    if session.get("role") == "admin":
        return render_template('add-hospital.html')
    else:
        return index()

@app.route('/add-doctor')
def add_doctor():
    if session.get("role") == "admin":
        return render_template('add-private-doc.html')
    else:
        return index()

@app.route('/update-hopital', methods=['POST', 'GET'])
def update_hopital():
    if request.method == 'POST' and session.get("role") == "admin":
        name = str(request.form['name'])
        location = str(request.form['location'])
        phoneno = str(request.form['phoneno'])
        email = str(request.form['email'])
        password = str(request.form['password'])
        services = str(request.form['services'])
        ambulance = str(request.form['ambulance'])
        photo = request.files['photo']
        ambulancePhoto = request.files['ambulance-pic']

        readimage = photo.read()  # read the image file data, the real image
        readimage2 = ambulancePhoto.read()
        # encode image to base64 and decode to utf-8
        encodedimage = b64encode(readimage).decode("utf-8")
        encodedimage2 = b64encode(readimage2).decode("utf-8")


        update_conn = pymysql.connect(
                host='localhost',
                user='root',
                password="",
                db='webDoc',
            )

        sql = "INSERT INTO `hospital`(`name`, `location`, `phoneno`, `email`, `password`, `services`, `ambulance`, `photo`, `ambulancePhoto`) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        update_cursor =  update_conn.cursor()
        update_cursor.execute(sql, (name, location, phoneno, email, password, services, ambulance, encodedimage, encodedimage2))
        update_conn.commit()

        msg = "Successfully added " + name + " to the database."
        return render_template('admin-panel.html', msg=msg)
    
    else:
        return redirect('/admin-dasboard')

@app.route('/all-hospitals')
def all_hosp():
    if session.get("role") == "admin":
        allHospitalConn = pymysql.connect(
            host='localhost',
            user='root',
            password='',
            db='webDoc'
        )

        sql = "SELECT `name`, `location`, `phoneno`, `email`, `password`, `services`, `ambulance`, `photo`, `ambulancePhoto`, `ratings` FROM `hospital` WHERE 1"
        allHospitalCursor = allHospitalConn.cursor()
        allHospitalCursor.execute(sql)

        if allHospitalCursor.rowcount == 0:
            return render_template('adminResults.html', msg="No hospital registered yet")
        else:
            rows = allHospitalCursor.fetchall()
            return render_template('adminResults.html', rows=rows, msg="These are the available hospitals")
    else:
        return redirect('/')


@app.route('/remove-hospital', methods=['POST', 'GET'])    
def remove_hospital():
    name = str(request.form['name'])

    conn = pymysql.connect(
                host='localhost',
                user='root',
                password="",
                db='webDoc',
            )

    sql = "DELETE FROM `hospital` WHERE name = %s"
    remove_cursor = conn.cursor()
    remove_cursor.execute(sql, name)
    conn.commit()
    return redirect('/all-hospitals')


@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('role', None)
    return redirect('/')


# run
if __name__ == '__main__':
    app.run(debug=True, port=4000)
# port = 10000
print(session.photo)