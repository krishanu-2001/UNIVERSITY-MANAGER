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

def admin_login():
    flash = ""
    flag = 1
    if request.method == 'POST':
        # Fetch form data
        adminDetails = request.form
        aid = adminDetails['adminid']
        password = adminDetails['password']
        hashedpassword = hashlib.md5(password.encode()).hexdigest()
        # adding aid = root, password = password for admin
        curpassword = "password"
        curpassword = hashlib.md5(curpassword.encode()).hexdigest()
        name = "root"
        
        #give access here!!
        if(flag >= 1 and name == aid and hashedpassword == curpassword):
            session['aid'] = aid
            return redirect(url_for('admin_home', name = name))
        else:
            flash = "wrong id or password!"
            flag = 0
    if flag != 0:
        flash = ""
    return render_template('admin/admin_login.html', flash = flash)

def admin_home():
    return render_template('admin/admin_home.html')

def admin_selectstudent():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * from student where 1 = 1")
    rv = cur.fetchall()
    studentlist = rv
    mysql.connection.commit()
    cur.close()
    return render_template('admin/admin_selectstudent.html', studentlist = studentlist)

def admin_studentprofile():
    if(session.get('aid')):
        rollno = str(request.args.get("rollno"))
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
                cur.execute("UPDATE student SET phone = %s, address = %s, cpi = %s, class = %s, program = %s, email = %s, dob_dd = %s, dob_mm = %s, dob_yy = %s WHERE sid = %s",(phone, address, cpi, _class, program, email, dob_dd, dob_mm, dob_yy, rollno)  )
                mysql.connection.commit()
                cur.close()
            else:
                flash = "wrong id or password!"
                flag = 0
            #give access here!!
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM student WHERE sid = '%s'"%(rollno))
        studentDetail = cur.fetchall()
        mysql.connection.commit()
        cur.close()


        if flag != 0:
            flash = ""
        return render_template('admin/admin_studentprofile.html', rollno = rollno, studentDetail = studentDetail)
    
    else:
        return "not authorized to view"
