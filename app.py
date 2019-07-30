from flask import *
import MySQLdb


app = Flask(__name__)
app.secret_key = "ismail"
con = MySQLdb.connect(host='localhost', user='root', password='1603', port=3306, db='db')
cmd = con.cursor()


@app.route('/')
def hello_world():
    return render_template('homePage.html')


@app.route('/regPage')
def regpage():
    return render_template('formPage.html')


@app.route('/register', methods=['POST'])
def register():
    firstname = request.form['fn']
    lastname = request.form['ln']
    gender = request.form['gender']
    email = request.form['email']
    password = request.form['pw']
    dob = request.form['dob']

    cmd.execute("insert into login values ('"+ email+"', '"+password+"') ")
    cmd.execute("insert into userdb values('" + firstname + "', '" + lastname + "', '" + gender + "', '" + email + "','" + password + "', '" + dob + "')")
    con.commit()

    return render_template('formPage.html')


@app.route('/view', methods=['POST', 'GET'])
def view():
    cmd.execute("select * from userdb")
    s = cmd.fetchall()

    return render_template('view.html', val=s)


@app.route('/viewLogin', methods=['POST', 'GET'])
def view_login():
    cmd.execute("select * from login")
    s = cmd.fetchall()

    return render_template('viewLogin.html', val=s)


@app.route('/delete')
def delete():
    email = request.args.get('id')
    print(id)
    cmd.execute("delete from userdb where email ='"+str(email)+"'")
    con.commit()
    return ''' <script>alert('deleted successfully'); window.location='view'</script>'''


@app.route('/edit', methods=['GET'])
def edit():
    email = request.args.get('id')
    cmd.execute("select * from userdb where email ='"+str(email)+"'")
    s = cmd.fetchone()
    session['emailid'] = email
    return render_template('edit.html', val=s)


@app.route('/update', methods=['POST'])
def update():
    firstname = request.form['fn']
    lastname = request.form['ln']
    gender = request.form['gender']

    password = request.form['pw']
    dob = request.form['dob']
    emailid = session['emailid']

    cmd.execute("update userdb set `first name`='" + firstname + "', `last name`='" + lastname + "', gender='" + gender + "', password='" + password + "', dob='"+dob+"' ")
    con.commit()
    return '''<script>alert('Updated Successfully');window.location='view'</script>'''


@app.route('/logPage')
def log():
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['pw']
    cmd.execute("SELECT * FROM login WHERE email= '"+email+"' AND password='"+ password +"'")
    s = cmd.fetchone()
    if s is not None:
        return render_template('homePage.html')
    else:
        '''<script>alert('Similar Information not Available');window.location='regPage'</script>'''


if __name__ == '__main__':
    app.run()
