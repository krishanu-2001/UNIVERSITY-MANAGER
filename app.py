from flask import *
from flask_cors import CORS, cross_origin
from flask_mysqldb import MySQL
import yaml
import hashlib
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask_mail import Mail
from flask_mail import Message
import models.student_krish as student_krish
import models.admin_krish as admin_krish
import models.faculty_r as faculty_r
import models.course_krish as course_krish

app = Flask(__name__)
CORS(app)
app.secret_key = "abc"
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'

# Configure db
db = yaml.load(open('db.yaml'))
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'ADD EMAIL HERE'
app.config['MAIL_PASSWORD'] = 'ADD PASSWORD HERE'

mysql = MySQL(app)
mail = Mail(app)

#UTIL function
def get_reset_token(id, expires_sec=600):
    s = Serializer(app.config['SECRET_KEY'], expires_sec)
    return s.dumps({'user_id': id}).decode('utf-8')
def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return user_id
def send_reset_mail(user,email,id):
    token = get_reset_token(id)
    msg = Message('Password Reset Request',
                  sender='noreply@universitymanager.com',
                  recipients=[email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('reset_token', token=token, user=user , _external=True)}
If you did not make this request then simply ignore this email and no changes will be made.
'''
    mail.send(msg)

# endUtils

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

@app.route('/resetrequest/<user>')
def resetrequest(user):
    flash=""
    return render_template('resetrequest.html', flash = flash, user=user)
@app.route('/resetpassword/<user>', methods=['GET','POST'])
def resetpassword(user):
    flash="Reset link has been sent to your registered Email."
    if request.method == 'POST':
        # Fetch form data
        userDetails = request.form
        id = userDetails['id']
    if(user=="student"):
        cur = mysql.connection.cursor()
        cur.execute("SELECT email FROM student WHERE sid = '%s' "% (id))
        rv = cur.fetchall()
        if (rv==() ):
            if(id==''):
                flash="Invalid Username"
                return render_template('resetrequest.html', flash = flash, user=user)       
        else:
            email=rv[0][0]
            send_reset_mail(user,email,id) 
        cur.close()
        return render_template('student/login.html', flash = flash)
    elif(user=="faculty"):
        cur = mysql.connection.cursor()
        cur.execute("SELECT email FROM faculty WHERE fid = '%s' "% (id))
        rv = cur.fetchall()
        if (rv==() ):
            if(id==''):
                flash="Invalid Username"
                return render_template('resetrequest.html', flash = flash, user=user)       
        else:
            email=rv[0][0]
            send_reset_mail(user,email,id) 
        cur.close()
        return render_template('faclogin.html', flash = flash)
    else:
        return render_template('admin/admin_login.html', flash = flash)   

@app.route('/reset_password/<user>/<token>', methods=['GET','POST'])
def reset_token(user,token):
    user_id=verify_reset_token(token)
    flash=""
    if user_id is None:
        flash="Your token is Invalid or Expired."
        return render_template('resetrequest.html', flash = flash, user=user)
    if request.method == 'POST':
        # Fetch form data
        userDetails = request.form
        password = userDetails['password'] 
        cpassword = userDetails['confirmpassword']
        hashedpassword = hashlib.md5(password.encode()).hexdigest()
        if(password!=cpassword):
            flash="Passwords do not match. Check Password."
            render_template('resetpassword.html', flash = flash, user=user ,token=token)
        else:
            if(user=="student"):
                cur = mysql.connection.cursor()
                cur.execute("UPDATE student SET password = %s WHERE sid = %s",(hashedpassword, user_id))
                mysql.connection.commit()
                cur.close()
                flash="Your password has been updated!"
                return render_template('student/login.html', flash = flash)
            elif(user=="faculty"):
                cur = mysql.connection.cursor()
                cur.execute("UPDATE faculty SET password = %s WHERE fid = %s",(hashedpassword, user_id))
                mysql.connection.commit()
                cur.close()
                flash="Your password has been updated!"
                return render_template('faclogin.html', flash = flash)
            else:
                return render_template('admin/admin_login.html', flash = flash)

    return render_template('resetpassword.html', flash = flash, user=user ,token=token)     

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
app.add_url_rule('/admin_selectdept', view_func=admin_krish.admin_selectdept, methods=['GET','POST'])
app.add_url_rule('/admin_adddept', view_func=admin_krish.admin_adddept, methods=['GET','POST'])
app.add_url_rule('/admin_deletedept', view_func=admin_krish.admin_deletedept, methods=['GET','POST'])
app.add_url_rule('/admin_editdept', view_func=admin_krish.admin_editdept, methods=['GET','POST'])
app.add_url_rule('/admin_selectfaculty', view_func=admin_krish.admin_selectfaculty, methods=['GET','POST'])
app.add_url_rule('/admin_addfaculty', view_func=admin_krish.admin_addfaculty, methods=['GET','POST'])
app.add_url_rule('/admin_deletefaculty', view_func=admin_krish.admin_deletefaculty, methods=['GET','POST'])
app.add_url_rule('/admin_editfaculty', view_func=admin_krish.admin_editfaculty, methods=['GET','POST'])
app.add_url_rule('/adminShowStudentByProgram', view_func=admin_krish.adminShowStudentByProgram, methods=['GET'])
app.add_url_rule('/admin_course_req', view_func=admin_krish.admin_course_req, methods=['GET','POST'])
app.add_url_rule('/add_course_req/<id>', view_func=admin_krish.add_course_req, methods=['GET','POST'])
app.add_url_rule('/del_course_req/<id>', view_func=admin_krish.del_course_req, methods=['GET','POST'])

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
            return redirect(url_for('faculty'))
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
                return redirect(url_for('faculty'))
    return render_template('facsignup.html', flash = flash) 
@app.route('/faculty')
def faculty():
    flash=""
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
        courselist={}
    return render_template('faculty.html',facultyDetails=facultyDetails,courselist=courselist,flash=flash)

@app.route('/changepass/faculty', methods=['GET', 'POST'])
def facchangepassword():
    flash=""
    cur = mysql.connection.cursor()
    if(session.get('fid')):
        fid = session['fid']
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM faculty WHERE fid = '%s' "% (fid))
        facultyDetails = cur.fetchall();
        if request.method == 'POST':
        # Fetch form data
            formDetails = request.form
            curpassword = formDetails['curpassword']
            newpassword = formDetails['newpassword']
            conpassword = formDetails['conpassword']
            hashedpassword = hashlib.md5(curpassword.encode()).hexdigest()
            hashednewpassword = hashlib.md5(newpassword.encode()).hexdigest()
            passwordcheck=facultyDetails[0][7]
            if (len(curpassword) == 0 or len(newpassword) == 0 or len(conpassword) == 0):
                flash = "Null Values Encountered."
                return render_template('facultychangepass.html',facultyDetails=facultyDetails,flash=flash)
            elif (conpassword != newpassword):
                flash = "Passwords do not match. Check password."
                return render_template('facultychangepass.html',facultyDetails=facultyDetails,flash=flash)
            elif (passwordcheck != hashedpassword):
                flash = "Current Password is wrong."
                return render_template('facultychangepass.html',facultyDetails=facultyDetails,flash=flash)    
            else:
                cur = mysql.connection.cursor()
                cur.execute("UPDATE faculty SET password = %s WHERE fid = %s",(hashednewpassword,fid) )
                mysql.connection.commit()
                return redirect(url_for('faculty',flash="Password Changed."))
    return render_template('facultychangepass.html',facultyDetails=facultyDetails,flash=flash)    
    
@app.route('/faculty/<id>')
def facultypublicprofile(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM faculty WHERE fid = '%s' "% (id))
    facultyDetails = cur.fetchall()[0];
    cur.execute("SELECT cname FROM course_list NATURAL JOIN teaches WHERE fid='%s' "% (id))
    courselist = cur.fetchall();
    cur.execute("SELECT dname FROM department WHERE did IN (SELECT did FROM works_in where fid='%s') "% (id))
    department = cur.fetchall();
    cur.close()
    return render_template('facultypublicprofile.html',facultyDetails=facultyDetails,courselist=courselist,department=department) 

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
        email = facultyDetails['email']
        phone = facultyDetails['phone']
        address = facultyDetails['address']
        if(len(phone) > 0 and len(address) > 0 and len(gender) > 0 and len(name) > 0 and len(email) > 0 and len(dob) > 0 ):
            #pass
            cur = mysql.connection.cursor()
            cur.execute("UPDATE faculty SET phone = %s, address = %s, gender = %s, fname = %s, email = %s, dob = %s WHERE fid = %s",(phone, address, gender, name, email, dob, fid))
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
@app.route('/flogout')
def flogout():
    flash = "logout successfully!"
    if(session.get('fid')):
        session.pop('fid')
    return render_template('index.html', flash = flash)
@app.route('/getfacultybyid', methods=['GET','POST'])
def getfacultybyid():
    if request.method == 'POST':
            _id = str(request.json['id'])
            cur = mysql.connection.cursor()
            cur.execute("SELECT * FROM faculty WHERE fid=%s",[_id] )
            fac=cur.fetchall()[0]
            cur.execute("SELECT did FROM works_in WHERE fid=%s",[_id] )
            did=cur.fetchall()[0]
            faculty=[]
            faculty.append({'fid':fac[0],'fname':fac[1],'phone':fac[2],'address':fac[3],'salary':fac[4],'email':fac[5],'dob':fac[6],'gender':fac[8],'position':fac[9],'did':did})
            cur.close()
            return json.dumps(faculty)   

app.add_url_rule('/faculty_timetable', view_func=faculty_r.faculty_timetable, methods=['GET','POST'])
app.add_url_rule('/assigngrade/<id>', view_func=faculty_r.assign_grade, methods=['GET','POST'])

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
@app.route('/getdepartmentbyid', methods=['GET','POST'])
def getdepartmentbyid():
    if request.method == 'POST':
            _id = str(request.json['id'])
            cur = mysql.connection.cursor()
            cur.execute("SELECT * FROM department WHERE did=%s",[_id] )
            dept=cur.fetchall()[0]
            department=[]
            department.append({'did':dept[0],'dname':dept[1],'building':dept[2],'budget':dept[3],'contact':dept[4],'hodfid':dept[5],'hodsince':dept[6]})
            cur.close()
            return json.dumps(department)
@app.route('/department/<id>/faculty')
def department_faculty(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM department WHERE did='%s' "% (id))
    deptinfo=cur.fetchall()[0];
    cur.execute("SELECT * FROM faculty JOIN works_in ON faculty.fid=works_in.fid WHERE did ='%s' "% (id))
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
@app.route('/department/<id>/programs')
def department_programs(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM department WHERE did='%s' "% (id))
    deptinfo=cur.fetchall()[0];
    cur.execute("SELECT * FROM has JOIN program ON has.has_pid=program.program_id WHERE has_did ='%s' "% (id))
    programlist=cur.fetchall();
    cur.close()    
    return render_template('deptprogramlist.html',programlist=programlist,deptinfo=deptinfo)       

if __name__ == '__main__':
    flag = 0
    app.run(debug=True)

