import os
from selenium import webdriver
import time
import csv


#####################################################################################################
# CODE BY DEAN ALLEN, DEVELOPED FOR RPS                                                             #
# FEB 10, 2020                                                                                      #
# ###################################################################################################

# get info from text file
os.chdir('..')
with open('userInfo.txt', 'r') as file:
    info = [line.strip() for line in file]


# scroller function
def scroller2(numberOfConnections):
    # iterate scrolls by number of connecitons/40
    for i in range(numberOfConnections//40 + 1):
        print("loader count:", i)
        # scroll to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # wait
        time.sleep(1.5)
        # scroll up a little bit
        driver.execute_script("window.scrollBy(0, -45);")
        # wait
        time.sleep(1)


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
username.send_keys(info[0])
###############################################################



# locate password form by_class_name
password = driver.find_element_by_name('session_password')



###############################################################CHANGE PASSWORD BELOW
password.send_keys(info[1])
###############################################################
# locate submit button by_class_name
log_in_button = driver.find_element_by_class_name('sign-in-form__submit-btn')

# .click() to mimic button click
log_in_button.click()

# goto connections
driver.get('https://www.linkedin.com/mynetwork/invite-connect/connections/')

# connections
numberOfConnections = int(driver.find_element_by_class_name('mn-connections__header').text.split(" ")[0])

# scroll to bottom to load all connections
scroller2(numberOfConnections)

# get user links and put into a list
connections = driver.find_elements_by_class_name('mn-connection-card__link')

# create a set of urls so no duplicates
urls = set()

# add all connection link to url set
for a in connections:
    urls.add(a.get_attribute('href'))

# wait for everything to load
time.sleep(1)

# load their profile
print(len(urls))
for url in urls:

    try:

        # get the profile URL
        driver.get(url)

        # add a 5 second pause loading each URL
        time.sleep(3)

        print("prifle viewed")

    except:
        print("error, contact not able to viewed")
        pass


# terminates the application
driver.quit()
