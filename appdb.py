from flask import Flask, render_template, request, redirect
from flask_mysqldb import MySQL
import yaml


app = Flask(__name__)

#Configure db
db = yaml.load(open('db.yaml'))
app.config['MYSQL_HOST']=db['mysql_host']
app.config['MYSQL_USER']=db['mysql_user']
app.config['MYSQL_PASSWORD']=db['mysql_password']
app.config['MYSQL_DB']=db['mysql_db']

mysql=MySQL(app)

@app.route('/', methods=['GET'])
def home():
    if request.method=='GET':
        return render_template('home.html')

    
@app.route('/newuser')
def register_success():
       return render_template('register_success.html')

@app.route('/newlogged')
def login_success():
    return render_template('login_success')

@app.route('/register', methods=['GET','POST'])
def index():
    if request.method=='POST':
        #Fetch form data
        userDetails = request.form
        username=userDetails['username']
        password=userDetails['password']
        cur=mysql.connection.cursor()
        cur.execute("INSERT INTO users(username,password) VALUES (%s,%s)", (username,password))
        mysql.connection.commit()
        cur.close()
        return redirect ('/newuser')
    return render_template('index.html')


@app.route('/login', methods=['GET','POST']) 
def index2():
    if request.method=='POST':
        #Fetch form data
        userDetails = request.form
        username=userDetails['username']
        password=userDetails['password']
        cur=mysql.connection.cursor()
        cur.execute("INSERT INTO logged(username,password) VALUES (%s,%s)", (username,password))
        mysql.connection.commit()
        cur.close()
        return redirect ('/newuser')
    return render_template('index2.html')

@app.route('/users')
def users():
    cur = mysql.connection.cursor()
    resultValue = cur.execute("SELECT * FROM users")
    if resultValue > 0:
        userDetails = cur.fetchall() 
        return render_template('users.html', userDetails=userDetails)

@app.errorhandler(404)
def page_not_found(e):
    
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(debug=True)

