import requests
from bs4 import BeautifulSoup

urls=['https://www.hamrodoctor.com/search/hospital?hospital_type=0&title=%20Top%20hospitals%20in%20Nepal']

with open('hrefs.txt', 'w') as file:
    for url in urls:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        parent_links = soup.find_all('div', class_="item")
        if parent_links:
            for link in parent_links:
                href_value = link.find('a').get('href')
                print(href_value)
                file.write("https://hamrodoctor.com/"+href_value + '\n')
        else:
            print("None")