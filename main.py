import re
import requests
from bs4 import BeautifulSoup


query = "contact lenses"
query = query.replace(' ', '+')
URL = f"http://google.com/search?gl=us&hl=en&q={query}"


# desktop user-agent
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:65.0) Gecko/20100101 Firefox/65.0"

headers = {"user-agent" : USER_AGENT}
resp = requests.get(URL, headers=headers)

if resp.status_code == 200:
     soup = BeautifulSoup(resp.content, "html.parser")
else:
    print("Failed to fetch page.")
    exit(1)

# with open('test.htm', 'r') as myfile:
#   data = myfile.read()
#
# soup = BeautifulSoup(data, "html.parser")


results = []
for product_element in soup.find_all(attrs={'class': re.compile(r"pla-unit-container")}):
    link_elements = product_element.find_all('a')
    if link_elements:
        # Get the link.
        link = link_elements[1]['href']

        # Get the title and link title.
        titles = []
        spans = product_element.find_all('span')
        for s in spans:
            if s.text != '' and '<span' not in s and '</span>' not in s:
                titles.append(s.text)

        # Get the price.
        price = ''
        divs = product_element.find_all('div')
        for d in divs:
            if d.text != '':
                match_price = re.match(r'^.\d+\.\d+$', d.text)
                if match_price:
                    price = match_price.group()

        item = {
            "title": titles[0],
            "link_title": titles[-1],
            "link": link,
            "price": price
        }
        results.append(item)




print(results)
print(len(results))