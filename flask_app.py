import flask.scaffold
from flask import Flask, request, jsonify, g, send_file
from waitress import serve
import sqlite3
import logging
from database import initDB, getSemesters, getCourseCodes, getCourses, getSeatData, DATABASE_FILE_PATH

logging.basicConfig(filename='flask_app.log', level=logging.DEBUG, format='%(asctime)s %(levelname)s : %(message)s')
app = Flask(__name__)

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE_FILE_PATH)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@flask.scaffold.setupmethod
def before_first_request():
    initDB(get_db().cursor())

@app.route("/coursecodes")
def courseCodes():
    app.logger.info(f"/coursecodes {request.remote_addr} {request.headers.get('User-Agent')}")

    response = jsonify(getCourseCodes(get_db().cursor()))
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route("/semesters")
def semesters():
    app.logger.info(f"/semesters {request.remote_addr} {request.headers.get('User-Agent')}")

    response = jsonify(getSemesters(get_db().cursor()))
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route("/data")
def enrollmentData():
    app.logger.info(f"/data {request.remote_addr} {request.headers.get('User-Agent')}")

    args = request.args
    courses = getCourses(get_db().cursor(), semesterName=args['semester'], courseCode=args['code'])

    jcourses = []
    for c in courses:
        jcourses.append(
            {
                "section": c.section,
                "number": c.courseNumber,
                "modality": c.modality,
                "title": c.title,
                "ge": c.ge,
                "units": c.units,
                "type": c.type,
                "days": c.days,
                "times": c.times,
                "instructor": c.instructor,
                "location": c.location,
                "dates": c.dates,
                "seats": [{"d": s[0], "n":s[1]} for s in getSeatData(get_db().cursor(), uuid=c.uuid)]
            }
        )

    response = jsonify(jcourses)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/')
def webpage():
    app.logger.info(f"/ {request.remote_addr} {request.headers.get('User-Agent')}")

    return send_file('index.html')

@app.route('/indexHelper.js')
def helperjs():
    app.logger.info(f"/indexHelper.js {request.remote_addr} {request.headers.get('User-Agent')}")

    return send_file('indexHelper.js')

if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=80)
    # serve(app, host='127.0.0.1', port=8000)
