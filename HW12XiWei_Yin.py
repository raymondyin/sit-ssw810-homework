"""
@author: Xi Wei (Raymond) Yin
cwid: 10442986

assignment: Homework 12
date: Dec 11, 2018

url:
https://sit.instructure.com/courses/28343/assignments/118688
"""

from flask import Flask, render_template
import sqlite3

app = Flask(__name__)


@app.route('/instructor_courses')
def instructor_courses():
    DB_FILE = "810_startup.db"

    query = """SELECT i.CWID, i.Name, i.Dept, g.Course, count(*) AS Students FROM Instructors i 
                JOIN Grades g on i.CWID=g.Instructor_CWID GROUP BY g.Course order by i.Name;"""
    db = sqlite3.connect(DB_FILE)
    rows = db.execute(query)

    data = [{'CWID': cwid, 'Name': name, 'Department': department, 'Courses': courses, 'Students': students}
            for cwid, name, department, courses, students in rows]

    db.close()

    return render_template('instructor_courses.html',
                           instructors=data)


if __name__ == '__main__':
    app.run(debug=True)
