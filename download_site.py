import requests
from datetime import date

d = date.today().strftime("winter_schedule_page_%d_%m_%Y")
# d = date.today().strftime("spring_schedule_page_%d_%m_%Y")

page = requests.get(url="https://www.sjsu.edu/classes/schedules/winter-2023.php").text
# page = requests.get(url="https://www.sjsu.edu/classes/schedules/spring-2023.php").text

with open(f"pages/{d}.txt", "w") as f:
  f.write(page)