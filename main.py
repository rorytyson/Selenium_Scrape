# pip3 install webdriver_manager
from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Input the location of the Chrome Driver on the computer.
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
# driver = webdriver.Chrome('/Users/roryt/Documents/Design/Python Projects/chromedriver')
# Input the web page you want to scrape.
global_dynamicUrl = "https://senior-secondary.scsa.wa.edu.au/certification/student-achievement-data-by-school"
driver.get(global_dynamicUrl)

#************* FUNCTION - Capture drop-down options **************
def capture_dropdwns(selection_id):
    # Use the ID of the Select tag  for the drop-down.
    element = driver.find_element(By.ID, selection_id)
    # find the element tag for individual name options.
    # all_options = element.find_elements(by=By.TAG_NAME, 'option')
    all_options = element.find_elements_by_tag_name("option")
    # Declare a list to store the school names that are found.
    list_of_options = []
    # Loop through all the school names and save them into the list.
    for option in all_options:
        list_of_options.append(option.get_attribute("value"))
        option.click()
    # return the list of drop-down options
    return list_of_options
#******************************************************************

school_names = capture_dropdwns("firstSchool")
time.sleep(2)

list_w_values = []
finished_text = open('finished_text.txt', 'w')

for schools in school_names:
    select_schoolName = Select(driver.find_element(By.ID, 'firstSchool'))
    select_schoolName.select_by_visible_text(schools)

    # Fill in the First Year drop-down
    select_firstYear = Select(driver.find_element(By.ID, 'firstYear'))
    selectLen = len(select_firstYear.options)
    select_firstYear.select_by_index(selectLen-1)

    # Fill in the Second Year drop-down
    select_secondYear = Select(driver.find_element(By.ID, 'secondYear'))
    selectLen = len(select_secondYear.options)
    select_secondYear.select_by_index(selectLen-1)

    # Click on the submit button
    submit_button = driver.find_element(By.ID, 'getResults')
    submit_button.click()

    # table - Number of eligible year 12 students
    # form - Full-time WACE-eligible Year 12 students
    eligible_Students_No = driver.find_element(By.ID, 'e-w-num1').text
    # table - % students who achieved the WACE
    # form - Full-time WACE-eligible Year 12 students who achieved the WACE
    students_Achieve_Per = driver.find_element(By.ID, 'achieved-w-per1').text
    # table - Number of students with an ATAR
    # form - Full-time WACE-eligible Year 12 students who completed four or more year 12 ATAR courses
    students_W_ATAR_No = driver.find_element(By.ID, 'four-atar-num1').text
    # table - Number completed Cert II or higher but less than four ATAR courses
    # form - Full-time WACE-eligible Year 12 students who completed a Certificate II or higher but less than four or more Year 12 ATAR courses
    complete_cert_2_No = driver.find_element(By.ID, 'cert2-num1').text

    finished_text.write(f'{schools}\t{eligible_Students_No}\t{students_Achieve_Per}\t{students_W_ATAR_No}\t{complete_cert_2_No}\n')
    #formatted = f'{schools} {eligible_Students_No}\t{students_Achieve_Per}\t{students_W_ATAR_No}\t{complete_cert_2_No}\n'
    # list_w_values.append(finished_text)

    # print(f'{schools}\t{eligible_Students_No}\t{students_Achieve_Per}\t{students_W_ATAR_No}\t{complete_cert_2_No}\n')
    time.sleep(0.5)
