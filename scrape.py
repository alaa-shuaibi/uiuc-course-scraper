import argparse, requests, json
from bs4 import BeautifulSoup

parser = argparse.ArgumentParser()
parser.add_argument("--subject")
args = parser.parse_args()

data = requests.get('http://catalog.illinois.edu/courses-of-instruction/' + str(args.subject))

if data.status_code >= 400:
    print('Status Code: ' + str(data.status_code))
    exit()

html = BeautifulSoup(data.text, 'html.parser')
container = html.find('div', {'class': 'courses'})
courses = {}

for courseblock in container.find_all('div', {'class': 'courseblock'}):
    title = courseblock.find('p', {'class': 'courseblocktitle'}).text
    desc = courseblock.find('p', {'class': 'courseblockdesc'}).text.replace('\xa0', ' ').replace('\n', '')

    name = title[:len(str(args.subject)) + 4].replace('\xa0', ' ')
    label = title[len(str(args.subject)) + 7 : title.find('credit:') - 3]
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

with open(args.subject + '.json', 'w') as outfile:
    json.dump(courses, outfile)