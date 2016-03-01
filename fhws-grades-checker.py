from selenium import webdriver
from winsound import Beep
import sys
import time
from datetime import datetime
from random import randint

"""
This script checks periodically if the new grades are online within the FHWS-Studentenportal. If three login attempts in a row failed the script exits.
It depends on selenium with phantomjs-webdriver. To use this script both must be installed!
Tested with python 2.7 and windows - if you want to use in on linux you have to remove winsound.
"""

current_semester = '2015 Winter'  # put your current semester in here!
k_number = 'your k-number here'
password = 'your password here'
waiting_time_between_checks = 60 * randint(15,30)  # between 15 and 30 minutes

def log(msg):
	print("{}: {}".format(datetime.today().time(), msg))
	

def login(driver):
	counter = 0
	while not driver.current_url == 'https://studentenportal.fhws.de/home' and counter < 3:
		time.sleep(25)
		driver.get("https://studentenportal.fhws.de/login")
		driver.find_element_by_name('username').send_keys(k_number)
		driver.find_element_by_name('password').send_keys(password)
		driver.find_element_by_xpath('/html/body/div[1]/div/div/div/div/form/input').click()
		counter += 1
	
	if counter == 3:
		log("Could not login :/")
		return False
	else:
		log("Successful logged in!")
		return True


def check_for_grades(driver):
	driver.get('https://studentenportal.fhws.de/grades')
	if driver.current_url == 'https://studentenportal.fhws.de/login':
		log("Not logged in anymore :/")
		return -1
	src = driver.page_source  
	if not current_semester in src:
		log("Not online atm :/ ")
		return 0
	else:
		log("YES! Online!!!")  # message if the grades are online
		return 1
	

if __name__ == '__main__':
	driver = webdriver.PhantomJS()
	driver.set_window_size(1120, 550)
	
	while True:
		r = check_for_grades(driver)
		if r == -1:
			s = login(driver)
			if not s:
				Beep(500, 1500)
				sys.exit(-1)
		elif r == 0:
			time.sleep(waiting_time_between_checks)  
		elif r == 1:
			Beep(1000, 1500)
			sys.exit(0)
		
	
	
	print driver.current_url
	driver.quit()
