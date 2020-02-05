from selenium import webdriver
import time
import csv
from parsel import Selector


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

time.sleep(3)

# locate email form by_class_name
username = driver.find_element_by_name('session_key')

# send_keys() to simulate key strokes
username.send_keys('')

# locate password form by_class_name
password = driver.find_element_by_name('session_password')

# send_keys() to simulate key strokes
password.send_keys('')

# locate submit button by_class_name
log_in_button = driver.find_element_by_class_name('sign-in-form__submit-btn')

# .click() to mimic button click
log_in_button.click()

# goto connections
driver.get('https://www.linkedin.com/mynetwork/invite-connect/connections/')

# scroll
scroller()

# get user links
connections = driver.find_elements_by_class_name('mn-connection-card__link')

urls = set()

for a in connections:
    urls.add(a.get_attribute('href'))

time.sleep(0.5)

leads = []

for url in urls:
    # get the profile URL
    driver.get(url)

    # add a 5 second pause loading each URL
    time.sleep(0.5)

    #  names
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
        email = ""

    leads.append({'first': first, 'last': last, 'org': title, 'email': email})

    print("name", name)
    print("title", title)
    print("email", email)

    time.sleep(0.5)


# write to file
with open('leads.csv', mode='w') as csv_file:
    writer = csv.writer(csv_file)
    for lead in leads:
        writer.writerow([lead['first'], lead['last'], lead['org'], lead['email']])



# terminates the application
driver.quit()
