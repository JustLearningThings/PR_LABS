from bs4 import BeautifulSoup as bs
import requests

class Scraper:
    def __init__(self) -> None:
        self.DOMAIN = '999.md'

    
    def parse_from(self,
        url: str,
        num_pages_to_scrape: int,
        url_list: list[str] = [],
        num_page: int = 0,):
        # recursion edge case
        if num_page == num_pages_to_scrape:
            return url_list
        
        # make a request
        req = requests.get(url=url + '?page=' + str(num_page))
        html = req.text
        soup = bs(html, 'html.parser')
        
        # check if has more pages
        li = soup.select('.paginator li')[-1]

        # scrape
        links = soup.find_all('a', {'class': 'js-item-ad'})
        filtered_links = ['https://' + self.DOMAIN + link['href'] for link in links if 'booster' not in link['href']]
        filtered_links = list(set(filtered_links))

        url_list.extend(filtered_links)
        num_page += 1

        return self.parse_from(url, num_pages_to_scrape, url_list, num_page)
        

    def parse_page(self,
            url: str,
    ):
        # setup
        req = requests.get(url)
        html = req.text
        soup = bs(html, 'html.parser')

        data = {
            'prices': [],
            'author': {},
            'characteristics': {},
            'type': None,
            'last_changed': None,
            'views': None,
            'region': None,
            'phone': None
        }

        # extract price

        prices = soup.find_all('span', {'itemprop': 'price'})
        currencies = soup.find_all('span', {'itemprop': 'priceCurrency'})

        data_prices = []
        for i in range(len(prices)):
            data_prices.append({
                'value': str(prices[i].text).strip(),
                'currency': str(currencies[i].text).strip()
                })
        
        data['prices'] = data_prices

        # extract characteristics

        prop_names = [str(p.text).strip()
                    for p in soup.select('div.adPage__content__features > div > ul > li > span.adPage__content__features__key')]
        prop_values = [str(p.text).strip()
                    for p in soup.select('div.adPage__content__features > div > ul > li > span.adPage__content__features__value')]
        
        i, characteristics = 0, {}
        while i < len(prop_values):
            characteristics[prop_names[i]] = prop_values[i]

            i += 1

        while i < len(prop_names):
            characteristics[prop_names[i]] = True

            i += 1
        
        data['characteristics'] = characteristics

        # extract author

        owner = soup.find('a', {'class': 'adPage__aside__stats__owner__login'})
        data['author'] = str(owner.text).strip()

        # extract date
        lc = soup.find('div', {'class': 'adPage__aside__stats__date'})
        data['last_changed'] = str(lc.text).replace('Data actualizării:', '').strip()

        # extract type

        type = soup.find('div', {'class': 'adPage__aside__stats__type'})
        data['type'] = str(type.text).replace('Tipul:', '').strip()

        # extract views

        views = soup.find('div', {'class': 'adPage__aside__stats__views'})
        views = str(views.text)
        views = views[:views.index('(')]
        views = views.replace('Vizualizări:', '').strip()
        data['views'] = views

        # extract region

        region_data = soup.select('dl.adPage__content__region > dd')
        region = ''.join(dd.text for dd in region_data).replace('  ', '').replace(',', ', ').replace(' ,', ',').strip()
        data['region'] = region

        # extract contacts

        tel = soup.select('dl.js-phone-number > dd > ul > li > a')[0]['href']
        tel = str(tel).replace('tel:', '')
        data['phone'] = tel

        return data

# s = Scraper()
# print(s.parse_page('https://999.md/ro/76773625'))
# print(s.parse_from(
#     url='https://999.md/ro/list/real-estate/apartments-and-rooms?o_30_241=893&applied=1&eo=12900&eo=12912&eo=12885&eo=13859&ef=32&ef=33&o_33_1=776',
#     num_pages_to_scrape=2,
# ))