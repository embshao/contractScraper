#GET JSON OBJECT FOR ONE PAGE
from urllib.request import urlopen as urlReq
from bs4 import BeautifulSoup as soup
import json
import dateutil.parser as parser

data = {}
contract_url = "https://www.sourcewell-mn.gov/cooperative-purchasing/022217-wex"
urlClient = urlReq(contract_url)
page_html = urlClient.read()
urlClient.close()

p_soup = soup(page_html, "html.parser")

container = p_soup.find("div", {"class": "vendor-contract-header__content"})
data['title'] = container.findAll('p')[0].text
str = container.findAll('p')[1].text.split('\n')
date = str[1].split('Maturity Date:')[1].strip()
data['expiration'] = parser.parse(date).isoformat()
str = str[0].replace('#','')
data['contract_number'] = str
name = str.split('-')[1]

files = {}
files["contract-forms"] = p_soup.findAll("div", {"class": "field--item"})[2].findAll('span')[3].a["href"]
data["files"] = [files]

vendor = {}
contacts = {}
vendor["name"] =  name
c_content = p_soup.find("div", {"id": "tab-contact-information"})
c_content = c_content.article.div.findAll('div')
contacts['name'] = c_content[0].text
contacts['phone'] = c_content[1].findAll("div")[1].text.strip()
contacts['email'] = c_content[6].text
vendor['contacts'] = [contacts]
data['vendor'] = vendor

with open("data_file.json", "w") as write_file:
    json.dump(data, write_file)