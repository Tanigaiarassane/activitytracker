import os
from flask import Flask,redirect,url_for
from flask import render_template, jsonify
from flask_sqlalchemy  import SQLAlchemy
from datetime import datetime
import logging

from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField,PasswordField,BooleanField, SelectField
from wtforms.validators import DataRequired, Length,Email,EqualTo,ValidationError
# adding
app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba248'

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') or 'sqlite:///test1.db'

db = SQLAlchemy(app)

stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)
app.logger.addHandler(stream_handler) 
members = [{'name':'tanigai', 'location':'chennai'},
               {'name': 'Dhina', 'location': 'Pondy'}
]


class ActivityItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable= False, unique = True)
    content = db.Column(db.Text, nullable = False)
    status = db.Column(db.String(10), nullable = False, default= "New")
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)


class ToDo(FlaskForm):
    name = StringField('Title',validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    status = SelectField('Status', choices=[('New', 'New'),
                                                 ('In Progress', 'Progress'), ('Closed', 'Closed') ])
    submit = SubmitField('Submit')


@app.route("/")
def hello():
    return render_template('responsive.html')


@app.route("/list")
def listing():
    return render_template('list.html', items = members)

@app.route("/create", methods = ["POST","GET"])
def new_item():
    form = ToDo()
    if form.validate_on_submit():
        #print "Validation completed ...{}".format(form.name.data)
        activity = ActivityItem(name=form.name.data, content = form.content.data, status = form.status.data)
        db.session.add(activity)
        db.session.commit()
        #print ActivityItem.query.all()
        return redirect(url_for('listing'))
    return render_template('create.html', form =form)

@app.route("/jlist")
def jlisting():
    return jsonify({'members': members})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)

