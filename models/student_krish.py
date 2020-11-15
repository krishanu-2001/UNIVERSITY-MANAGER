from flask import *
from flask_mysqldb import MySQL
import yaml
import hashlib
from decimal import *

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

''' sets credits through switch case '''
def setCredits(sv, rv, cur_cpi):
    temp = []
    _credits = Decimal(0.00)
    cur_cpi = Decimal(0.00)
    total_credits = Decimal(rv[0])
    for row in sv:
        x = []
        count = 0
        for col in row:
            count += 1
            x.append(col)
            print(col)
            if(count == 4):
                # do cases here
                cpi = row[count]
                val = 0.00
                if(col == 'A' or col == 'AA'):
                    val = Decimal(1.00) * cpi
                elif (col == 'AB'):
                    val = Decimal(0.90) * cpi
                elif (col == 'B' or col == 'BB'):
                    val = Decimal(0.80) * cpi
                else:
                    val = Decimal(0.00) * cpi
                _credits += val
                x.append(round(val,2))
        temp.append(x)
    overall_credits = cur_cpi * total_credits / 10
    overall_credits += _credits
    return temp, _credits, total_credits, overall_credits

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
                        ('%s', '%s', 'N');
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


def student_grade_sheet():
    
    if(session.get('rollno')):
        userDetails = session['rollno']
        rollno = session['rollno']
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM student WHERE sid = '%s' ;"% (rollno))
        rv = cur.fetchall();
        getcontext().prec = 4
        # join enroll and course_list wrt cid where sid = rollno
        cur.execute('''SELECT SUM(credits)
                        FROM enroll
                        NATURAL JOIN course_list
                        WHERE sid = '%s' ; 
                        '''% (rollno))
        rv = cur.fetchall()

        cur.execute('''SELECT cpi from student where
                        sid = '%s'; 
                        '''% (rollno))
        xv = cur.fetchall()
        
        cur.execute('''SELECT cid, cname, grade, grade_endsem,credits FROM enroll 
                        NATURAL JOIN course_list
                        WHERE sid = '%s';
                         '''% (rollno))
        sv = cur.fetchall()
        courselist = sv
        cur_cpi = xv[0][0]
        # generate cpi params
        
        courselist, _credits, total_credits, overall_credits = setCredits(courselist, rv[0], cur_cpi)
        overall_total = total_credits
        # cpi params ends
        cur.close()
        mysql.connection.commit()


    else:
        userDetails = "Not Authorized to access"
        timeTableInfo = "Nothing to display"
        courselist = "nothing"
        _credits = 0.0
        total_credits = 0.0
        overall_credits = 0.0
        overall_credits = 0.0

    return render_template('student/student_grade_sheet.html'
                ,userDetails=userDetails, courselist=courselist
                ,credits = _credits, total_credits = total_credits,
                 overall_credits = overall_credits, overall_total = overall_total)
