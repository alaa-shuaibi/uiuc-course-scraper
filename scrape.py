import sys, requests, json
from bs4 import BeautifulSoup

if len(sys.argv) != 2:
    raise Exception('Exactly 1 argument is required: <SUBJECT>')

subject = sys.argv[1]

data = requests.get('http://catalog.illinois.edu/courses-of-instruction/' + subject)

if data.status_code >= 400:
    print('Status Code: ' + str(data.status_code))
    exit()

html = BeautifulSoup(data.text, 'html.parser')
container = html.find('div', {'class': 'courses'})
courses = {}

for courseblock in container.find_all('div', {'class': 'courseblock'}):
    title = courseblock.find('p', {'class': 'courseblocktitle'}).text
    desc = courseblock.find('p', {'class': 'courseblockdesc'}).text.replace('\xa0', ' ').replace('\n', '')

    name = title[:len(str(subject)) + 4].replace('\xa0', ' ')
    label = title[len(str(subject)) + 7 : title.find('credit:') - 3]
    hours = title[title.find('credit:') + 8 : -2]

    key = name.replace(' ', '').lower()
    courses[key] = {
        'name': name,
        'label': label,
        'hours': hours,
        'description': desc
    }

    # print(name + ' | ' + label + ' | ' + hours)
    # print(desc + '\n')

with open("data/" + subject + '.json', 'w') as outfile:
    json.dump(courses, outfile)