import logging
from typing import List
from helper_classes import Semester, Course
from scrapers import ScraperWinter2023, ScraperSpring2023
from database import processCourse

semesters = [
  Semester(scraper=ScraperWinter2023(), startRecording="10/12/2022", endRecording="1/5/2023"),
  Semester(scraper=ScraperSpring2023(), startRecording="10/24/2022", endRecording="2/20/2023"),
]

logging.basicConfig(filename='periodic.log', level=logging.DEBUG, format='%(asctime)s %(levelname)s : %(message)s')

def validateUniqueSemesters():
  lp = []
  for sem in semesters:
    if sem.scraper.uniquePrefix in lp:
      logging.error("A uniquePrefix must be set in the AbstractScraper subclass.")
      raise Exception("A uniquePrefix must be set in the AbstractScraper subclass.")
    lp.append(sem.scraper.uniquePrefix)

  ln = []
  for sem in semesters:
    if sem.scraper.uniqueName in ln:
      logging.error("A uniqueName must be set in the AbstractScraper subclass.")
      raise Exception("A uniqueName must be set in the AbstractScraper subclass.")
    ln.append(sem.scraper.uniqueName)


if __name__ == "__main__":
  validateUniqueSemesters()
  for sem in semesters:
    if sem.isActive():
      courses: List[Course] = sem.scraper.scrape()
      logging.info(f'{sem.scraper.uniqueName}: scraped {len(courses)} courses.')
      for course in courses:
        processCourse(course)
      logging.info(f'{sem.scraper.uniqueName}: inserted courses into db.')
