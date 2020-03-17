import requests
from bs4 import BeautifulSoup
import threading
import queue

class GetJobAds(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.queue = queue
        
    def access_value(self, string, starting_point, ending_point):
        try:
            value = (string.split(starting_point)[1]).split(ending_point)[0]
        except Exception:
            value = None
        return value
    
    def get_last_page(self, source):
        soup = BeautifulSoup(source, 'lxml')
        next_pages = soup.find_all('li', {'role': 'presentation'})
        last_page = next_pages[-1].findChildren("a")[0]['href'].split('=')[-1]
        return int(last_page)
    
    def get_all_urls(self):
        PATH_URL = "https://thehub.io/jobs?roles=backenddeveloper&roles=frontenddeveloper&roles=fullstackdeveloper&roles=androiddeveloper&roles=iosdeveloper&countryCode="
        urls = []
        countries = ['DK'] #'SE', 'NO'
        for country in countries:
            r = requests.get(f"{PATH_URL}{country}")
            c = r.text
            last_page = self.get_last_page(c)
            for page in range(1, last_page + 1):
                r = requests.get(f"{PATH_URL}&page={page}")
                c = r.text
                soup = BeautifulSoup(c, 'lxml')
                ahrefs = soup.find_all('a', {'class': 'card-job-find-list__link'})
                for a in ahrefs:
                    urls.append(a["href"])
        return urls
    
    def get_data_from_url(self, url):
        job_ad_information = {}
        r = requests.get(f"https://thehub.io/{url}")
        c = r.text
        company_info = c.split('location:{country:')
        contacts = '{Country:'+company_info[1]
        job_ad_info = '{Country:'+company_info[2]
        country = self.access_value(contacts, '{Country:"', '"')
        salary = self.access_value(contacts, 'salary:"', '"')
        email = self.access_value(contacts, 'email:"', '"')
        phone = self.access_value(contacts, 'phone:"', '"')
        website = self.access_value(job_ad_info, 'website:"', '"')
        title = self.access_value(job_ad_info, 'title:"', '"')
        job_ad_created = self.access_value(job_ad_info, 'createdAt:"', '"')
        job_ad_expiring = self.access_value(job_ad_info, 'expirationDate:"', '"')
    
        job_ad_information.update(
            {
                "country": country,
                "title": title,
                "salary": salary,
                "website": website.replace("\\u002F", "/"),
                "email": email,
                "phone": phone,
                "Ad date": job_ad_created,
                "Ad expiration date": job_ad_expiring
    
            })
        return job_ad_information

j = GetJobAds()
job_ad = j.get_data_from_url('jobs/5e6fff49ab17a30da473e6ef')
print(job_ad)
