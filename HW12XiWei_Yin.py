"""
@author: Xi Wei (Raymond) Yin
cwid: 10442986

assignment: Homework 12
date: Dec 11, 2018

url:
https://sit.instructure.com/courses/28343/assignments/118688
"""

from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return "hello Flask!"


if __name__ == '__main__':
    app.run(debug=True)
