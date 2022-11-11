from flask import Flask, request, jsonify
from waitress import serve
import logging
from database import getSemesters, getCourseCodes, getCourses, getSeatData

logging.basicConfig(filename='flask_app.log', level=logging.DEBUG, format='%(asctime)s %(levelname)s : %(message)s')
app = Flask(__name__)

@app.route("/coursecodes")
def courseCodes():
    app.logger.info("\n"+str(request.headers))

    response = jsonify(getCourseCodes())
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route("/semesters")
def semesters():
    app.logger.info("\n"+str(request.headers))

    response = jsonify(getSemesters())
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route("/data")
def enrollmentData():
    app.logger.info("\n"+str(request.headers))

    args = request.args
    courses = getCourses(semesterName=args['semester'], courseCode=args['code'])

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
                "seats": [{"d": s[0], "n":s[1]} for s in getSeatData(uuid=c.uuid)]
            }
        )

    response = jsonify(jcourses)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=80)
