from flask import Flask, jsonify
from bs4 import BeautifulSoup
import csv
import requests

def scrape_jobs():
    # Send a GET request to the website
    given_url = "https://dailyremote.com"
    base_url = "https://dailyremote.com/?page="

    sp = soup(given_url)
    pagination_links = sp.find_all('a', class_='pagination-page')

    last_number = None

    for link in pagination_links:
        page_number = link.get_text()
        for page_num in page_number:
            if page_num.isdigit():
                last_number = int(page_number)

    # Define the CSV file name
    flag = False

    # for i in range(1, last_number + 1):
    for i in range(1,2):
        url = base_url + str(i)
        sp = soup(url)
        job_listings = sp.find_all("article")

        if flag == False:
            csv_file = 'job_data.csv'
            with open(csv_file, 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['Job Title', 'Location', 'Company', 'Company URL', 'Skills', 'Category'])
            flag = True

        with open(csv_file, 'a', newline='') as file:
            writer = csv.writer(file)
            # Extract data from each job listing
            for job in job_listings:
                job_title = title(job)
                job_location = location(job)
                company = company_name(job)
                website_url = company_url(job)
                skills = skill(job)
                categories = category(job)

                # Write the data to the CSV file
                writer.writerow([job_title, job_location, company, website_url, skills, categories])

    # Return a success message
    # return jsonify({"message": "Job data has been scraped and saved to job_data.csv"})

# Title
def title(x):
    try:
        title=x.find('a').text
        return title.replace('\n', '')
    except Exception as e:
        pass

#Company Name
def company_name(x):
    try:
        return x.find('span').text
    except Exception as e:
        pass

#location
def location(x):
    try:
        return x.find('span',attrs={'class':'meta-holder'}).text.strip()
    except Exception as e:
        pass

#Company_Url
def company_url(x):
    try:
        import requests
        given_url="https://dailyremote.com"
        HEADERS = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
 'Accept-Language': 'en-US,en;q=0.9'}
        end_point=x.find('a').get('href')
        link= given_url+end_point
        url_1 = requests.get(link,headers=HEADERS)
        soup2 = BeautifulSoup(url_1.content, "html.parser")
        company_link=soup2.find('a',attrs={'class':'primary-btn outline js-apply-button'})
        company_url=company_link.get('href')
        return given_url+company_url
    except Exception as e:
        pass

#category
def category(x):
    try:
        return x.find('span',attrs={'class':'job-category'}).text.strip()
    except Exception as e:
        pass

#Skills
def skill(x):
    try:
        string=x.find('div',attrs={'class':'tag-wrap display-flex items-center'}).text
        # Split the string into a list of words and remove empty strings
        words = [word.strip() for word in string.split('\n') if word.strip()]

        # Join the words with a comma
        result = ', '.join(words)
        return result
    except Exception as e:
        pass

def soup(url):
#    import requests
#    import pandas as pd
#    from bs4 import BeautifulSoup
   HEADERS = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
 'Accept-Language': 'en-US,en;q=0.9'}
   response = requests.get(url,headers=HEADERS)
    # Parse the HTML content using BeautifulSoup
   soup = BeautifulSoup(response.content, "html.parser")
   return soup
