from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)

# Data model
class Time(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    puzzle = db.Column(db.String(20), nullable=False) # Foriegn key to puzzle table? Category type?
    value = db.Column(db.Numeric(10,2), nullable=False)
    date_entered = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    method_entered = db.Column(db.Integer, nullable=False) # Foriegn key to method table? {1,2,3,4}

    def __repr__(self):
        return "TIME {}".format(self.id)



@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        # Add new time to database manually
        value = request.form['value']
        puzzle = request.form['puzzle']
        new_time = Time(value=value, puzzle=puzzle, method_entered=1)

        try:
            db.session.add(new_time)
            db.session.commit()
            return redirect("/")
        except:
            return "There was an issue manually adding the time."
    else:
        # Show page
        times = Time.query.order_by(Time.date_entered).all()
        return render_template('index.html', times=times)

@app.route('/delete/<int:id>')
def delete(id):
    time_to_delete = Time.query.get_or_404(id)
    
    try:
        db.session.delete(time_to_delete)
        db.session.commit()
        return redirect('/')
    except:
         return "There was an issue deleting the time."

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    time = Time.query.get_or_404(id)
    if request.method == 'POST':
        time.value = request.form['value']
        time.puzzle = request.form['puzzle']
        
        try:
            db.session.commit()
            return redirect('/')
        except:
            return "There was an error updating the time"
    else:
        return render_template('update.html', time=time)

    

if __name__ == "__main__":
    app.run(debug=True)