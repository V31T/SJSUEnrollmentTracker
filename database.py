import sqlite3
import time
from helper_classes import Course
from typing import List

DATABASE_FILE_PATH = "courses.db"

COURSE_INFO_TABLE = "courseInfo"
SEMESTER_TABLE = "semester_id"
CODE_TABLE = "code_id"
MODALITY_TABLE = "modality_id"
TITLE_TABLE = "title_id"
GE_TABLE = "ge_id"
TYPE_TABLE = "type_id"
DAYS_TABLE = "days_id"
TIMES_TABLE = "times_id"
INSTRUCTOR_TABLE = "instructor_id"
DATES_TABLE = "dates_id"

SEAT_HISTORY_TABLE = "seatHistory"

connection = sqlite3.connect(DATABASE_FILE_PATH, check_same_thread=False) #TODO: turning off the checking might be a bad idea
cursor = connection.cursor()

cursor.execute(f'''
  CREATE TABLE IF NOT EXISTS {SEMESTER_TABLE} 
  (id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT,
  UNIQUE(name));
''')
cursor.execute(f'''
  CREATE TABLE IF NOT EXISTS {CODE_TABLE} 
  (id INTEGER PRIMARY KEY AUTOINCREMENT,
  code TEXT,
  UNIQUE(code));
''')
cursor.execute(f'''
  CREATE TABLE IF NOT EXISTS {MODALITY_TABLE} 
  (id INTEGER PRIMARY KEY AUTOINCREMENT,
  modality TEXT,
  UNIQUE(modality));
''')
cursor.execute(f'''
  CREATE TABLE IF NOT EXISTS {TITLE_TABLE} 
  (id INTEGER PRIMARY KEY AUTOINCREMENT,
  title TEXT,
  UNIQUE(title));
''')
cursor.execute(f'''
  CREATE TABLE IF NOT EXISTS {GE_TABLE} 
  (id INTEGER PRIMARY KEY AUTOINCREMENT,
  ge TEXT,
  UNIQUE(ge));
''')
cursor.execute(f'''
  CREATE TABLE IF NOT EXISTS {TYPE_TABLE} 
  (id INTEGER PRIMARY KEY AUTOINCREMENT,
  type TEXT,
  UNIQUE(type));
''')
cursor.execute(f'''
  CREATE TABLE IF NOT EXISTS {DAYS_TABLE} 
  (id INTEGER PRIMARY KEY AUTOINCREMENT,
  days TEXT,
  UNIQUE(days));
''')
cursor.execute(f'''
  CREATE TABLE IF NOT EXISTS {TIMES_TABLE} 
  (id INTEGER PRIMARY KEY AUTOINCREMENT,
  times TEXT,
  UNIQUE(times));
''')
cursor.execute(f'''
  CREATE TABLE IF NOT EXISTS {INSTRUCTOR_TABLE} 
  (id INTEGER PRIMARY KEY AUTOINCREMENT,
  instructor TEXT,
  UNIQUE(instructor));
''')
cursor.execute(f'''
  CREATE TABLE IF NOT EXISTS {DATES_TABLE} 
  (id INTEGER PRIMARY KEY AUTOINCREMENT,
  dates TEXT,
  UNIQUE(dates));
''')
# Create the course information table if it does not exist already.
cursor.execute(f'''
  CREATE TABLE IF NOT EXISTS {COURSE_INFO_TABLE} 
  (uuid INTEGER PRIMARY KEY,
  semesterNameID INTEGER,
  codeID INTEGER,
  section INTEGER,
  courseNumber INTEGER,
  modalityID INTEGER,
  titleID INTEGER,
  geID INTEGER,
  units REAL,
  typeID INTEGER,
  daysID INTEGER,
  timesID INTEGER,
  instructorID INTEGER,
  location TEXT,
  datesID INTEGER);
''')


# Create the seat history table if it does not exist already. Ensure that a course cannot have multiple entries for the same day.
cursor.execute(f'''
  CREATE TABLE IF NOT EXISTS {SEAT_HISTORY_TABLE} 
  (uuid INTEGER,
  seats INTEGER,
  epochDay INTEGER,
  UNIQUE(uuid, epochDay));
''')

def semesterNameToId(name: str):
  l = cursor.execute(f'''
      SELECT id
      FROM {SEMESTER_TABLE}
      WHERE name=?
    ''', [name]).fetchone()
  return l[0] if l is not None else None

def idToSemesterName(id: int):
  l = cursor.execute(f'''
      SELECT name
      FROM {SEMESTER_TABLE}
      WHERE id=?
    ''', [id]).fetchone()
  return l[0] if l is not None else None

