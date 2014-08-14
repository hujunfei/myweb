# -*- coding: utf-8 -*-
from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def index():
    return render_template("index.html")

@app.route('/post', methods=['GET'])
def add_article():
    return render_template("article/add.html")


if __name__ == '__main__':
    app.run()
