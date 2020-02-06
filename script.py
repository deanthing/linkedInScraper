from selenium import webdriver
import time
import csv
import pandas as pd
from parsel import Selector


# CODE BY DEAN ALLEN for RPS
# FEB 6TH, 2020
# EDIT LINES 42 AND 48 TO EDIT EMAIL AND PASSWORD FOR LINKED

# this functino scrolls the webpage to the bottom when called
def scroller():
    SCROLL_PAUSE_TIME = 0.5

    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height


# specifies the path to the chromedriver.exe
driver = webdriver.Chrome('/usr/local/bin/chromedriver')

# driver.get method() will navigate to a page given by the URL address
driver.get('https://www.linkedin.com')

# sleep to make sure everything loads
time.sleep(2)

# locate email form by_class_name
username = driver.find_element_by_name('session_key')

###############################################################CHANGE USERNAME BELOW
# CHANGE USERNAME/EMAIL HERE
username.send_keys('ur email here')
###############################################################



# locate password form by_class_name
password = driver.find_element_by_name('session_password')



###############################################################CHANGE PASSWORD BELOW
password.send_keys('ur pass here')
###############################################################
# locate submit button by_class_name
log_in_button = driver.find_element_by_class_name('sign-in-form__submit-btn')

# .click() to mimic button click
log_in_button.click()

# goto connections
driver.get('https://www.linkedin.com/mynetwork/invite-connect/connections/')

# scroll to bottom to load all connections
scroller()

# get user links and put into a list
connections = driver.find_elements_by_class_name('mn-connection-card__link')

# create a set of urls so no duplicates
urls = set()

# add all connection link to url set
for a in connections:
    urls.add(a.get_attribute('href'))

# sleep for a little to be confuse algorithms
time.sleep(0.5)

# initialize vars
leads = []
first = ""
last = ""
email = ""
namesSplit = ""
title = ""
for url in urls:

    try:

        # get the profile URL
        driver.get(url)

        # add a 5 second pause loading each URL
        time.sleep(0.5)

        #  names, split first and last
        name = driver.find_element_by_class_name('t-24').text
        namesSplit = name.split()
        last = namesSplit[-1]
        first = namesSplit[:-1]
        first = ' '.join(first)

        # title
        title = driver.find_element_by_class_name('t-18').text

        # get email
        try:
            driver.get(url + 'detail/contact-info/')
            time.sleep(0.5)
            email = driver.find_element_by_class_name('ci-email').text.split()[-1]
        except:
            email = "No eMail found"

        leads.append({'first': first, 'last': last, 'org': title, 'email': email})

        csvLead = [first, last, title, email]

        with open('leads.csv', 'a') as f:
            writer = csv.writer(f)
            writer.writerow(csvLead)

        print("name", name)
        print("title", title)
        print("email", email)

        time.sleep(0.5)
    except:
        print("error, contact not able to saved")
        pass

# remove duplicates


with open('leads.csv','r') as in_file, open('noDuplicates.csv','w') as out_file:
    seen = set() # set for fast O(1) amortized lookup
    for line in in_file:
        if line in seen: continue # skip duplicate
        seen.add(line)
        out_file.write(line)
# terminates the application
driver.quit()
