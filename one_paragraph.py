#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import (Flask, render_template, redirect, url_for, request,
                   session)
from flask.ext.sqlalchemy import SQLAlchemy
from functools import wraps

import datetime
import os
import urlparse
import md5


urlparse.uses_netloc.append("postgres")

app = Flask(__name__)
app.secret_key = "secret_key"
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ["DATABASE_URL"]
db = SQLAlchemy(app)


class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(120), unique=False)

    def __init__(self, email, password):
        self.email = email
        self.password = md5.md5(password).hexdigest()

    def check_password(self, password):
        return self.password == md5.md5(password).hexdigest()

    def __repr__(self):
        return '<User %r>' % self.email


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)
    date = db.Column(db.Date, index=True)
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'), index=True)
    author = db.relationship('Author',
                             backref=db.backref('posts', lazy='dynamic'))

    __table_args__ = (db.UniqueConstraint("date", "author_id",
                      name="_date_and_author_id"), )

    def __init__(self, content, author_id, date=None):
        self.content = content
        if date is None:
            date = datetime.date.today()
        self.date = date
        self.author_id = author_id

    def __repr__(self):
        return '<Post %r>' % self.date


@app.before_request
def make_session_permanent():
    session.permanent = True
    app.permanent_session_lifetime = datetime.timedelta(days=7)


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "email" not in session:
            return redirect(url_for("login", next=request.url))
        return f(*args, **kwargs)
    return decorated_function


@app.route("/add_user", methods=["GET", "POST"])
def add_user():
    if request.method == "GET":
        return render_template("add_user.html", title="Add User: 1Paragraph")
    else:
        email = request.form["email"]
        pw = request.form["password"]
        new_user = Author(email, pw)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for("index"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html", title="Login: 1Paragraph")
    else:
        user = Author.query.filter_by(email=request.form["email"]).first()
        if user is not None and user.check_password(request.form["password"]):
            session["email"] = user.email
            session["user_id"] = user.id
        return redirect(request.args.get("next"))


@app.route("/logout")
@login_required
def logout():
    del session["email"]
    return redirect(url_for("index"))


@app.route("/diary/<string:date>", methods=["GET", "POST"])
@login_required
def get_diary(date):
    date_seq = [int(x) for x in date.split('-')]
    date_obj = datetime.date(date_seq[0], date_seq[1], date_seq[2])
    author_id = int(session["user_id"])
    if request.method == "GET":
        post = Post.query.filter_by(author_id=author_id,
                                    date=date_obj).first()
        if post:
            post_map = {'content': post.content, 'date': date}
        else:
            post_map = {'content': '', 'date': date}

        prev_date = Post.query\
            .filter("author_id=%d AND date < '%s'" % (author_id, date))\
            .order_by(Post.date.desc())\
            .first()
        if prev_date is not None:
            post_map['prev_date'] = prev_date.date.strftime("%Y-%m-%d")

        next_date = Post.query\
            .filter("author_id=%d AND date > '%s'" % (author_id, date))\
            .order_by(Post.date)\
            .first()
        if next_date is not None:
            post_map['next_date'] = next_date.date.strftime("%Y-%m-%d")

        return render_template("main.html", title="%s: 1Paragraph" % date,
                               post=post_map)
    else:
        try:
            new_post = Post(request.form["content"], author_id, date_obj)
            db.session.add(new_post)
            db.session.commit()
        except:
            db.session.rollback()
            db.session.query(Post)\
                .filter_by(author_id=author_id, date=date_obj)\
                .update({"content": request.form["content"]})
            db.session.commit()
        finally:
            print len(request.form["content"].strip())
            if len(request.form["content"].strip()) == 0:
                db.session.query(Post)\
                    .filter_by(author_id=author_id, date=date_obj)\
                    .delete()
                db.session.commit()

        return "OK"


@app.route("/")
@login_required
def index():
    datestr = datetime.date.today().strftime('%Y-%m-%d')
    return redirect(url_for("get_diary", date=datestr))


@app.route("/init")
def init():
    db.create_all()
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
