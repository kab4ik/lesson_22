from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from forms import CommentForm

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///vines.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'qwertysdfgsdgsdgsdgsdgsdgsdg'
db = SQLAlchemy(app)


class Vine(db.Model):
    __tablename__ = 'VINES'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    price = db.Column(db.Float)
    sort_id = db.Column(db.Integer, db.ForeignKey('SORTS.id'))
    sort = db.relationship('Sort', backref=db.backref('vines'))
    producer_id = db.Column(db.Integer, db.ForeignKey('PRODUCERS.id'))
    producer = db.relationship('Producer', backref=db.backref('vines'))
    bestseller = db.Column(db.Integer, default=0)
    def __str__(self):
        return self.name

class Sort(db.Model):
    __tablename__ = 'SORTS'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    def __str__(self):
        return self.name


class Producer(db.Model):
    __tablename__ = 'PRODUCERS'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    def __str__(self):
        return f'\"{self.name}\"'

class Comment(db.Model):
    __tablename__ = 'COMMETS'
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(80))
    email = db.Column(db.String(80))
    text = db.Column(db.String)
    vine_id = db.Column(db.Integer, db.ForeignKey('VINES.id'))
    vine = db.relationship('Vine', backref=db.backref('comments'))
    def __str__(self):
        return f'{self.text} ({self.author}, {self.email})'

@app.route('/')
def start():
    return redirect(url_for('index'))

@app.route('/index')
@app.route('/index/<string:sort_type>')
def index(sort_type=None):
    vines = Vine.query.all()
    if sort_type == 'byname':
        vines.sort(key=lambda x: x.name)
    if sort_type == 'bypricelow':
        vines.sort(key=lambda x: x.price)
    if sort_type == 'bypricehigh':
        vines.sort(key=lambda x: -x.price)
    if sort_type == 'byproducer':
        vines.sort(key=lambda x: (x.producer.name, x.name))
    return render_template('index.html', vines=vines)

@app.route('/vine/<int:pk>')
def vine(pk):
    vine = Vine.query.get(pk)
    return render_template('vine.html', vine=vine)

@app.route('/filter/<int:sort_id>/<int:producer_id>')
def filter(sort_id, producer_id):
    producer, sort = None, None
    if sort_id == 0:
        vines = Vine.query.filter(Vine.producer_id == producer_id).all()
        producer = Producer.query.get(producer_id)
    elif producer_id == 0:
        vines = Vine.query.filter(Vine.sort_id == sort_id).all()
        sort = Sort.query.get(sort_id)
    else:
        vines = Vine.query.filter(Vine.sort_id == sort_id,
                                  Vine.producer_id == producer_id).all()
        producer = Producer.query.get(producer_id)
        sort = Sort.query.get(sort_id)
    return render_template('filter.html', vines=vines, producer=producer, sort=sort)
@app.route('/config/<int:vine_id>')
def config(vine_id):
    vine = Vine.query.get(vine_id)
    producers = Producer.query.all()
    sorts = Sort.query.all()
    return render_template('config.html', vine=vine, sorts=sorts, producers=producers,)

@app.route('/configform/<int:vine_id>', methods=['post'])
def configform(vine_id):
    if request.method == 'POST':
        vine = Vine.query.get(vine_id)
        newname = request.form.get('name')
        newprice = float(request.form.get('price'))
        newproducer_id = int(request.form.get('producer_id'))
        newsort_id = int(request.form.get('sort_id'))
        newbestseller = int(request.form.get('bestseller') != None)
        try:
            vine.name = newname
            vine.price = newprice
            vine.sort_id = newsort_id
            vine.producer_id = newproducer_id
            vine.bestseller = newbestseller
            db.session.commit()
        except:
            print('Не удалось внести изменения', vine_id)
    return redirect(url_for('vine', pk=vine_id))
@app.route('/delete/<int:vine_id>')
def delete(vine_id):
    try:
        vine = Vine.query.get(vine_id)
        db.session.delete(vine)
        db.session.commit()
    except:
        print('Не удалось удалить', vine_id)
    return redirect(url_for('index'))

@app.route('/comment/<int:vine_id>', methods=['get', 'post'])
def comment(vine_id):
    vine = Vine.query.get(vine_id)
    form = CommentForm()
    if form.validate_on_submit():
        author = form.data['author']
        email = form.data['email']
        text = form.data['text']
        try:
            comment = Comment(vine_id=vine_id,
                              author=author, email=email, text=text)
            db.session.add(comment)
            db.session.commit()
            return redirect(url_for('vine', pk=vine_id))
        except:
            print('не удалось добавить комментарий')
    return render_template('comment.html', vine=vine, form=form)


if __name__ == '__main__':
    app.run(debug=True)