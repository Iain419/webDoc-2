from base64 import b64encode
from datetime import timedelta
import html
from re import L
from time import time


from flask import Flask, render_template, request, redirect, session
import pymysql

app = Flask(__name__)  # starting a flask app
# Set session exipiry lifetime if not in use
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=50)

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
        userPasswordFromDb = "SELECT * FROM users WHERE username = %s AND password = %s"
        pass_cursor = passw_conn.cursor()
        pass_cursor.execute(userPasswordFromDb, (username, password))


        if pass_cursor.rowcount > 0:
            session['username'] = username
            session['role'] = "user"
            session.permanent = True
            return redirect(request.referrer)
        
        elif pass_cursor.rowcount == 0:
            sql = "SELECT * FROM hospital WHERE name = %s and password = %s"
            pass_cursor.execute(sql, (username, password))
            if pass_cursor.rowcount > 0:
                session['username'] = username
                session['role'] = "hospital"
                session.permanent = True
                return dasboard()
            elif pass_cursor.rowcount == 0:
                sql = "SELECT * FROM `privateDoctors` WHERE username = %s AND password = %s"
                pass_cursor.execute(sql, (username, password))
                if pass_cursor.rowcount > 0:
                    session['username'] = username
                    session['role'] = "doctor"
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

@app.route('/dasboard')
def dasboard():
    username = session.get('username')
    conn = pymysql.connect(
        host='localhost',
        user='root',
        password='',
        db='webDoc'
    )
    cursor = conn.cursor()

    if session.get("role") == "user":
        sql = "SELECT * FROM users where username = %s"
        cursor.execute(sql, username)
        rows = cursor.fetchall()
        return render_template('user-dash.html', rows=rows)

    elif session.get("role") == "hospital":
        sql = "SELECT * FROM hospital WHERE name = %s"
        cursor.execute(sql, username)
        rows = cursor.fetchall()
        return render_template('hospital-dash.html', rows=rows)

    elif session.get("role") == "doctor":
        sql = "SELECT * FROM `privateDoctors` WHERE username = %s"
        cursor.execute(sql, username)
        rows = cursor.fetchall()
        return render_template('private-doc.html', rows=rows)
    
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
        return redirect('/')

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

@app.route('/all-doctors')
def all_doctors():
    if session.get("role") == "admin":
        allHospitalConn = pymysql.connect(
            host='localhost',
            user='root',
            password='',
            db='webDoc'
        )

        sql = "SELECT name, location, phoneno, email, photo, specialist FROM privateDoctors WHERE 1"
        allHospitalCursor = allHospitalConn.cursor()
        allHospitalCursor.execute(sql)

        if allHospitalCursor.rowcount == 0:
            return render_template('adminResultsDoc.html', msg="No hospital registered yet")
        else:
            rows = allHospitalCursor.fetchall()
            return render_template('adminResultsDoc.html', rows=rows, msg="These are the available doctors")
    else:
        return redirect('/')


@app.route('/all-users')
def all_users():
    if session.get("role") == "admin":
        allHospitalConn = pymysql.connect(
            host='localhost',
            user='root',
            password='',
            db='webDoc'
        )

        sql = "SELECT fullname, email FROM users WHERE 1"
        allHospitalCursor = allHospitalConn.cursor()
        allHospitalCursor.execute(sql)

        if allHospitalCursor.rowcount == 0:
            return render_template('adminResultsuser.html', msg="No hospital registered yet")
        else:
            rows = allHospitalCursor.fetchall()
            return render_template('adminResultsuser.html', rows=rows, msg="These are the available users")
    else:
        return redirect('/')


@app.route('/remove-hospital', methods=['POST', 'GET'])    
def remove_hospital():
    if session.get("role") == "admin":
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
    else:
        return redirect('/')

@app.route('/remove-doctor', methods=['POST', 'GET'])    
def remove_doctor():
    if session.get("role") == "admin":
        name = str(request.form['name'])

        conn = pymysql.connect(
                    host='localhost',
                    user='root',
                    password="",
                    db='webDoc',
                )

        sql = "DELETE FROM `privateDoctors` WHERE name = %s"
        remove_cursor = conn.cursor()
        remove_cursor.execute(sql, name)
        conn.commit()
        return redirect('/all-doctors')
    else:
        return redirect('/')

