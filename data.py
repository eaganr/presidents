import urllib
import json

from bs4 import BeautifulSoup as bs

'''
people = ["George Washington", "John Adams", "Thomas Jefferson", "James Madison", "James Monroe",
              "John Quincy Adams", "Andrew Jackson", "Martin Van Buren", "William H. Harrison", "John Tyler",
              "James K. Polk", "Zachary Taylor", "Millard Fillmore", "Franklin Pierce", "James Buchanan",
              "Abraham Lincoln", "Andrew Johnson", "Ulysses S. Grant", "Rutherford B. Hayes", "James A. Garfield",
              "Chester A. Arthur", "Grover Cleveland", "Benjamin Harrison", "William McKinley", "Theodore Roosevelt",
              "William Howard Taft", "Woodrow Wilson", "Warren G. Harding", "Calvin Coolidge", "Herbert Hoover",
              "Franklin D. Roosevelt", "Harry S. Truman", "Dwight D. Eisenhower", "John F. Kennedy", "Lyndon B. Johnson",
              "Richard M. Nixon", "Gerald R. Ford", "James Earl Carter", "Ronald Reagan", "George H. W. Bush",
              "William J. Clinton", "George W. Bush", "Barack H. Obama"]
'''

people = ["Bernie Sanders", "Hillary Clinton", "Ted Cruz", "John Kasich"]

def getLevel(p):
  if "Vice President of the United States" in p:
    return 9
  if "President of the United States" in p:
    return 10
  if "Speaker of the United States House of Representatives" in p:
    return 8
  if "House Minority Leader" in p:
    return 8
  if "Senate Majority Leader" in p:
    return 8
  if "Senate Minority Leader" in p:
    return 8
  #cabinet
  if "United States Secretary of State" in p:
    return 7
  if "First Lady of the United States" in p:
    return 7
  if "United States Secretary of the Treasury" in p:
    return 7
  if "United States Secretary of Defense" in p:
    return 7
  if "United States Secretary Attorney General" in p:
    return 7
  if "Lietenant Governor of" in p:
    return 3
  if "Governor of" in p:
    return 6
  if "United States Senator" in p:
    return 5
  if "U.S. House of Representatives" in p:
    return 4
  #state cabinet
  if "Attorney General of" in p:
    return 3
  if "Solicitor General of" in p:
    return 3
  if "Secretary of State of" in p:
    return 3
  if "First Lady of" in p:
    return 3
  if "Comptroller of" in p:
    return 3
  if "Senate" in p:
    return 2
  if "House of Representatives" in p:
    return 1
  if "Mayor" in p:
    return 0

pdata = []
for pres in people:
  url = "https://en.wikipedia.org/wiki/" + pres.replace(" ", "_")
  html = response = urllib.urlopen(url).read()
  b = bs(html)

  data = {}
  data["name"] = pres
  data["track"] = {}

  def makeOffice():
    try:
      office = {}
      office["office"] = position
      office["level"] = getLevel(position)
      startyear = int(years.split(u" \u2610 ")[0].split(",")[1][1:5])
      data["track"][startyear] = office
    except:
      "skipped: " + pres + " " + position

  rows = b.find("table", {"class":"vcard"}).findAll("tr")
  position = None
  years = None
  for row in rows:
    if "Incumbent" in str(row):
      continue
    if "Chairman of" in str(row):
      makeOffice()
      position = None
      continue
    if "President pro tempore of" in str(row):
      makeOffice()
      position = None
      continue
    if "Personal details" in str(row):
      break
    if "background:lavender" in str(row):
      if position:
        makeOffice()
      position = row.getText()
    if "In office" in str(row) or "Assumed office" in str(row) or "In role" in str(row):
      years = row.getText()[11:]
  makeOffice()
  pdata.append(data)

print json.dumps(pdata)
