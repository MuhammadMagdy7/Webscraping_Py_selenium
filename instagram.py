from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver import Chrome
import time
import os
import wget

# Inputs

user = input('Enter your username:')
passuser = input('Enter your password:')
try:
    searchName = input('write what you like to search at Instagram : ')
    block = ['$', '@', '#', '(', ')', '=', '-', '{', '}', '?']
    for i in block:
        if i in searchName:
            print('There is a code that is not allowed ')
            break
except:
    print('Error, try again')
    searchName = input('write what you like to search at Instagram : ')


try:
    ManyImg = int(input('How many imges you want? Enter number please: '))
except:
    print('error, please enter numbers. ')
    ManyImg = input(int('How many imges you want? Enter number please: '))

# Browser

url = 'https://www.instagram.com/'
driver = webdriver.Chrome()
driver.get(url)


# Login

username = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.NAME, 'username')))
password = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.NAME, 'password')))

username.clear()
time.sleep(1)
password.clear()
time.sleep(1)

username.send_keys(user)
time.sleep(1)
password.send_keys(passuser)

# Login Bottom

login = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
    (By.XPATH, '//*[@id="loginForm"]/div/div[3]/button/div')))
login.click()

# Close the window
try:
    NotNow = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
        (By.XPATH, "//button[contains(text(), 'Not Now')]"))).click()
    time.sleep(3)
    NotNow = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
        (By.XPATH, "//button[contains(text(), 'Not Now')]"))).click()
except:
    print('error')


# Search

Search = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
    (By.CSS_SELECTOR, "input[placeholder = 'Search']")))
Search.clear()
time.sleep(2)
keyword = f'#{searchName}'
Search.send_keys(keyword)
Search.send_keys(Keys.ENTER)
Search.clear()

time.sleep(3)

# loop Enter for search
loop = True
while loop:
    if url == driver.current_url:
        Search = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "input[placeholder = 'Search']")))
        Search.send_keys(Keys.ENTER)
    else:
        loop = False

# getting on images

time.sleep(5)
images = driver.find_elements(By.TAG_NAME, 'img')
scroll = 0
while len(images) < ManyImg:
    scroll += 1500
    time.sleep(3)
    driver.execute_script(f"window.scrollTo(0, {scroll})")
    time.sleep(5)
    images = driver.find_elements(By.TAG_NAME, 'img')


# get src

time.sleep(3)
images = [image.get_attribute('src') for image in images]

# create Folder
time.sleep(1)
path = os.getcwd()
path = os.path.join(path, keyword[1:] + 's')
os.mkdir(path)

# filling the folder by images
counter = 0
for image in images:
    save_as = os.path.join(path, keyword[1:] + str(counter) + '.jpg')
    wget.download(image, save_as)
    counter += 1

print('Finish')
driver.quit()