@app.route('/remove-user', methods=['POST', 'GET'])    
def remove_user():
    if session.get("role") == "admin":
        name = str(request.form['name'])

        conn = pymysql.connect(
                    host='localhost',
                    user='root',
                    password="",
                    db='webDoc',
                )

        sql = "DELETE FROM users WHERE fullname = %s"
        remove_cursor = conn.cursor()
        remove_cursor.execute(sql, name)
        conn.commit()
        return redirect('/all-users')
    else:
        return redirect('/')




@app.route('/update-doctor', methods=['POST', 'GET'])
def update_doctor():
    if request.method == 'POST' and session.get("role") == "admin":
        username = str(request.form['username'])
        name = str(request.form['name'])
        location = str(request.form['location'])
        phoneno = str(request.form['phoneno'])
        email = str(request.form['email'])
        password = str(request.form['password'])
        photo = request.files['photo']
        

        readimage = photo.read()  # read the image file data, the real image
        # encode image to base64 and decode to utf-8
        encodedimage = b64encode(readimage).decode("utf-8")
    


        update_conn = pymysql.connect(
                host='localhost',
                user='root',
                password="",
                db='webDoc',
            )

        sql = "INSERT INTO `privateDoctors`(`username`, `name`, `location`, `phoneno`, `email`, `password`, `photo`) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        update_cursor =  update_conn.cursor()
        update_cursor.execute(sql, (username, name, location, phoneno, email, password, encodedimage,))
        update_conn.commit()

        msg = "Successfully added " + name + " to the database."
        return render_template('admin-panel.html', msg=msg)
    
    else:
        return redirect('/')
    
@app.route('/all-hospitals-available', methods=['POST', 'GET'])
def all_hosp_available(location = 'none'):
    allHospitalConn = pymysql.connect(
                    host='localhost',
                    user='root',
                    password='',
                    db='webDoc'
                )
    allHospitalCursor = allHospitalConn.cursor()

    if 'username' in session:
        username = session.get('username')
        sql = "SELECT `name`, `location`, `phoneno`, `email`, `password`, `services`, `ambulance`, `photo`, `ambulancePhoto`, hospital.ratings ,userratings.ratings FROM `hospital` LEFT JOIN userratings ON hospital.name = userratings.hospitalName WHERE `location` = %s OR userratings.username = %s"
    else:
        sql = "SELECT `name`, `location`, `phoneno`, `email`, `password`, `services`, `ambulance`, `photo`, `ambulancePhoto`, `ratings` FROM `hospital` WHERE `location` = %s"



    if location == 'none':
        location = str(request.form['location'])
        location = location.title()
        if 'username' in session:
            allHospitalCursor.execute(sql, (location, username))
        else:
            allHospitalCursor.execute(sql, location)

        if allHospitalCursor.rowcount == 0:
            return render_template('hospital-results.html', msg="Sorry we couldn't find any hospital near you")
        else:
            rows = allHospitalCursor.fetchall()
            return render_template('hospital-results.html', rows=rows)
    else:
        location = location.title()
        if 'username' in session:
            allHospitalCursor.execute(sql, (location, username))
        else:
            allHospitalCursor.execute(sql, location)

        if allHospitalCursor.rowcount == 0:
            return render_template('hospital-results.html', msg="Sorry we couldn't find any hospital near you")
        else:
            rows = allHospitalCursor.fetchall()
            return render_template('hospital-results.html', rows=rows)
        
        

@app.route('/rate', methods=['POST', 'GET'])
def rate():
    if request.method == "POST" and 'username' in session:
        hospitalName = str(request.form['name'])
        username = str(session.get("username"))
        rate = int(request.form['rate'])
        currentRatings = int(request.form['currentRatings'])
        location = str(request.form['location'])
        hospitalRatingsDb = currentRatings

        newRatings = (hospitalRatingsDb + rate)/2
        newRatings = round(newRatings, 2)

        conn2 = pymysql.connect(
                host='localhost',
                user='root',
                password='',
                db='webDoc'
            )
        
        newRatingsSql = "UPDATE hospital SET ratings = %s WHERE name = %s"
        newRatingsCursor = conn2.cursor()
        newRatingsCursor.execute(newRatingsSql, (newRatings, hospitalName))
        conn2.commit()

        conn3 = pymysql.connect(
                host='localhost',
                user='root',
                password='',
                db='webDoc'
            )
        
        userRatingsSql1 = "SELECT `username`, `hospitalName`, `ratings` FROM `userratings` WHERE username = %s AND hospitalName = %s"
        ratingsCursor = conn3.cursor()
        ratingsCursor.execute(userRatingsSql1, (username, hospitalName))

        if ratingsCursor.rowcount == 0:
            sql = "INSERT INTO `userratings`(`username`, `hospitalName`, `ratings`) VALUES (%s, %s, %s)"
            cursor = conn3.cursor()
            cursor.execute(sql, (username, hospitalName, newRatings))
            conn3.commit()
            return all_hosp_available(location)


        else:
            sql = "UPDATE `userratings` SET ratings = %s WHERE hospitalName = %s"
            cursor = conn3.cursor()
            cursor.execute(sql, (newRatings, hospitalName))
            conn3.commit()
            return all_hosp_available(location)
    else:
        return redirect(request.referrer)

