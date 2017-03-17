from flask import render_template, url_for, redirect
from forms import CommentForm
from events import app, db
from api import eventbrite
from models import Comment
import datetime


@app.route('/', methods=['GET', 'POST'])
def about():
    user = eventbrite.get_user()
    print(user)
    id = user['id']
    name = user['name']
    return render_template('about.html', user=user, id=id, name=name)


@app.route('/events', methods=['GET', 'POST'])
def events():
    user = eventbrite.get_user()
    events = eventbrite.get_user_events(user.id)
    print(events)
    return render_template('events.html', event=events)


@app.route('/comments', methods=['GET', 'POST'])
def index():
    comments = Comment.query.order_by(db.desc(Comment.timestamp))
    return render_template('comments.html', comments=comments)


@app.route('/add', methods=['GET', 'POST'])
def add():
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(
            form.text.data,
            datetime.datetime.now()
        )
        db.session.add(comment)
        db.session.commit()
        return redirect(url_for('add'))
    comments = Comment.query.order_by(db.desc(Comment.timestamp))
    return render_template('add.html', comments=comments, form=form)
