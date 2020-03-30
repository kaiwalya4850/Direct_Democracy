from selenium import webdriver
import time 
import pandas as pd
from bs4 import BeautifulSoup

def tablemaker(soup,bill_type):
	column_names = ["BILL_Name", "BIll_link","Bill_type"]
	df = pd.DataFrame(columns = column_names)
	divs = soup.find_all('div',  class_="view-content")
	for div in divs:

		# print(div.prettify())
		subdivs=div.find_all('div',  class_="views-field views-field-title-field")
		for sd in subdivs:
			# print(sd.prettify())
			ancors=sd.find_all('a')
			for ancor in ancors :
				BIll_name=ancor.getText()
				# print(BIll_name)
				link= "https://www.prsindia.org"+ancor['href']
				# print(link)
				df=df.append(pd.Series([BIll_name,link,bill_type], index=df.columns ), ignore_index=True)
	return df
driver = webdriver.Chrome(executable_path='./chromedriver.exe')
driver.maximize_window()
url ='https://www.prsindia.org/billtrack/field_bill_category/all'
driver.get(url)
time.sleep(1.5) 
driver.find_element_by_xpath("//select[@id='edit-field-bill-status']/option[text()='Draft']").click() 
buttons= driver.find_element_by_xpath(("//button[@id='edit-submit-billtrack']"))
time.sleep(1.5) 
buttons.click()
time.sleep(1.5) 
html_source = driver.page_source
soup = BeautifulSoup(html_source, 'html.parser')

DRaft_df=tablemaker(soup,'Draft')
print(DRaft_df)


url ='https://www.prsindia.org/billtrack/field_bill_category/all'
driver.get(url)
time.sleep(1.5) 
driver.find_element_by_xpath("//select[@id='edit-field-bill-status']/option[text()='Pending']").click() 
buttons= driver.find_element_by_xpath(("//button[@id='edit-submit-billtrack']"))
time.sleep(1.5) 
buttons.click()
time.sleep(1.5) 
html_source = driver.page_source
soup = BeautifulSoup(html_source, 'html.parser')
pending_df=tablemaker(soup,'Pending')
print(pending_df)
# print(soup)



final_df= DRaft_df.append(pending_df)
final_df=final_df.reset_index()
final_df=final_df.drop(columns=['index'])
final_df.to_csv("res.csv")

print(final_df)
driver.close()