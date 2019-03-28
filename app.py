from flask import Flask, render_template, request
from dbconnector import simpleQuery, get_db

app = Flask(__name__)


@app.route('/', methods=['POST', 'GET'])
def hello_world():
    patrons = simpleQuery("patron", "patronFirstName, patronLastName")
    if request.method == "POST":
        db = get_db()
        cur = db.cursor()

        selectedPatron = request.form['listOfPatrons']

        cur.execute("SELECT patronFirstName, patronLastName, patronEmail FROM patron WHERE patronLastName = " + "'" + selectedPatron + "'")
        patronInfo = cur.fetchall()

        return render_template('accounts.html', html_patrons = patrons, firstName = patronInfo[0])

    else:
        return render_template('accounts.html', html_patrons=patrons)

if __name__ == '__main__':
    app.run(debug=True)
