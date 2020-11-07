from flask import *
from flask_mysqldb import MySQL
import yaml
import hashlib
import models.student_krish as student_krish
import models.admin_krish as admin_krish

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


#student starts here student starts here student starts here student starts here student starts here
#student starts here student starts here student starts here student starts here student starts here

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
        cur.execute("SELECT COUNT(*), password, sname FROM student WHERE sid = '%s' "% (rollno))
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
    return render_template('student/login.html', flash = flash)

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
            cur.execute("SELECT COUNT(*) FROM student WHERE sid = '%s' "% (rollno))
            rv = cur.fetchall();
            flag = (rv[0][0]);
            if(flag >= 1):
                flash = "already enrolled!"
                mysql.connection.commit()
                cur.close()
            else:
                cur.execute("INSERT INTO student(sid, sname, password) VALUES(%s, %s, %s)",(rollno, name, hashedpassword))
                mysql.connection.commit()
                cur.close()
                session['rollno'] = rollno
                return redirect(url_for('users', name = name))
    return render_template('student/signup.html', flash = flash)


@app.route('/logout')
def logout():
    flash = "logout successfully!"
    if(session.get('rollno')):
        session.pop('rollno')
    return render_template('index.html', flash = flash)


@app.route('/users')
def users():
    
    if(session.get('rollno')):
        userDetails = session['rollno']
        rollno = session['rollno']
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM student WHERE sid = '%s' "% (rollno))
        rv = cur.fetchall();
        cur.close()
    else:
        userDetails = "Not Authorized to access"

    return render_template('student/users.html',userDetails=userDetails)


@app.route('/studentprofile', methods=['GET','POST'])
def studentprofile():
    if(session.get('rollno')):
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
                print("not allowed to update")
            else:
                flash = "wrong id or password!"
                flag = 0
            #give access here!!
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM student WHERE sid = '%s'"%(rollno))
        studentDetail = cur.fetchall()
        mysql.connection.commit()
        if flag != 0:
            flash = ""
        return render_template('student/studentprofile.html', rollno = rollno, studentDetail = studentDetail)
    
    else:
        return "not authorized to view"


#testing add_url_rule > code in student.krish file in models
app.add_url_rule('/student_timetable', view_func=student_krish.student_timetable, methods=['GET','POST'])
app.add_url_rule('/student_course_list', view_func=student_krish.student_course_list, methods=['GET','POST'])
app.add_url_rule('/student_course_reg', view_func=student_krish.student_course_reg, methods=['GET','POST'])
app.add_url_rule('/student_course_reg', view_func=student_krish.student_course_reg, methods=['GET','POST'])
app.add_url_rule('/student_grade_sheet', view_func=student_krish.student_grade_sheet, methods=['GET','POST'])

#student ends here student ends here student ends here student ends here student ends here student ends here
#student ends here student ends here student ends here student ends here student ends here student ends here


#admin starts here admin starts here admin starts here admin starts here admin starts here admin starts here
#admin starts here admin starts here admin starts here admin starts here admin starts here admin starts here

app.add_url_rule('/admin_login', view_func=admin_krish.admin_login, methods=['GET','POST'])
app.add_url_rule('/admin_home', view_func=admin_krish.admin_home, methods=['GET','POST'])
app.add_url_rule('/admin_selectstudent', view_func=admin_krish.admin_selectstudent, methods=['GET','POST'])
app.add_url_rule('/admin_studentprofile', view_func=admin_krish.admin_studentprofile, methods=['GET','POST'])
app.add_url_rule('/adminShowStudent', view_func=admin_krish.adminShowStudent, methods=['GET'])
app.add_url_rule('/ExcelDownload', view_func=admin_krish.ExcelDownload, methods=['GET'])
app.add_url_rule('/adminShowCourse', view_func=admin_krish.adminShowCourse, methods=['GET'])
#admin ends here admin ends here admin ends here admin ends here admin ends here admin ends here admin ends here
#admin ends here admin ends here admin ends here admin ends here admin ends here admin ends here



