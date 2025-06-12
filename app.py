from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///friends.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Corrected config key
db = SQLAlchemy(app)

class Friends(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    number = db.Column(db.Integer, nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self) -> str:
        return f"{self.sno} - {self.name}"  

@app.route('/', methods=['GET','POST'])
def hello_world():
    if request.method=='POST':
        name=request.form['name']
        number=request.form['number']
        friend=Friends(name=name, number=number)
        db.session.add(friend)
        db.session.commit()
        
    allfriends=Friends.query.all()
    return render_template('index.html', allfriends=allfriends)

@app.route('/show')
def products():
    allfriends=Friends.query.all()
    print(allfriends)
    return 'this is products page'

@app.route('/delete/<int:sno>')
def delete(sno):
    allfriends=Friends.query.filter_by(sno=sno).first()
    db.session.delete(allfriends)
    db.session.commit()
    return redirect("/")

@app.route('/update/<int:sno>', methods=['GET','POST'])
def update(sno):
    if request.method=='POST':
        name=request.form['name']
        number=request.form['number']
        allfriends=Friends.query.filter_by(sno=sno).first()
        allfriends.name=name
        allfriends.number=number
        db.session.add(allfriends)
        db.session.commit()
        return redirect("/")
        
    allfriends=Friends.query.filter_by(sno=sno).first()
    return render_template('update.html', allfriends=allfriends)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=8000)
