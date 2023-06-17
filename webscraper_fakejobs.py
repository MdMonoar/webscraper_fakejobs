# ref link: https://realpython.com/beautiful-soup-web-scraper-python/

# importing necessary library
import requests
from bs4 import BeautifulSoup

# saving the url in url object
url = "https://pythonjobs.github.io/"

# storing the page data in an object
page = requests.get(url)

# creating a Beautiful Soup object
soup = BeautifulSoup(page.content, "html.parser")

# finding the target elements
results = soup.find("section", class_="job_list")
# job_elements = results.find_all("div", class_="job")

# finding the backend jobs using list comprehension
backend_jobs = results.find_all(
    'h1', string=lambda text: 'back' in text.lower()
)

backend_job_elements = [ h1_element.parent for h1_element in backend_jobs ]

# making a list object where scraped data will be stored
scraped_data = []

# function for retrieving data
for job_element in backend_job_elements:
    title_element = job_element.find("h1")
    company_element = job_element.find('i', class_='i-company').parent
    location_element = job_element.find('i', class_='i-globe').parent
    more_links = job_element.find_all('a')
    # the links used their relative path, not a full url,
    # found the structure and the full urls = main url + relative link
    more_url = url + more_links[1]['href']
    more_page = requests.get(more_url)
    more_soup = BeautifulSoup(more_page.content, "html.parser")
    more_links = more_soup.find('div', class_='contact')
    email_element = more_links.find(string=lambda text: 'email' in text.lower()).parent
    website_element = more_links.find(string=lambda text: 'website' in text.lower()).parent

    # email = email_element.findChild('a').text.strip()
    title = title_element.text.strip()
    company = company_element.text.strip()
    location = location_element.text.strip()
    email = email_element.find('a').text.strip()
    website = website_element.find('a')['href']

    # print(title, '\n', company, '\n', location, '\n', email, '\n', website, '\n')
    
    # saving the data into a list
    data_list = [title, company, location, email, website]

    # appending the scraped data list
    scraped_data.append(data_list)

# print(scraped_data)

# importing pandas and openpyxl for saving the data into excel file
import pandas as pd
import openpyxl

# saving the data into a dataFrame
data_columns = ['Title', 'Company', 'Location', 'Email', 'Website']
df = pd.DataFrame(scraped_data, columns= data_columns)

# print(df.head())

# saving the df into an excel file
df.to_excel('scrapedData.xlsx', index=False)

# reading the data from the excel file
excel_data = pd.read_excel('scrapedData.xlsx')
print(excel_data)

# checking & testing

# print(results.prettify())

# for job_element in job_elements:
#     print(job_element, end="\n"*2)

# for job_element in job_elements:
#     title_element = job_element.find("h1")
#     company_element = job_element.find('i', class_='i-company').parent
#     location_element = job_element.find('i', class_='i-globe').parent
    
#     title = title_element.text.strip()
#     company = company_element.text.strip()
#     location = location_element.text.strip()

#     print(title, '\n', company, '\n', location, '\n')



