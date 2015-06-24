#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import (Flask, render_template, redirect, url_for, request,
                   session)
from functools import wraps
import os
import psycopg2
import urlparse


urlparse.uses_netloc.append("postgres")
db_url = urlparse.urlparse(os.environ["DATABASE_URL"])
print db_url
db_conn = psycopg2.connect(
    database=db_url.path[1:],
    user=db_url.username,
    password=db_url.password,
    host=db_url.hostname,
    port=db_url.port
)

app = Flask(__name__)
app.secret_key = "secret_key"


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "email" not in session:
            return redirect(url_for("login", next=request.url))
        return f(*args, **kwargs)
    return decorated_function


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html", title="Login: 1Paragraph")
    else:
        session["email"] = request.form["email"]
        return redirect(request.args.get("next"))


@app.route("/logout")
@login_required
def logout():
    del session["email"]
    return redirect(url_for("index"))


@app.route("/")
@login_required
def index():
    return render_template("main.html", title="1Paragraph")


if __name__ == "__main__":
    app.run(debug=True)
