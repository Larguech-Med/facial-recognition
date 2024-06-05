from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL

app = Flask(__name__)
app.secret_key = 'secret-key'

# MySQL Config
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'stage_facial_regonition'  # Correct spelling

print("testing")

mysql = MySQL(app)

@app.route('/')
def home():
    print("Entering home route")
    if 'username' in session:  # Corrected the session key name
        return render_template('home.html', username=session['username'])
    else:
        return render_template('home.html')
    

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        username = request.form.get('username')
        pwd = request.form.get('password')
        cur = mysql.connection.cursor()
        cur.execute(f"select username, password from user where username = '{username}'")
        user = cur.fetchone()
        cur.close()
        if user and pwd == user[2]:
            session['username'] = user
            return redirect(url_for('home'))
        else:
            return render_template('login.html', error='Invalid username or password')
    return render_template('login.html')

# Ensure Flask app runs
if __name__ == "__main__":
    app.run(debug=True)