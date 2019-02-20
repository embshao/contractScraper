#GET JSON OBJECTS FOR ALL CONTRACTS
from urllib.request import urlopen as urlReq #grab page
from bs4 import BeautifulSoup as soup #parse txt
import json
import dateutil.parser as parser
from urllib.request import Request
from socket import timeout
import logging

pageNames = []
numPages = 9
header = { 'User-Agent': 'CoProcure Technical Challenge'}

for x in range(0, numPages):
    basePageUrl = 'https://www.sourcewell-mn.gov/contract-search?category=All&keyword=&page=' + str(x)
    urlClient = urlReq(basePageUrl)
    page_html = urlClient.read()
    urlClient.close()
    p_soup = soup(page_html, "html.parser")
    container = p_soup.findAll("p", {"class":"component__search-vendors-contracts-number"})

    for n in container:
        pageNames.append(n.text.replace('#','').strip())

contract_data = []

for i in pageNames:
    data = {}
    contract_url = "https://www.sourcewell-mn.gov/cooperative-purchasing/" + i
    req = Request( contract_url, headers=header)
    try:
        urlClient = urlReq(contract_url, timeout=10)
        page_html = urlClient.read().decode('utf-8')
    except timeout:
        logging.error('socket timed out - URL %s', url)
    else:
        logging.info('Access successful.')
    urlClient.close()
    
    psoup = soup(page_html, "html.parser")
    
    #title, expiration, contractnumber, name
    container = psoup.find("div", {"class": "vendor-contract-header__content"})
    data['title'] = container.findAll('p')[0].text
    istr = container.findAll('p')[1].text.split('\n')
    date = istr[1].split('Maturity Date:')[1].strip()
    data['expiration'] = parser.parse(date).isoformat()
    istr = istr[0].replace('#','')
    data['contract_number'] = istr
    name = istr.split('-')[1]
    
    #files
    files = {}
    files["contract-forms"] = psoup.findAll("div", {"class": "field--item"})[2].findAll('span')[3].a["href"]
    data["files"] = [files]
    
    #vendor
    vendor = {}
    contacts = {}
    vendor["name"] =  name
    c_content = psoup.find("div", {"id": "tab-contact-information"})
    c_content = c_content.article.div.findAll('div')
    contacts['name'] = c_content[0].text
    contacts['phone'] = c_content[1].findAll("div")[1].text.strip()
    contacts['email'] = c_content[6].text
    vendor['contacts'] = [contacts]
    data['vendor'] = vendor
    
    contract_data.append(data)
    
with open("contract_data.json", "w") as write_file:
    json.dump(contract_data, write_file)