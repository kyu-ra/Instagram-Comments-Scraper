import time
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains

service = webdriver.FirefoxService(executable_path="path_to_geckodriver")
driver = webdriver.Firefox(service=service)
url="https://www.instagram.com/"

driver.get(url) 
time.sleep (2)

username = driver.find_element(By.NAME,"email")
username.send_keys("USERNAME")

password = driver.find_element (By.NAME,"pass")
password.send_keys("PASSWORD")
password.submit()

wait = WebDriverWait(driver, timeout=20)
wait.until(EC.visibility_of_element_located((By.XPATH, "//*[text()='Save info']")))
# Submits "save info" button
driver.find_element(By.XPATH, "//*[text()='Save info']").click()


driver.get(sys.argv[1])
time.sleep(4)

# load "sys.argv[2]" number of comments 
""" try:
    load_more_comment = driver.find_element(By.XPATH,'/html/body/div[2]/div/div/div[2]/div/div/div/div[1]/div[1]/div[2]/section/main/div/div[1]/div/div[2]/div/div[2]/div/div/ul/li/div/button')
    print("Found {}".format(str(load_more_comment)))
    i = 0
    while load_more_comment.is_displayed() and i < int(sys.argv[2]):
        load_more_comment.click()
        time.sleep(7)
        load_more_comment = driver.find_element(By.XPATH,'/html/body/div[2]/div/div/div[2]/div/div/div/div[1]/div[1]/div[2]/section/main/div/div[1]/div/div[2]/div/div[2]/div/div/ul/li/div/button')
        print(i)
        print("Found {}".format(str(load_more_comment)))
        i += 1
except Exception as e:
    print(e)
    pass """

# Need to rewrite the above method to accomodate for instagram's infinite scroll to read comments
# Change sys.argv[2] to look at output number and not read more number, or something

comments = driver.find_element(By.CSS_SELECTOR, ".x5yr21d.xw2csxc.x1odjw0f.x1n2onr6")
comments.click()

# Scrolling the main window and not the correct element
for i in range(1,100):
   driver.execute_script(f"arguments[0].scrollTo(0,{i});", comments)
   # when do we stop ?

# Scrapes the comments
# These class names are outdated too........
user_names = []
user_comments = []
comment = driver.find_elements(By.CLASS_NAME,'_a9ym')
for c in comment:
    container = c.find_element(By.CLASS_NAME,'_a9zr')
    name = container.find_element(By.CLASS_NAME,'_a9zc').text
    content = container.find_element(By.TAG_NAME,'span').text
    content = content.replace('\n', ' ').strip().rstrip()
    user_names.append(name)
    user_comments.append(content)

user_names.pop(0)
user_comments.pop(0)
# print(user_names)
# print(user_comments)
import excel_exporter
excel_exporter.export(user_names, user_comments)

driver.close()
