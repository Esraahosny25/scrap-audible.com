# -*- coding: utf-8 -*-
"""
Created on Tue Sep 10 13:18:19 2024

@author: israa
"""

#Selenium 

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import pandas as pd
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

#headless Mode
#options = Options()  # Initialize an instance of the Options class
#options.headless = True  # True -> Headless mode activated
#options.add_argument('window-size=1920x1080')  # Set a big window size, so all the data will be displayed


website='https://www.audible.com/adblbestsellers' #website to open 
driverPath="C:\\Users\\israa\\Downloads\\chromedriver-win64\\chromedriver-win64\\chromedriver.exe" #chrome driver path
driver=webdriver.Chrome(driverPath)  #initilize the driver


service = Service(driverPath)
driver = webdriver.Chrome(service = service)


driver.get(website)
#driver.maximize_window()

pagination=driver.find_element(By.XPATH, './/ul[contains(@class,"pagingElements")]')
pages=pagination.find_elements(By.TAG_NAME,"li")
lastPage=int(pages[-2].text)

titles=[]
authors=[]
dates=[]
ratings=[]
for page in range(1,lastPage):
    #time.sleep(2) implicit delay
    
    #explicit delay
    container = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, 'adbl-impression-container ')))
    books=WebDriverWait(container, 5).until(EC.presence_of_all_elements_located((By.XPATH, './/li[contains(@class,"productListItem")]')))

    #container=driver.find_element(By.CLASS_NAME,'adbl-impression-container ')
    #books= container.find_elements(By.XPATH, './/li[contains(@class,"productListItem")]')
    
    for book in books:
        titles.append(book.find_element(By.XPATH , './/h3/a').text)
        authors.append(book.find_element(By.XPATH, './/li[contains(@class, "authorLabel")]').text.split(':')[1])
        dates.append(book.find_element(By.XPATH, './/li[contains(@class, "releaseDateLabel")]/span').text.split(':')[1])
        ratingclass=book.find_element(By.CLASS_NAME,'bc-review-stars')
        ratingList=ratingclass.find_elements(By.TAG_NAME, "span")
        ratings.append(f'{len(ratingList)} of 5')
        
    try:
        nextPage=driver.find_element(By.XPATH,'.//span[contains(@class , "nextButton")]')
        nextPage.click()
    except:
        pass
    
    
driver.quit()
df_books= pd.DataFrame({'title': titles, 'author': authors, 'date': dates,'ratings':ratings})
df_books.to_csv('books_pagination.csv', index=False)