def codeToId(code: str):
  l = cursor.execute(f'''
      SELECT id
      FROM {CODE_TABLE}
      WHERE code=?
    ''', [code]).fetchone()
  return l[0] if l is not None else None

def idToCode(id: int):
  l = cursor.execute(f'''
      SELECT code
      FROM {CODE_TABLE}
      WHERE id=?
    ''', [id]).fetchone()
  return l[0] if l is not None else None

def modalityToId(modality: str):
  l = cursor.execute(f'''
      SELECT id
      FROM {MODALITY_TABLE}
      WHERE modality=?
    ''', [modality]).fetchone()
  return l[0] if l is not None else None

def idToModality(id: int):
  l = cursor.execute(f'''
      SELECT modality
      FROM {MODALITY_TABLE}
      WHERE id=?
    ''', [id]).fetchone()
  return l[0] if l is not None else None

def titleToId(title: str):
  l = cursor.execute(f'''
      SELECT id
      FROM {TITLE_TABLE}
      WHERE title=?
    ''', [title]).fetchone()
  return l[0] if l is not None else None

def idToTitle(id: int):
  l = cursor.execute(f'''
      SELECT title
      FROM {TITLE_TABLE}
      WHERE id=?
    ''', [id]).fetchone()
  return l[0] if l is not None else None

def geToId(ge: str):
  l = cursor.execute(f'''
      SELECT id
      FROM {GE_TABLE}
      WHERE ge=?
    ''', [ge]).fetchone()
  return l[0] if l is not None else None

def idToGe(id: int):
  l = cursor.execute(f'''
      SELECT ge
      FROM {GE_TABLE}
      WHERE id=?
    ''', [id]).fetchone()
  return l[0] if l is not None else None

def typeToId(type: str):
  l = cursor.execute(f'''
      SELECT id
      FROM {TYPE_TABLE}
      WHERE type=?
    ''', [type]).fetchone()
  return l[0] if l is not None else None

def idToType(id: int):
  l = cursor.execute(f'''
      SELECT type
      FROM {TYPE_TABLE}
      WHERE id=?
    ''', [id]).fetchone()
  return l[0] if l is not None else None

def daysToId(days: str):
  l = cursor.execute(f'''
      SELECT id
      FROM {DAYS_TABLE}
      WHERE days=?
    ''', [days]).fetchone()
  return l[0] if l is not None else None

def idToDays(id: int):
  l = cursor.execute(f'''
      SELECT days
      FROM {DAYS_TABLE}
      WHERE id=?
    ''', [id]).fetchone()
  return l[0] if l is not None else None

def timesToId(times: str):
  l = cursor.execute(f'''
      SELECT id
      FROM {TIMES_TABLE}
      WHERE times=?
    ''', [times]).fetchone()
  return l[0] if l is not None else None

def idToTimes(id: int):
  l = cursor.execute(f'''
      SELECT times
      FROM {TIMES_TABLE}
      WHERE id=?
    ''', [id]).fetchone()
  return l[0] if l is not None else None

def instructorToId(instructor: str):
  l = cursor.execute(f'''
      SELECT id
      FROM {INSTRUCTOR_TABLE}
      WHERE instructor=?
    ''', [instructor]).fetchone()
  return l[0] if l is not None else None

def idToInstructor(id: int):
  l = cursor.execute(f'''
      SELECT instructor
      FROM {INSTRUCTOR_TABLE}
      WHERE id=?
    ''', [id]).fetchone()
  return l[0] if l is not None else None

def datesToId(dates: str):
  l = cursor.execute(f'''
      SELECT id
      FROM {DATES_TABLE}
      WHERE dates=?
    ''', [dates]).fetchone()
  return l[0] if l is not None else None

def idTodates(id: int):
  l = cursor.execute(f'''
      SELECT dates
      FROM {DATES_TABLE}
      WHERE id=?
    ''', [id]).fetchone()
  return l[0] if l is not None else None