#faculty starts here faculty starts here faculty starts here faculty starts here faculty starts here faculty starts here
#faculty starts here faculty starts here faculty starts here faculty starts here faculty starts here faculty starts here
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
        facultyDetails = cur.fetchall();
        cur.execute("SELECT * FROM course_list JOIN teaches ON course_list.cid=teaches.cid WHERE fid='%s' " %(fid))
        courselist = cur.fetchall();
        cur.close()
    else:
        facultyDetails = "Not Authorized to access"
    return render_template('faculty.html',facultyDetails=facultyDetails,courselist=courselist)
@app.route('/facultyprofile', methods=['GET','POST'])
def facultyprofile():
    fid = session['fid']
    flash = ""
    flag = 1
    if request.method == 'POST':
        # Fetch form data
        facultyDetails = request.form
        fid = facultyDetails['fid']
        name = facultyDetails['name']
        dob = facultyDetails['dob']
        gender = facultyDetails['gender']
        position = facultyDetails['position']
        salary = facultyDetails['salary']
        email = facultyDetails['email']
        phone = facultyDetails['phone']
        address = facultyDetails['address']
        if(len(phone) > 0 and len(address) > 0 and len(gender) > 0 and len(name) > 0 and len(email) > 0 and len(dob) > 0 and len(position) > 0 and len(salary) > 0):
            #pass
            cur = mysql.connection.cursor()
            cur.execute("UPDATE faculty SET phone = %s, address = %s, gender = %s, fname = %s, email = %s, dob = %s, position = %s, salary = %s WHERE fid = %s",(phone, address, gender, name, email, dob, position, salary, fid))
            mysql.connection.commit()
            cur.close()
        else:
            flash = "wrong id or password!"
            flag = 0
        #give access here!!
    if flag != 0:
        flash = ""
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM faculty WHERE fid = '%s' "% (fid))
    facultyDetails = cur.fetchall()[0];
    cur.close()    
    return render_template('facultyprofile.html',facultyDetails=facultyDetails )    
@app.route('/fhome')
def fhome():
    cur = mysql.connection.cursor()
    if(session.get('fid')):
        fid = session['fid']
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM faculty WHERE fid = '%s' "% (fid))
        name = cur.fetchall()[0][1];
        cur.close()  
    else:
        name = "Not Authorized to access"
    return redirect(url_for('faculty', name = name))
@app.route('/flogout')
def flogout():
    flash = "logout successfully!"
    if(session.get('fid')):
        session.pop('fid')
    return render_template('index.html', flash = flash)    

#dept starts here dept starts here dept starts here dept starts here dept starts here
#dept starts here dept starts here dept starts here dept starts here dept starts here

@app.route('/department')
def departmenthome():
    cur = mysql.connection.cursor()
    cur.execute("SELECT did,dname FROM department")
    departments = cur.fetchall();
    cur.close()    
    return render_template('departmenthome.html',departments=departments)
@app.route('/department/<id>')
def department(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT did,dname FROM department")
    departments = cur.fetchall();
    cur.execute("SELECT * FROM departmentview WHERE did='%s' "% (id))
    deptinfo=cur.fetchall()[0];
    cur.close()    
    return render_template('department.html',departments=departments,deptinfo=deptinfo)    
@app.route('/department/<id>/faculty')
def department_faculty(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM department WHERE did='%s' "% (id))
    deptinfo=cur.fetchall()[0];
    cur.execute("SELECT * FROM faculty JOIN works_in ON faculty.fid=works_in.fid JOIN department ON works_in.did ='%s' GROUP BY faculty.fid"% (id))
    facultylist=cur.fetchall();
    cur.close()    
    return render_template('deptfaclist.html',facultylist=facultylist,deptinfo=deptinfo)   
@app.route('/department/<id>/student')
def department_student(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM department WHERE did='%s' "% (id))
    deptinfo=cur.fetchall()[0];
    cur.execute("SELECT * FROM student WHERE student.did='%s' "% (id))
    studentlist=cur.fetchall();
    cur.close()    
    return render_template('deptstudlist.html',studentlist=studentlist,deptinfo=deptinfo)   

if __name__ == '__main__':
    flag = 0
    app.run(debug=True)

