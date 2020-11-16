from flask import *
from flask_mysqldb import MySQL
import yaml
import hashlib
import flask_excel as excel
import pyexcel_xlsx

app = Flask(__name__)
app.secret_key = "abc"
excel.init_excel(app) # required since version 0.0.7

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
    cur.execute("SELECT * from student where 1 = 1;")
    rv = cur.fetchall()
    studentlist = rv
    mysql.connection.commit()
    cur.close()
    return render_template('admin/admin_selectstudent.html', studentlist = studentlist)
def admin_selectdept():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * from department where 1 = 1")
    departments = cur.fetchall()
    cur.close()
    return render_template('admin/admin_selectdept.html',departments=departments)    
def admin_adddept():
    if(session.get('aid')):
        flash = ""
        flag = 1
        if request.method == 'POST':
            # Fetch form data
            deptDetails = request.form
            did = deptDetails['did']
            dname = deptDetails['dname']
            building = deptDetails['building']
            phone = deptDetails['phone']
            budget = deptDetails['budget']
            hodfid= deptDetails['hodfid']
            hodsince= deptDetails['hodsince']
            if (hodfid==''):
                hodfid=None
            if (hodsince==''):
                hodsince=None    
            if(len(phone) > 0 and len(did) > 0 and len(dname) > 0 and len(building) > 0 and len(budget) > 0):
                #pass
                cur = mysql.connection.cursor()
                cur.execute("INSERT INTO department (did, dname, building, budget, contactno, fid,since) VALUES (%s, %s, %s, %s, %s, %s, %s)",(did, dname, building, budget, phone, hodfid, hodsince)  )
                mysql.connection.commit()
                cur.close()
            else:
                flash = "Some of The Values entered NOT VALID"
                flag = 0
            #give access here!!
        if flag != 0:
            flash = ""
        return redirect(url_for('admin_selectdept'))    
    else:
        return "not authorized to view"    
def admin_deletedept():
    if(session.get('aid')):
        flash = ""
        flag = 1
        if request.method == 'POST':
            _id = str(request.json['id'])
            cur = mysql.connection.cursor()
            cur.execute("DELETE FROM department WHERE did=%s",[_id] )
            mysql.connection.commit()
            cur.close()
        cur = mysql.connection.cursor()
        cur.execute("SELECT * from department where 1 = 1")
        departments = cur.fetchall()
        cur.close()
        if flag != 0:
            flash = ""
        return "Executed" 
    else:
        return "not authorized to view"
def admin_editdept():
    if(session.get('aid')):
        flash = ""
        flag = 1
        if request.method == 'POST':
            # Fetch form data
            deptDetails = request.form
            didorig=deptDetails['did_orig']
            did = deptDetails['did']
            dname = deptDetails['dname']
            building = deptDetails['building']
            phone = deptDetails['phone']
            budget = deptDetails['budget']
            hodfid= deptDetails['hodfid']
            hodsince= deptDetails['hodsince']
            if (hodfid==''):
                hodfid=None  
            if (hodsince==''):
                hodsince=None     
            if(len(did) > 0 and len(dname) > 0 and len(building) > 0 and len(phone) > 0 and len(budget) > 0):
                #pass
                cur = mysql.connection.cursor()
                cur.execute("UPDATE department SET did = %s, dname = %s, building = %s, budget = %s, contactno = %s,fid= %s,since= %s WHERE did = %s",(did, dname, building, budget, phone, hodfid, hodsince, didorig)  )
                mysql.connection.commit()
                cur.close()
            else:
                flash = "Some of The Values entered NOT VALID"
                flag = 0
            #give access here!!
        cur = mysql.connection.cursor()
        cur.execute("SELECT * from department where 1 = 1")
        departments = cur.fetchall()
        cur.close()
        if flag != 0:
            flash = ""
        return render_template('admin/admin_selectdept.html',departments=departments,flash=flash) 
    else:
        return "not authorized to view" 

def admin_selectfaculty():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * from faculty where 1 = 1")
    faculty = cur.fetchall()
    cur.close()
    return render_template('admin/admin_faculty.html',faculty=faculty)    
def admin_addfaculty():
    if(session.get('aid')):
        flash = ""
        flag = 1
        if request.method == 'POST':
            # Fetch form data
            facultyDetails = request.form
            fid = facultyDetails['fid']
            fname = facultyDetails['fname']
            address = facultyDetails['address']
            phone = facultyDetails['phone']
            salary = facultyDetails['salary']
            email = facultyDetails['email']
            dob = facultyDetails['dob']
            gender = facultyDetails['gender']
            position = facultyDetails['position']
            did= facultyDetails['did']
            password="password"
            password = hashlib.md5(password.encode()).hexdigest()
            if (did==''):
                did=None    
            if(len(phone) > 0 and len(fid) > 0 and len(fname) > 0 and len(address) > 0 and len(salary) > 0 and len(email) > 0 and len(dob) > 0):
                #pass
                cur = mysql.connection.cursor()
                cur.execute("INSERT INTO faculty (fid, fname, address, salary, phone, email, dob, gender, position, password) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",(fid, fname, address, salary, phone, email, dob, gender, position, password)  )
                if(did!=None):
                    cur.execute("INSERT INTO works_in (fid, did) VALUES (%s, %s)",(fid,did)  )
                mysql.connection.commit()
                cur.close()
            else:
                flash = "Some of The Values entered NOT VALID"
                flag = 0
            #give access here!!
        if flag != 0:
            flash = ""
        return redirect(url_for('admin_selectfaculty'))    
    else:
        return "not authorized to view"    
