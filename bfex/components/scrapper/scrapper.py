from bs4 import BeautifulSoup
import requests
import json
import re

# this should be done with a real service but
# I do not know how that will work yet
data = json.load(open(r'../../../../faculty.json'))

base_url = "https://www.ualberta.ca/science/about-us/contact-us/faculty-directory/"

for item in data:
    name_from_json = item['name']
    name_from_json = re.sub('[.]', '', name_from_json)
    name_list = re.findall('[A-Z][^A-Z]*', name_from_json)
    formated_name = "-".join(name_list).lower()

    # concatenate names into url
    url = base_url + formated_name

    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    links = soup.find_all("a")
    for link in links:
        try:
            if 'orcid' in link.attrs['href']:
                print(formated_name)
                print("    "+"ORCID ID")
                print("    "+link.attrs['href'])
            if "researcherid" in link.attrs['href']:
                print(formated_name)
                print("    "+"ResearcherID")
                print("    "+link.attrs['href'])
        except KeyError:
            # not all 'a' tags have the links we want
            pass
