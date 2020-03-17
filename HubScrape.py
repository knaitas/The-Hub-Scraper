import requests
from bs4 import BeautifulSoup

def get_last_page(source):
    soup = BeautifulSoup(source, 'lxml')
    next_pages = soup.find_all('li', {'role': 'presentation'})
    last_page = next_pages[-1].findChildren("a")[0]['href'].split('=')[-1]
    return int(last_page)

def get_all_urls():
    urls = []
    r = requests.get(PATH_URL)
    c = r.text
    last_page = get_last_page(c)
    for i in range(1, last_page + 1):
        r = requests.get(PATH_URL + "&page=" + str(i))
        c = r.text
        soup = BeautifulSoup(c, 'lxml')
        ahrefs = soup.find_all('a', {'class': 'card-job-find-list__link'})
        for a in ahrefs:
            urls.append(a["href"])
    return urls

BASE_URL = "https://thehub.io"
PATH_URL = "https://thehub.io/jobs?roles=backenddeveloper&roles=frontenddeveloper&roles=fullstackdeveloper&roles=androiddeveloper&roles=iosdeveloper&countryCode=DK"

print(get_all_urls())
#<li class="page-item" role="presentation"><a aria-label="Go to last page" class="page-link nuxt-link-active" href="/jobs?roles=backenddeveloper&amp;roles=frontenddeveloper&amp;roles=fullstackdeveloper&amp;roles=androiddeveloper&a