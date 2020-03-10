from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func, desc
import datetime

app = Flask(__name__, template_folder="templates")
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
db = SQLAlchemy(app)
db.create_all()

class Statistics(db.Model):
    ''' 
    Definition of the model for cpu stat
    '''
    id = db.Column(db.Integer, primary_key=True)
    cpu_load = db.Column(db.Float, nullable=False)
    datetime = db.Column(db.DateTime, nullable=False)

    def __init__(self, cpu_load):
        self.cpu_load = cpu_load
        self.datetime = datetime.datetime.utcnow()

def aggregate(func):
    '''
    general function for aggregation of results
    '''
    return db.session.query(Statistics, func(Statistics.cpu_load)).all()

@app.route('/')
def home():
    '''
    showing of the metrics stats
    '''
    last_records = Statistics.query.order_by(desc(Statistics.id)).limit(100).all()
    min_data = aggregate(func.min)
    max_data = aggregate(func.max)
    avg_data = aggregate(func.avg)

    last_100_min = db.session.query(Statistics, func.min(Statistics.cpu_load)).order_by(desc(Statistics.id)).limit(5).all()
    last_100_max = db.session.query(Statistics, func.max(Statistics.cpu_load)).order_by(desc(Statistics.id)).limit(5).all()
    last_100_avg = db.session.query(Statistics, func.avg(Statistics.cpu_load)).order_by(desc(Statistics.id)).limit(5).all()
    return render_template('main.html',
    records=last_records,\
    min_load=min_data[0][1], \
    max_load=max_data[0][1], \
    avg_load=avg_data[0][1], \
    min_100_load = last_100_min[0][1],\
    max_100_load = last_100_max[0][1],\
    avg_100_load = last_100_avg[0][1])

@app.route('/data', methods=['POST'])
def insert_data():
    ''' 
    receiving of the cpu load data
    In the curl it will looks like
    curl -d "load=10" -X POST $HOST/data
    '''
    param = request.form['load']
    value = float(param)

    if value < 0 or value > 100:
        raise Exception('load parameter have invalid data. Should be in percent ')
    load = Statistics(value)
    db.session.add(load)
    db.session.commit()
    db.session.close()
    return 'Added CPU load {0}'.format(value)

def run():
    db.create_all()
    app.run(debug=True, host='0.0.0.0', port=8081)
if __name__ == '__main__':
    run()