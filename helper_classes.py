from dataclasses import dataclass
from typing import Type, Callable
import time


@dataclass
class Course:
  semesterName: str
  uuid: int  # combine courseNumber with an integer named uniquePrefix in each Scrapper Subclass
  code: str
  section: int
  courseNumber: int
  modality: str
  title: str
  ge: str
  units: float
  type: str
  days: str
  times: str
  instructor: str
  location: str
  dates: str
  seats: int


@dataclass
class Semester:
  scraper: Callable
  startRecording: str
  endRecording: str

  def isActive(self) -> bool:
    start = int(time.mktime(time.strptime(self.startRecording, "%m/%d/%Y")))
    end = int(time.mktime(time.strptime(self.endRecording, "%m/%d/%Y")))
    now = int(time.time())
    return start <= now and now <= end

