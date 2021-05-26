from flask import *
from flask_mysqldb import MySQL
import yaml
import hashlib
import flask_excel as excel
import pyexcel_xlsx
import re
import string
import random

regex = re.compile(
        r'^(?:http|ftp)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
        r'localhost|' #localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)

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

# UTIl
def generateString(N):
  # generate a hash
  # using random.choices()
  # generating random strings 
  res = ''.join(random.choices(string.ascii_uppercase +
                              string.digits, k = N))
  return res

def url_shortner_home():
  if request.method == 'POST':
    longurl = request.form['longurl']
    # https://krishanu-2001.github.io
    if re.match(regex, longurl) is not None:
      cur = mysql.connection.cursor()
      cur.execute("select shorturl, longurl from url where longurl = '%s';"%(longurl))
      existsrv = cur.fetchall()
      count = 0
      if existsrv and len(existsrv) > 0:
        str = existsrv[0][0]

      else:
        str = generateString(10)
        cur.execute("select * from url where shorturl = '%s';"%(str))
        rv = cur.fetchall()
        while(rv and len(rv) > 0 and count < 50):
          count += 1
          str = generateString(10)
          cur.execute("select shorturl, longurl from url where shorturl = '%s';"%(str))
          rv = cur.fetchall()

      mysql.connection.commit()
      cur.close()
      if count > 50:
        flash('Please try again!')
      else:
        strlink = "http://127.0.0.1:5000/url_find/" + str
        flash(strlink)
        cur = mysql.connection.cursor()
        cur.execute("insert ignore into url (shorturl, longurl) values ('%s','%s');"%(str, longurl))
        cur = mysql.connection.cursor()
        mysql.connection.commit()
        cur.close()

    else:
      flash('Not Valid Url')

    return redirect(url_for('url_shortner_home'))

  return render_template('url_shortner/home.html')

def url_find(url):
  cur = mysql.connection.cursor()
  cur.execute("SELECT longurl FROM url WHERE shorturl='%s';"% (url))
  rv = cur.fetchall()
  mysql.connection.commit()
  cur.close()
  if(rv and len(rv) > 0):
    longurl = rv[0][0]
    return redirect(longurl)
  else:
    return redirect(url_for('url_shortner_home'))