def processCourse(c: Course, epochDays=None):
  # enter the ids into id tables
  cursor.execute(f'INSERT OR IGNORE INTO {SEMESTER_TABLE} (name) VALUES (?)', [c.semesterName])
  cursor.execute(f'INSERT OR IGNORE INTO {CODE_TABLE} (code) VALUES (?)', [c.code])
  cursor.execute(f'INSERT OR IGNORE INTO {MODALITY_TABLE} (modality) VALUES (?)', [c.modality])
  cursor.execute(f'INSERT OR IGNORE INTO {TITLE_TABLE} (title) VALUES (?)', [c.title])
  cursor.execute(f'INSERT OR IGNORE INTO {GE_TABLE} (ge) VALUES (?)', [c.ge])
  cursor.execute(f'INSERT OR IGNORE INTO {TYPE_TABLE} (type) VALUES (?)', [c.type])
  cursor.execute(f'INSERT OR IGNORE INTO {DAYS_TABLE} (days) VALUES (?)', [c.days])
  cursor.execute(f'INSERT OR IGNORE INTO {TIMES_TABLE} (times) VALUES (?)', [c.times])
  cursor.execute(f'INSERT OR IGNORE INTO {INSTRUCTOR_TABLE} (instructor) VALUES (?)', [c.instructor])
  cursor.execute(f'INSERT OR IGNORE INTO {DATES_TABLE} (dates) VALUES (?)', [c.dates])

  connection.commit()

  # Insert the course information into the course info table if it needs to be updated or is not there.
  cursor.execute(f'''
    REPLACE INTO {COURSE_INFO_TABLE}
    (semesterNameID, uuid, codeID, section, courseNumber, modalityID, titleID, geID, units, typeID, daysID, timesID, instructorID, location, datesID)
    VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);
  ''', [semesterNameToId(c.semesterName), c.uuid, codeToId(c.code), c.section, c.courseNumber, modalityToId(c.modality), titleToId(c.title), geToId(c.ge), c.units, typeToId(c.type), daysToId(c.days), timesToId(c.times), instructorToId(c.instructor), c.location, datesToId(c.dates)])

  # Insert the seat information into the seat history table along with the current day and course uuid.
  if epochDays is None:
    epochDays = int(time.time() / 60 / 60 / 24)
  cursor.execute(f'''
    INSERT OR IGNORE INTO {SEAT_HISTORY_TABLE}
    (uuid, seats, epochDay)
    VALUES (?,?,?);
  ''', [c.uuid, c.seats, epochDays])

  connection.commit()

def getSemesters() -> list:
  l = cursor.execute(f'''
      SELECT name
      FROM {SEMESTER_TABLE}
    ''').fetchall()
  semesters = [t[0] for t in l]
  return semesters

def getCourseCodes() -> list:
  l = cursor.execute(f'''
        SELECT code
        FROM {CODE_TABLE}
      ''').fetchall()
  codes = [t[0] for t in l]
  return codes

def getCourses(semesterName: str) -> List[Course]:
  l = cursor.execute(f'''
    SELECT semesterNameID, uuid, codeID, section, courseNumber, modalityID, titleID, geID, units, typeID, daysID, timesID, instructorID, location, datesID 
    FROM {COURSE_INFO_TABLE}
    WHERE semesterNameID=?;
  ''', [semesterNameToId(semesterName)]).fetchall()
  courses = [Course(idToSemesterName(c[0]), c[1], idToCode(c[2]), c[3], c[4], idToModality(c[5]), idToTitle(c[6]), idToGe(c[7]), c[8], idToType(c[9]), idToDays(c[10]), idToTimes(c[11]), idToInstructor(c[12]), c[13], idTodates(c[14]), -1) for c in l]
  return courses

def getCourses(semesterName: str, courseCode: str) -> List[Course]:
  l = cursor.execute(f'''
    SELECT semesterNameID, uuid, codeID, section, courseNumber, modalityID, titleID, geID, units, typeID, daysID, timesID, instructorID, location, datesID 
    FROM {COURSE_INFO_TABLE}
    WHERE semesterNameID=? AND codeID=?;
  ''', [semesterNameToId(semesterName), codeToId(courseCode)]).fetchall()
  courses = [Course(idToSemesterName(c[0]), c[1], idToCode(c[2]), c[3], c[4], idToModality(c[5]), idToTitle(c[6]), idToGe(c[7]), c[8], idToType(c[9]), idToDays(c[10]), idToTimes(c[11]), idToInstructor(c[12]), c[13], idTodates(c[14]), -1) for c in l]
  return courses

def getAllCourses() -> List[Course]:
  l = cursor.execute(f'''
    SELECT semesterNameID, uuid, codeID, section, courseNumber, modalityID, titleID, geID, units, typeID, daysID, timesID, instructorID, location, datesID 
    FROM {COURSE_INFO_TABLE};
  ''').fetchall()
  courses = [Course(idToSemesterName(c[0]), c[1], idToCode(c[2]), c[3], c[4], idToModality(c[5]), idToTitle(c[6]), idToGe(c[7]), c[8], idToType(c[9]), idToDays(c[10]), idToTimes(c[11]), idToInstructor(c[12]), c[13], idTodates(c[14]), -1) for c in l]
  return courses

def getSeatData(uuid: int) -> list:
  l = cursor.execute(f'''
    SELECT epochDay, seats
    FROM {SEAT_HISTORY_TABLE}
    WHERE uuid=?
    ORDER BY epochDay ASC;
  ''', [uuid]).fetchall()
  return l
