from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
import datetime

app = Flask(__name__, template_folder="templates")
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
db = SQLAlchemy(app)
db.create_all()

class Statistics(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cpu_load = db.Column(db.Float, nullable=False)
    datetime = db.Column(db.DateTime, nullable=False)

    def __init__(self, cpu_load):
        self.cpu_load = cpu_load
        self.datetime = datetime.datetime.utcnow()
    def __repr__(self):
        return '<ID {0}>'.format(self.id)

@app.route('/')
def home():
    last_records = Statistics.query.order_by(Statistics.id).limit(100).all()
    min_data = db.session.query(Statistics, func.min(Statistics.cpu_load)).all()
    max_data = db.session.query(Statistics, func.max(Statistics.cpu_load)).all()
    avg_data = db.session.query(Statistics, func.avg(Statistics.cpu_load)).all()
    print(avg_data)
    return render_template('main.html', min_load=min_data[0][1], max_load=max_data[0][1], avg_load=avg_data[0][1])

@app.route('/data', methods=['POST'])
def insert_data():
    param = request.form['load']
    value = float(param)

    if value < 0 or value > 100:
        raise Exception('load parameter have invalid data. Should be in percent ')
    load = Statistics(value)
    db.session.add(load)
    db.session.commit()
    db.session.close()
    return 'Added CPU load {0}'.format(value)


# If we're running in stand alone mode, run the application
if __name__ == '__main__':
    db.create_all()
    app.run(debug=True, host='0.0.0.0', port=8081)