from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask import request,redirect

app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///firstapp.db"

db = SQLAlchemy(app)

class FirstApp(db.Model):
    sno = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fname = db.Column(db.String(100), nullable=False)
    lname = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f"{self.sno} - {self.fname}"
    
with app.app_context():
    db.create_all()

@app.route("/", methods = ['GET', 'POST'])
def hello_world():
    # return "<p>Hello, World!</p>"
    if request.method=='POST':
        fname = request.form.get('fname')
        lname = request.form.get('lname')
        email = request.form.get('email')
        
        if fname and lname and email:    
            firstapp = FirstApp(fname=fname, lname=lname, email=email)
            db.session.add(firstapp)
            db.session.commit()

    allpeople = FirstApp.query.all()
    print(allpeople)

    return render_template('Index.html', people=allpeople)

@app.route("/home")
def home():
    return "Wellcome to the Home Page" 

@app.route('/delete/<int:sno>')
def delete(sno):
    allpeople = FirstApp.query.filter_by(sno=sno).first()

    db.session.delete(allpeople)
    db.session.commit()

    return redirect("/") 

@app.route('/update/<int:sno>', methods=['GET', 'POST'])
def update(sno):
    person = FirstApp.query.filter_by(sno=sno).first()

    if request.method == 'POST':
        person.fname = request.form['fname']
        person.lname = request.form['lname']
        person.email = request.form['email']
        db.session.commit()
        return redirect('/')

    return render_template('update.html', person=person)


if __name__ == "__main__":
    app.run(debug=True)