@app.route('/all-ambulance', methods=['POST', 'GET'])
def all_ambulance():
    if request.method == 'POST':
        location = str(request.form['location'])
        location = location.title()
        conn = pymysql.connect(
                host='localhost',
                user='root',
                password='',
                db='webDoc'
        )

        sql = "SELECT `name`,`location`,`phoneno`,`ambulancePhoto`,`ratings` FROM `hospital` WHERE `location` = %s AND `ambulance` = 'yes'"
        cursor = conn.cursor()
        cursor.execute(sql, location)

        if cursor.rowcount == 0:
            return render_template('ambulance-results.html', msg="No ambulance registered yet")
        else:
            rows = cursor.fetchall()
            return render_template('ambulance-results.html', rows=rows, msg="These are the available ambulance")

    
    else:
        return redirect('/')


@app.route('/private-doc', methods=['POST', 'GET'])
def private_doc():
    if 'username' in session and request.method == 'POST':
        location = str(request.form['location'])
        location = location.title()
        conn = pymysql.connect(
            host='localhost',
            user='root',
            password='',
            db='webDoc'
        )
        cursor = conn.cursor()
        sql = "SELECT name, location, phoneno, email, photo, specialist FROM privateDoctors WHERE location = %s"
        cursor.execute(sql, location)
        if cursor.rowcount == 0:
            return render_template('doctor-results.html', msg="Sorry no doctors were found within this region")
        else:
            rows = cursor.fetchall()
            return render_template('doctor-results.html', rows=rows)
    else:
        return render_template('index.html', msg="You must be logged in to view the private doctors")
        


@app.route('/dashboard-update', methods=['POST', 'GET'])
def dashboard_update():
    intial_username = session.get("username")

    conn = pymysql.connect(
        host='localhost',
        user='root',
        password='',
        db='webDoc'
    )
    cursor = conn.cursor()

    if request.method == 'POST' and session.get("role") == "user":
        username = str(request.form['username'])
        fullname = str(request.form['fullname'])
        email = str(request.form['email'])
        password = str(request.form['password'])

        sql = "UPDATE users SET username = %s, fullname = %s, email = %s, password=%s WHERE username = %s"
        cursor.execute(sql, (username, fullname, email, password, intial_username))
        conn.commit()
        return logout()

    elif request.method == 'POST' and session.get('role') == "hospital":
        name = str(request.form['name'])
        location = str(request.form['location'])
        phoneno = str(request.form['phoneno'])
        email = str(request.form['email'])
        password = str(request.form['password'])
        services = str(request.form['services'])
        ambulance = str(request.form['ambulance'])
        photo = request.files['photo']
        ambulancePhoto = request.files['ambulancePhoto']

        readimage = photo.read()  
        readimage2 = ambulancePhoto.read()

        encodedimage = b64encode(readimage).decode("utf-8")
        encodedimage2 = b64encode(readimage2).decode("utf-8")

        sql = "UPDATE `hospital` SET `name`=%s,`location`=%s,`phoneno`=%s,`email`=%s,`password`=%s,`services`=%s,`ambulance`=%s,`photo`=%s,`ambulancePhoto`=%s WHERE name=%s"
        cursor.execute(sql, (name, location, phoneno, email, password, services, ambulance, encodedimage, encodedimage2, intial_username))
        conn.commit()
        return logout()
    
    elif request.method == 'POST' and session.get('role') == "doctor":
        username = str(request.form['username'])
        name = str(request.form['name'])
        location = str(request.form['location'])
        phoneno = str(request.form['phoneno'])
        email = str(request.form['email'])
        specialist = str(request.form['specialist'])
        password = str(request.form['password'])
        photo = request.files['photo']

        readimage = photo.read() 

        encodedimage = b64encode(readimage).decode("utf-8")

        sql = "UPDATE `privateDoctors` SET `username`=%s,`name`=%s,`location`=%s, `phoneno`=%s,`email`=%s,`specialist`=%s,`password`=%s,`photo`=%s WHERE username = %s"
        cursor.execute(sql,(username, name, location, phoneno, email,  specialist, password, encodedimage, intial_username))
        conn.commit()
        return logout()

    else:
        return redirect('/')



