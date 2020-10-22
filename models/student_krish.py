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

#UTIL function
def generateTT(rv, sv):
    TT = []
    weekDay = ['MON', 'TUE', "WED", "THU", "FRI", "SAT"]
    headingTT = []
    for j in range(7,18):
        headingTT.append(str(j) + ":00 - " + str(j) + ":55")

    for i in range(6):
        day = weekDay[i] # MON
        fillWeek = []
        fillWeek.append(day)
        for j in range(7,18):
            fillWeek.append(['',''])
        TT.append(fillWeek)

    #iterate through sv and fill TT
    for cid, cname, room, time, day, ccid in sv:
        day = day - 1
        time = time-6 # note 7 am is starting time
        #print([TT[day][time][0], TT[day][time][1], day, time])
        TT[day][time][0] = str(cname)
        TT[day][time][1] = str(room)

    return headingTT, TT

# endUtils

#working well use this for refractoring

def student_timetable():
    
    if(session.get('rollno')):
        userDetails = session['rollno']
        rollno = session['rollno']
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM student WHERE sid = '%s' ;"% (rollno))
        rv = cur.fetchall();
        
        # join enroll and course_list wrt cid where sid = rollno
        cur.execute('''SELECT sid,cid,room
                        FROM enroll
                        NATURAL JOIN course_list
                        WHERE sid = '%s' ; 
                        '''% (rollno))
        rv = cur.fetchall()
        cur.execute('''SELECT * FROM 
                        (SELECT cid, cname FROM enroll 
                        NATURAL JOIN course_list
                        WHERE sid = '%s') as temp, room_cid 
                        WHERE temp.cid = room_cid.ccid;
                         '''% (rollno))
        sv = cur.fetchall()

        HeadingTT, timeTableInfo = generateTT(rv, sv)
        cur.close()
        

    else:
        userDetails = "Not Authorized to access"
        timeTableInfo = "Nothing to display"
        HeadingTT = ""
    return render_template('student/student_timetable.html'
                ,userDetails=userDetails, timeTableInfo=timeTableInfo, HeadingTT=HeadingTT)


def student_course_list():
    
    if(session.get('rollno')):
        userDetails = session['rollno']
        rollno = session['rollno']
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM student WHERE sid = '%s' ;"% (rollno))
        rv = cur.fetchall();
        
        # join enroll and course_list wrt cid where sid = rollno
        cur.execute('''SELECT sid,cid,room
                        FROM enroll
                        NATURAL JOIN course_list
                        WHERE sid = '%s' ; 
                        '''% (rollno))
        rv = cur.fetchall()
        cur.execute('''SELECT cid, cname, grade, hours FROM enroll 
                        NATURAL JOIN course_list
                        WHERE sid = '%s';
                         '''% (rollno))
        sv = cur.fetchall()
        courselist = sv
        cur.close()
        mysql.connection.commit()


    else:
        userDetails = "Not Authorized to access"
        timeTableInfo = "Nothing to display"
        courselist = "nothing"

    return render_template('student/student_course_list.html'
                ,userDetails=userDetails, courselist=courselist)

def student_course_reg():
    courseList = ""
    if(session.get('rollno')):
        userDetails = session['rollno']
        rollno = session['rollno']
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM student WHERE sid = '%s' ;"% (rollno))
        rv = cur.fetchall()
        xlist = []
        if request.method == 'POST':
            clist = (request.form.getlist('courses'))
            for cids in clist:
                cur.execute('''
                        INSERT IGNORE INTO enroll 
                        (sid, cid, grade) VALUES
                        ('%s', '%s', 'A');
                        '''% (rollno, cids))


        # join student and course list where class =( sem+1 )/ 2
        cur.execute('''
            SELECT fid, cid, cname, fname FROM 
                faculty as A
                NATURAL JOIN
                (SELECT * from teaches
                NATURAL JOIN
                course_list WHERE cid in 
                (SELECT cid FROM student, course_list 
                WHERE class = (sem + 1)/2 AND sid = '%s')
            ) as B;
             '''% (rollno))
        rv = cur.fetchall()
        courselist = rv
        mysql.connection.commit()
        cur.close()
        

    else:
        userDetails = "Not Authorized to access"
        timeTableInfo = "Nothing to display"
        courselist = "nothing"

    return render_template('student/student_course_reg.html'
                ,userDetails=userDetails, courselist=courselist)
