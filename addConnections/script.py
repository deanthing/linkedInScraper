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

# go to connections page
driver.get('https://www.linkedin.com/mynetwork/')

# scroller to load all potential questions
scroller2(500)

# get list
listOfPeople = driver.find_element_by_class_name("js-discover-entity-list__pymk")

# get list elements
items = listOfPeople.find_elements_by_tag_name("li")

# loop through people loaded
for person in items:
    # try do add em, if it fails, it will pass and print "error"
    try:

        # scroll into view
        driver.execute_script("arguments[0].scrollIntoView();", person)

        # click
        person.find_element_by_class_name("artdeco-button--full").click();

        # print name in console
        print(person.find_element_by_class_name("discover-person-card__name").text)

        # sleep
        time.sleep(3.5)

    except:
        print("error")
        pass

# terminates the application
driver.quit()
