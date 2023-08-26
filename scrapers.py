from typing import List
import requests
from bs4 import BeautifulSoup
from helper_classes import Course


class AbstractScraper:
  uniqueName = ""
  url: str = ""
  uniquePrefix: int = -1

  def scrape(self) -> List[Course]:
    courses: List[Course] = []

    for row in self.getRows():
      l = [td.text.strip() for td in row.find_all("td")]

      if len(l) == 14:
        try:
          courses.append(self.parseTD(l))
        except:
          print("Could not process course: ", l)

    return courses

  def parseTD(self, td: List[str]) -> Course:
    raise Exception("Must override this abstract function.")
    return Course()

  def getPageContent(self):
    return requests.get(self.url).content

  def getRows(self):
    soup = BeautifulSoup(self.getPageContent(), "html.parser")
    rows = soup.find("table", {"id": "classSchedule"}).find("tbody").find_all("tr")
    return rows


class ScraperWinter2023(AbstractScraper):
  uniqueName = "Winter 2023"
  url = "https://www.sjsu.edu/classes/schedules/winter-2023.php"
  uniquePrefix = 1

  def parseTD(self, td: List[str]) -> Course:
    uuid = int(str(self.uniquePrefix) + td[1])
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
    return Course(semesterName=self.uniqueName, uuid=uuid, code=code, section=section, courseNumber=courseNumber, modality=modality, title=title, ge=ge, units=units, type=type, days=days, times=times, instructor=instructor, location=location, dates=dates, seats=seats)


class ScraperSpring2023(AbstractScraper):
  uniqueName = "Spring 2023"
  url = "https://www.sjsu.edu/classes/schedules/spring-2023.php"
  uniquePrefix = 2

  # ['AAS 1 (Section 01)', '25135', 'In Person', 'Introduction to Asian American Studies', 'GE: F', '3.0', 'LEC', 'MW', '09:00AM-10:15AM', 'Joanne Rondilla', 'CL234', '01/25/23-05/15/23', '35', 'Must be in compliance with COVID vaccination requirements to enroll in classes meeting In Person or Hybrid Modalities.']
  def parseTD(self, td: List[str]) -> Course:
    uuid = int(str(self.uniquePrefix) + td[1])
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
    return Course(semesterName=self.uniqueName, uuid=uuid, code=code, section=section, courseNumber=courseNumber, modality=modality, title=title, ge=ge, units=units, type=type, days=days, times=times, instructor=instructor, location=location, dates=dates, seats=seats)


class ScraperSummer2023(AbstractScraper):
  uniqueName = "Summer 2023"
  url = "https://www.sjsu.edu/classes/schedules/summer-2023.php"
  uniquePrefix = 3

  def parseTD(self, td: List[str]) -> Course:
    uuid = int(str(self.uniquePrefix) + td[1])
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
    return Course(semesterName=self.uniqueName, uuid=uuid, code=code, section=section, courseNumber=courseNumber, modality=modality, title=title, ge=ge, units=units, type=type, days=days, times=times, instructor=instructor, location=location, dates=dates, seats=seats)


class ScraperFall2023(AbstractScraper):
  uniqueName = "Fall 2023"
  url = "https://www.sjsu.edu/classes/schedules/fall-2023.php"
  uniquePrefix = 4

  def parseTD(self, td: List[str]) -> Course:
    uuid = int(str(self.uniquePrefix) + td[1])
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
    return Course(semesterName=self.uniqueName, uuid=uuid, code=code, section=section, courseNumber=courseNumber, modality=modality, title=title, ge=ge, units=units, type=type, days=days, times=times, instructor=instructor, location=location, dates=dates, seats=seats)
