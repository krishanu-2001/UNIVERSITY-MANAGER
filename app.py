from flask import *
from flask_mysqldb import MySQL
import yaml
import hashlib

app = Flask(__name__)
app.secret_key = "abc"

# Configure db
db = yaml.load(open('db.yaml'))
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']

mysql = MySQL(app)


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    flash = ""
    flag = 1
    if request.method == 'POST':
        # Fetch form data
        userDetails = request.form
        rollno = userDetails['rollno']
        password = userDetails['password']
        hashedpassword = hashlib.md5(password.encode()).hexdigest()
        cur = mysql.connection.cursor()
        cur.execute("SELECT COUNT(*), password, sname FROM student WHERE rollno = '%s' "% (rollno))
        rv = cur.fetchall()
        flag = (rv[0][0])
        curpassword = (rv[0][1])
        name = (rv[0][2])
        mysql.connection.commit()
        cur.close()
        #give access here!!
        if(flag >= 1 and hashedpassword == curpassword):
            session['rollno'] = rollno
            return redirect(url_for('users', name = name))
        else:
            flash = "wrong id or password!"
            flag = 0
    if flag != 0:
        flash = ""
    return render_template('login.html', flash = flash)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    flash = ""
    if request.method == 'POST':
        # Fetch form data
        userDetails = request.form
        rollno = userDetails['rollno']
        name = userDetails['name']
        password = userDetails['password']
        hashedpassword = hashlib.md5(password.encode()).hexdigest()
        confpassword = userDetails['confpassword']
        if (len(rollno) == 0 or len(password) == 0 or len(name) == 0):
            flash = "null values encountered"

        elif (confpassword != password):
            #pass
            flash = "check password"
        else:
            cur = mysql.connection.cursor()
            cur.execute("SELECT COUNT(*) FROM student WHERE rollno = '%s' "% (rollno))
            rv = cur.fetchall();
            flag = (rv[0][0]);
            if(flag >= 1):
                flash = "already enrolled!"
                mysql.connection.commit()
                cur.close()
            else:
                cur.execute("INSERT INTO student(rollno, sname, password) VALUES(%s, %s, %s)",(rollno, name, hashedpassword))
                mysql.connection.commit()
                cur.close()
                session['rollno'] = rollno
                return redirect(url_for('users', name = name))
    return render_template('signup.html', flash = flash)


@app.route('/logout')
def logout():
    flash = "logout successfully!"
    if(session.get('rollno')):
        session.pop('rollno')
    return render_template('index.html', flash = flash)


@app.route('/users')
def users():
    cur = mysql.connection.cursor()
    if(session.get('rollno')):
        userDetails = session['rollno']
        rollno = session['rollno']
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM student WHERE rollno = '%s' "% (rollno))
        rv = cur.fetchall();
        cur.close()
    else:
        userDetails = "Not Authorized to access"

    return render_template('users.html',userDetails=userDetails)


@app.route('/studentprofile', methods=['GET','POST'])
def studentprofile():
    rollno = session['rollno']
    flash = ""
    flag = 1
    if request.method == 'POST':
        # Fetch form data
        userDetails = request.form
        rollno = userDetails['rollno']
        phone = userDetails['phone']
        address = userDetails['address']
        cpi = userDetails['cpi']
        _class = userDetails['class']
        program = userDetails['program']
        email = userDetails['email']
        dob_dd = userDetails['dob_dd']
        dob_mm = userDetails['dob_mm']
        dob_yy = userDetails['dob_yy']
        if(len(phone) > 0 and len(address) > 0 and len(_class) > 0 and len(program) > 0 and len(email) > 0):
            #pass
            cur = mysql.connection.cursor()
            cur.execute("UPDATE student SET phone = %s, address = %s, cpi = %s, class = %s, program = %s, email = %s, dob_dd = %s, dob_mm = %s, dob_yy = %s WHERE rollno = %s",(phone, address, cpi, _class, program, email, dob_dd, dob_mm, dob_yy, rollno)  )
            mysql.connection.commit()
            cur.close()
        else:
            flash = "wrong id or password!"
            flag = 0
        #give access here!!

    if flag != 0:
        flash = ""
    return render_template('studentprofile.html', rollno = rollno)

@app.route('/faclogin', methods=['GET', 'POST'])
def faclogin():
    flash = ""
    flag = 1
    if request.method == 'POST':
        # Fetch form data
        facultyDetails = request.form
        fid = facultyDetails['fid']
        password = facultyDetails['password']
        hashedpassword = hashlib.md5(password.encode()).hexdigest()
        cur = mysql.connection.cursor()
        cur.execute("SELECT COUNT(*), password, fname FROM faculty WHERE fid = '%s' "% (fid))
        rv = cur.fetchall()
        flag = (rv[0][0])
        curpassword = (rv[0][1])
        name = (rv[0][2])
        mysql.connection.commit()
        cur.close()
        #give access here!!
        if(flag >= 1 and hashedpassword == curpassword):
            session['fid'] = fid
            return redirect(url_for('faculty', name = name))
        else:
            flash = "wrong id or password!"
            flag = 0
    if flag != 0:
        flash = ""
    return render_template('faclogin.html', flash = flash)    
@app.route('/facsignup', methods=['GET', 'POST'])
def facsignup():
    flash = ""
    if request.method == 'POST':
        # Fetch form data
        facultyDetails = request.form
        fid = facultyDetails['fid']
        name = facultyDetails['name']
        password = facultyDetails['password']
        hashedpassword = hashlib.md5(password.encode()).hexdigest()
        confpassword = facultyDetails['confpassword']
        if (len(fid) == 0 or len(password) == 0 or len(name) == 0):
            flash = "null values encountered"

        elif (confpassword != password):
            #pass
            flash = "check password"
        else:
            cur = mysql.connection.cursor()
            cur.execute("SELECT COUNT(*) FROM faculty WHERE fid = '%s' "% (fid))
            rv = cur.fetchall();
            flag = (rv[0][0]);
            if(flag >= 1):
                flash = "already enrolled!"
                mysql.connection.commit()
                cur.close()
            else:
                cur.execute("INSERT INTO faculty(fid, fname, password) VALUES(%s, %s, %s)",(fid, name, hashedpassword))
                mysql.connection.commit()
                cur.close()
                session['fid'] = fid
                return redirect(url_for('faculty', name = name))
    return render_template('facsignup.html', flash = flash) 
@app.route('/faculty')
def faculty():
    cur = mysql.connection.cursor()
    if(session.get('fid')):
        facultyDetails = session['fid']
        fid = session['fid']
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM faculty WHERE fid = '%s' "% (fid))
        rv = cur.fetchall();
        cur.close()
    else:
        userDetails = "Not Authorized to access"
    return render_template('faculty.html',facultyDetails=facultyDetails)
@app.route('/flogout')
def flogout():
    flash = "logout successfully!"
    if(session.get('fid')):
        session.pop('fid')
    return render_template('index.html', flash = flash)    


if __name__ == '__main__':
    flag = 0
    app.run(debug=True)
