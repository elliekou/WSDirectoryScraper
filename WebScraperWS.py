import csv
from bs4 import BeautifulSoup
import requests
import re

#import into CSV
rowList = ["Company Type", "Company Name", "Address", "City", "State", "Zip", "Phone Number", "Website"]
with open("winstonsalem.csv", "w", newline= '') as file:
    writer = csv.writer(file)
    writer.writerow(rowList)

#grabbing the html for winston chamber of commerce
#using the request library

url = "https://members.winstonsalem.com/memberdirectory?action=Listing"
result = requests.get(url)

#using Bs4 to parse the request

doc = BeautifulSoup(result.text, "html.parser")

#Class name in regular expression
pattern = re.compile(r"card-title gz-card-title")

directories = doc.find_all(["h5"], class_ = pattern)
print(directories)

for directory in directories:
    #get url to next page
    url = directory.find(["a"])["href"]
    companyType = url
    print(companyType)

    result = requests.get(url)
    doc = BeautifulSoup(result.text, "html.parser")

    infoboxes = doc.find_all(["div"], class_ = "card-body gz-directory-card-body")

    for infobox in infoboxes:

        #grabs company name from header
        header_info = infobox.find(["h5"], class_ = "card-title gz-card-title")

        company_name = header_info.find(attrs={"alt" : True})

        if company_name == None:
            continue

        #grabs the address from card body

        body_info = infobox.find(["li"], class_="list-group-item gz-card-address")

        try:
            street_address = body_info.find(["span"], itemprop="streetAddress")
        except:
            street_address = None

        try:
            city_addy = body_info.find(["span"], itemprop="addressLocality")
        except:
            city_addy = None

        try:
            state_addy = body_info.find(["span"], itemprop="addressRegion")
        except:
            state_addy = None

        try:
            zip_code = body_info.find(["span"], itemprop="postalCode")
        except:
            zip_code = None

        try:
            address_info = body_info.find_all(["span"])
        except:
            address_info = None

        
        #validate and keep program running
        if street_address == None:
            continue
        if city_addy == None:
            continue
        if state_addy == None:
            continue
        if zip_code == None:
            continue
        if address_info == None:
            continue

        #get phone number
        body_info = infobox.find(["li"], class_="list-group-item gz-card-phone")

        try:
            phone_number = body_info.find(["span"], itemprop="telephone")
        except:
            phone_number = None

        #validate
        if phone_number == None:
            continue

        #phonenum = phone_number.span

        print(address_info)

        company = company_name["alt"]
        street = street_address.text
        city = city_addy.text
        state = state_addy.text
        zip = zip_code.text
        phone = phone_number.text

        print(company, street, city, state, zip, phone)

        #grab the website
        body_info = infobox.find(["li"], class_="list-group-item gz-card-website")
        
        try:
            url = body_info.find(["a"])["href"]
            result = requests.get(url)
            doc = BeautifulSoup(result.text, "html.parser")
            website = url
        except:
            website = None

        rowList = [companyType, " ", company, street, city, state, zip, phone, website]
        print(rowList)
        with open("winstonsalem.csv", "a", newline= '') as file:
            writer = csv.writer(file)
            writer.writerow(rowList)