@app.route('/dashboard-delete', methods=['POST', 'GET'])
def delete_():
    conn = pymysql.connect(
            host='localhost',
            user='root',
            password='',
            db='webDoc'
        )
    cursor = conn.cursor()
    if request.method == 'POST' and session.get('role') == 'user':
        username = request.form['username']
        sql = "DELETE FROM `users` WHERE username = %s"
        cursor.execute(sql, username)
        conn.commit()
        return logout()
    elif request.method == 'POST' and session.get('role') == 'hospital':
        name = str(request.form['name'])
        sql = "DELETE FROM `hospital` WHERE name = %s"
        cursor.execute(sql, name)
        conn.commit()
        return logout()

@app.route('/scheduled-appoinments')
def scheduled_appoinments():
    username = session.get('username')

    conn = pymysql.connect(
        host='localhost',
        user='root',
        password='',
        db='webDoc'
    )
    cursor = conn.cursor()
    
    if session.get("role") == "user":
        sql = "SELECT name, location, phoneno, email, photo, specialist,schedules.date, schedules.time FROM privateDoctors LEFT JOIN schedules ON privateDoctors.name = schedules.doctorName WHERE schedules.patientName = %s"
        cursor.execute(sql, username)
        
        if cursor.rowcount == 0:
            return render_template('scheduledResults.html', msg="No appoinments booked yet")
        else:
            rows = cursor.fetchall()
            return render_template('scheduledResults.html', msg="You current appoinments" , rows=rows)
        
    elif session.get('role') == "doctor":
        sql = "SELECT users.fullname, users.email, schedules.date, schedules.time FROM users LEFT JOIN schedules ON users.username = schedules.patientName WHERE schedules.doctorName = (SELECT privateDoctors.name FROM privateDoctors LEFT JOIN schedules on privateDoctors.name = schedules.doctorName WHERE privateDoctors.username = %s)"
        cursor.execute(sql, username)

        if cursor.rowcount == 0:
            return render_template('scheduledResults.html', msg="No appoinments booked yet")
        else:
            rows = cursor.fetchall()
            return render_template('scheduledResultsDoc.html', rows=rows)




@app.route('/schedule', methods=['POST', 'GET'])
def schedule():
    username = session.get('username')

    conn = pymysql.connect(
        host='localhost',
        user='root',
        password='',
        db='webDoc'
    )
    cursor = conn.cursor()
    patientSql = "SELECT fullname FROM users where username = %s"
    cursor.execute(patientSql, username)
    rows = cursor.fetchall()

    if request.method == 'POST':
        date = request.form['date']
        time = request.form['time']
        doctorName = request.form['name']

        sql = "INSERT INTO schedules(patientName, doctorName, date, time) VALUES(%s, %s, %s, %s)"
        cursor.execute(sql, (username, doctorName, date, time))
        conn.commit()
        return redirect('/scheduled-appoinments')



    else:
        return redirect('/')


@app.route('/remove-appoinment', methods=['POST', 'GET'])
def remove():
    username = session.get('username')
    doctorName = str(request.form['name'])

    conn = pymysql.connect(
        host='localhost', 
        user='root', 
        password='',
        db='webDoc'
    )
    cursor = conn.cursor()
    if session.get("role") == "user" and request.method == "POST":
        sql = "DELETE FROM `schedules` WHERE patientName = %s AND doctorName = %s"
        cursor.execute(sql, (username, doctorName))
        conn.commit()
        return redirect('/scheduled-appoinments')
    

@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('role', None)
    return redirect('/')


# run
if __name__ == '__main__':
    app.run(debug=True, port=5000)
# port = 10000