def admin_deletefaculty():
    if(session.get('aid')):
        flash = ""
        flag = 1
        if request.method == 'POST':
            _id = str(request.json['id'])
            cur = mysql.connection.cursor()
            cur.execute("DELETE FROM faculty WHERE fid=%s",[_id] )
            mysql.connection.commit()
            cur.close()
        if flag != 0:
            flash = ""
        return "Executed" 
    else:
        return "not authorized to view"
def admin_editfaculty():
    if(session.get('aid')):
        flash = ""
        flag = 1
        if request.method == 'POST':
            # Fetch form data
            facultyDetails = request.form
            fidorig=facultyDetails['fid_orig']
            fid = facultyDetails['fid']
            fname = facultyDetails['fname']
            address = facultyDetails['address']
            phone = facultyDetails['phone']
            salary = facultyDetails['salary']
            email= facultyDetails['email']
            dob= facultyDetails['dob']
            gender= facultyDetails['gender']
            position= facultyDetails['position']
            did= facultyDetails['did']
            if (did==''):
                did=None    
            if(len(phone) > 0 and len(fid) > 0 and len(fname) > 0 and len(address) > 0 and len(salary) > 0 and len(email) > 0 and len(dob) > 0):
                #pass
                cur = mysql.connection.cursor()
                cur.execute("UPDATE faculty SET fid = %s, fname= %s, address= %s, salary= %s, phone= %s, email= %s, dob= %s, gender= %s, position= %s WHERE fid = %s",(fid, fname, address, salary, phone, email, dob, gender, position, fidorig)  )
                if(did!=None):
                    cur.execute("UPDATE works_in SET fid = %s,did= %s WHERE fid = %s", (fid,did,fidorig) )
                mysql.connection.commit()
                cur.close()
            else:
                flash = "Some of The Values entered NOT VALID"
                flag = 0
            #give access here!!
        if flag != 0:
            flash = ""
        return redirect(url_for('admin_selectfaculty')) 
    else:
        return "not authorized to view" 
                   
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

def adminShowStudent():
    return render_template('admin/adminShowStudent.html')

def ExcelDownload():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * from student where 1 = 1;")
    rv = cur.fetchall()

    studentlist = [['rno','name','phone','address','cpi','sem','branch','email','dob_dd','dob_mm','dob_yy','password','class']]
    for rows in rv:
        temp = []
        for items in rows:
            temp.append(items)
        studentlist.append(temp)

    mysql.connection.commit()
    cur.close()

    return excel.make_response_from_array(studentlist, "xlsx")
    
def adminShowCourse():
    return render_template('admin/adminShowCourse.html')


def adminShowStudentByProgram():
    cur = mysql.connection.cursor()
    cur.execute("SELECT sid,program FROM student ORDER BY program;")
    variable = cur.fetchall()
    mysql.connection.commit()
    cur.close();
    return render_template('admin/adminShowStudentByProgram.html',student = variable)

def admin_course_req():
    if(session.get('aid')):
        cur = mysql.connection.cursor()
        cur.execute("""SELECT A.sid,B.cname,A.cid,A.option from admin_control as A
                    NATURAL JOIN course_list as B
                    WHERE A.cid = B.cid
                        ;""")
        rv = cur.fetchall();
        cur.close()
        mysql.connection.commit()
    else:
        print("unauthorized access")

    return render_template('admin/admin_course_req.html', req = rv)

def add_course_req(id):
    if(session.get('aid')):
        cur = mysql.connection.cursor()
        x = id.split('_')
        _sid = x[0]
        _cid = x[1]
        cur.execute('''
                        INSERT IGNORE INTO enroll 
                        (sid, cid, grade) VALUES
                        ('%s', '%s', 'N');
                        '''% (_sid, _cid))
        cur.close()
        mysql.connection.commit()
        return redirect(("/del_course_req/%s"%(id)))
    else:
        print("unauthorized access")

    return redirect(url_for('admin_course_req'))

def del_course_req(id):
    if(session.get('aid')):
        cur = mysql.connection.cursor()
        x = id.split('_')
        _sid = x[0]
        _cid = x[1]
        print(_sid, _cid)
        cur.execute('''
                        DELETE FROM admin_control where 
                        sid = '%s' AND cid='%s';
                        '''% (_sid, _cid))
        rv = cur.fetchall()
        cur.close()
        print(rv)
        mysql.connection.commit()
    else:
        print("unauthorized access")

    return redirect(url_for('admin_course_req'))

def ExcelDownload_course():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * from course_list where 1 = 1;")
    rv = cur.fetchall()

    courselist = [['cid','cname','room','hours','year','sem','credits']]
    for rows in rv:
        temp = []
        for items in rows:
            temp.append(items)
        courselist.append(temp)

    mysql.connection.commit()
    cur.close()

    return excel.make_response_from_array(courselist, "xlsx")

def add_course():
    if(session.get('aid')):
        flash = ""
        flag = 1
        if request.method == 'POST':
            # Fetch form data
            userDetails = request.form
            cid = userDetails['cid']
            cname = userDetails['cname']
            room = userDetails['room']
            hours = userDetails['hours']
            year = userDetails['year']
            sem = userDetails['sem']
            credit = userDetails['credit']
            if(len(cname) > 0 and len(cid) > 0):
                #pass
                cur = mysql.connection.cursor()
                cur.execute("insert ignore into course_list values (%s,%s,%s,%s,%s,%s,%s)",(cid, cname, room, hours, year, sem, credit)  )
                mysql.connection.commit()
                cur.close()
            else:
                flash = "wrong cid or cname!"
                flag = 0
            #give access here!!

        if flag != 0:
            flash = ""
        return render_template('admin/admin_add_course.html')
    
    else:
        return "not authorized to view"
