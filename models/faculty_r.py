from flask import *
from flask_mysqldb import MySQL
import yaml
import hashlib
import json

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

def faculty_timetable():
    
    if(session.get('fid')):
        userDetails = session['fid']
        fid = session['fid']
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM faculty WHERE fid = '%s' ;"% (fid))
        rv = cur.fetchall();
        facultyDetails=rv
        cur.execute("SELECT * FROM course_list JOIN teaches ON course_list.cid=teaches.cid WHERE fid='%s' " %(fid))
        courselist = cur.fetchall();
        # join teaches and course_list wrt cid where fid=fid
        cur.execute('''SELECT fid,cid,room
                        FROM teaches
                        NATURAL JOIN course_list
                        WHERE fid = '%s' ; 
                        '''% (fid))
        rv = cur.fetchall()
        cur.execute('''SELECT * FROM 
                        (SELECT cid, cname FROM teaches 
                        NATURAL JOIN course_list
                        WHERE fid = '%s') as temp, room_cid 
                        WHERE temp.cid = room_cid.ccid;
                         '''% (fid))
        sv = cur.fetchall()

        HeadingTT, timeTableInfo = generateTT(rv, sv)
        cur.close()
    else:
        userDetails = "Not Authorized to access"
        timeTableInfo = "Nothing to display"
        facultyDetails = "Not Authorized to access"
        courselist={}
        HeadingTT = ""
    return render_template('faculty_timetable.html'
                ,userDetails=userDetails, timeTableInfo=timeTableInfo,facultyDetails=facultyDetails,courselist=courselist, HeadingTT=HeadingTT)

def assign_grade(id):

    if(session.get('fid')):
        userDetails = session['fid']
        fid = session['fid']
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM faculty WHERE fid = '%s' ;"% (fid))
        rv = cur.fetchall();
        facultyDetails=rv
        cur.execute("SELECT cname FROM course_list WHERE cid = '%s' ;"% (id))
        coursename=cur.fetchall()[0][0]
        cur.execute("SELECT * FROM course_list JOIN teaches ON course_list.cid=teaches.cid WHERE fid='%s' " %(fid))
        courselist = cur.fetchall();
        # join teaches and course_list wrt cid where fid=fid
        cur.execute('''SELECT fid,cid,room
                        FROM teaches
                        NATURAL JOIN course_list
                        WHERE fid = '%s' ; 
                        '''% (fid))
        rv = cur.fetchall()
        cur.execute('''SELECT * FROM 
                        (SELECT cid, cname FROM teaches 
                        NATURAL JOIN course_list
                        WHERE fid = '%s') as temp, room_cid 
                        WHERE temp.cid = room_cid.ccid;
                         '''% (fid))
        sv = cur.fetchall()

        HeadingTT, timeTableInfo = generateTT(rv, sv)
        cur.execute('''SELECT sid,sname,grade,grade_endsem FROM enroll NATURAL JOIN student where cid='%s';
                         '''% (id))
        coursestudentlist=cur.fetchall()             
        cur.close()
        if request.method == 'POST':
            # Fetch form data
            data = request.form
            for x in data:
                list=x   
            data_=json.loads(list)
            for student in data_ :
              if len(student)!=0:
                sid=student['sid']
                msegrade=student['grademidsem']
                esegrade=student['gradeendsem']
                cur = mysql.connection.cursor()
                cur.execute("UPDATE enroll SET grade = %s, grade_endsem = %s WHERE (sid = %s AND cid= %s)",(msegrade,esegrade,sid,id))
                mysql.connection.commit()
                cur.close()
    else:
        userDetails = "Not Authorized to access"
        timeTableInfo = "Nothing to display"
        facultyDetails = "Not Authorized to access"
        courselist={}
        coursestudentlist={}
        coursename=""
        HeadingTT = ""
    return render_template('assigngrades.html'
            ,userDetails=userDetails,id=id,cname=coursename,coursestudentlist=coursestudentlist, timeTableInfo=timeTableInfo,facultyDetails=facultyDetails,courselist=courselist, HeadingTT=HeadingTT)