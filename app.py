from flask import Flask
from flask import render_template, redirect, request, flash
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
import pymysql
import secrets

conn = "mysql+pymysql://{0}:{1}@{2}/{3}".format(secrets.dbuser, secrets.dbpass, secrets.dbhost, secrets.dbname)

app = Flask(__name__)
app.config['SECRET_KEY']='SuperSecretKey'
app.config['SQLALCHEMY_DATABASE_URI'] = conn
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # silence the deprecation warning
db = SQLAlchemy(app)

class zzhijie_singersapp(db.Model):
    singerid = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))

    def __repr__(self):
        return "id: {0} | first name: {1} | last name: {2}".format(self.id, self.first_name, self.last_name)

class SingersForm(FlaskForm):
    first_name = StringField('First Name:', validators=[DataRequired()])
    last_name = StringField('Last Name:', validators=[DataRequired()])

@app.route('/')
def index():
    all_singers = zzhijie_singersapp.query.all()
    return render_template('index.html', singers=all_singers, pageTitle='Zhijie Singers')

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        form = request.form
        search_value = form['search_string']
        search = "%{0}%".format(search_value)
        results = colbert_friends.query.filter(or_(colbert_friends.first_name.like(search),
                                                    colbert_friends.last_name.like(search))).all()
        return render_template('index.html', singers=results, pageTitle='Zhijie singers', legend="Search Results")
    else:
        return redirect('/')

@app.route('/add_singer', methods=['GET', 'POST'])
def add_singer():
    form = SingersForm()
    if form.validate_on_submit():
        singer = zzhijie_singersapp(first_name=form.first_name.data, last_name=form.last_name.data)
        db.session.add(singer)
        db.session.commit()
        return redirect('/')

    return render_template('add_singer.html', form=form, pageTitle='Add A New Singer')

@app.route('/delete_singer/<int:singerid>', methods=['GET','POST'])
def delete_singer(singerid):
    if request.method == 'POST': #if it's a POST request, delete the friend from the database
        obj = zzhijie_singersapp.query.filter_by(singerid=singerid).first()
        db.session.delete(obj)
        db.session.commit()
        flash('Singer was successfully deleted!')
        return redirect("/")

    else: #if it's a GET request, send them to the home page
        return redirect("/")

@app.route('/singer/<int:singer_id>', methods=['GET','POST'])
def get_singer(singer_id):
    singer = zzhijie_singersapp.query.get_or_404(singer_id)
    return render_template('singer.html', form=singer, pageTitle='Singer Details', legend="Singer Details")

@app.route('/singer/<int:singer_id>/update', methods=['GET','POST'])
def update_singer(singer_id):
    singer = zzhijie_singersapp.query.get_or_404(singer_id)
    form = SingersForm()

    if form.validate_on_submit():
        singer.first_name = form.first_name.data
        singer.last_name = form.last_name.data
        db.session.commit()
        return redirect(url_for('get_singer', singer_id=singer.singerid))

    form.singerid.data = singer.singerid
    form.first_name.data = friend.first_name
    form.last_name.data = friend.last_name
    return render_template('update_singer.html', form=form, pageTitle='Update Singer', legend="Update A Singer")




if __name__ == '__main__':
    app.run(debug=True)
