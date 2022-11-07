from bs4 import BeautifulSoup
from datetime import datetime
import os
from helper_classes import Course
from database import processCourse


def fileToEpochDays(path):
  return int(datetime.strptime(path[21:31], '%d_%m_%Y').timestamp() / 60 / 60 / 24)

def fileToUniqueName(path):
  if "spring" in path:
    return "Spring 2023"
  elif "winter" in path:
    return "Winter 2023"
  else:
    raise Exception

def fileToUniquePrefix(path):
  if "spring" in path:
    return 2
  elif "winter" in path:
    return 1
  else:
    raise Exception


def parseTD(uniqueName, uniquePrefix, td) -> Course:
  uuid = int(str(uniquePrefix) + td[1])
  code, section = td[0].replace(" (Section", "").replace(")", "").rsplit(" ", 1)
  section = int(section)
  courseNumber = int(td[1])
  modality = td[2]
  title = td[3]
  ge = td[4]
  units = float(td[5])
  type = td[6]
  days = td[7]
  times = td[8]
  instructor = td[9]
  location = td[10]
  dates = td[11]
  seats = td[12]
  return Course(semesterName=uniqueName, uuid=uuid, code=code, section=section, courseNumber=courseNumber,
                modality=modality, title=title, ge=ge, units=units, type=type, days=days, times=times,
                instructor=instructor, location=location, dates=dates, seats=seats)

def scrapeAndInsert(path, uniqueName, uniquePrefix, epochDays):
  courses = []
  contents = None
  with open(path, 'r') as f:
    contents = f.read()

  soup = BeautifulSoup(contents, "html.parser")
  rows = soup.find("table", {"id": "classSchedule"}).find("tbody").find_all("tr")

  for row in rows:
    l = [td.text.strip() for td in row.find_all("td")]
    if len(l) == 14:
      courses.append(parseTD(uniqueName, uniquePrefix, l))

  for course in courses:
    processCourse(course, epochDays=epochDays)

for filename in os.scandir("pages"):
    if filename.is_file():
        path = filename.path.split("/")[1]
        scrapeAndInsert(filename.path, fileToUniqueName(path), fileToUniquePrefix(path), fileToEpochDays(path))