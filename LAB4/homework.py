from bs4 import BeautifulSoup as bs
import socket
import json

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 65432  # The port used by the server

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

def send_req(path: str):
    msg = bytes(f'GET {path}', 'utf-8')
    client.send(msg)

    return str(client.recv(4096))


def parse_page(path: str):
    res = send_req(path)
    html = bs(str(res), 'html.parser')

    return html.select('h1')[0].text.strip()

def scrape(path: str, save_as_json=False):
    res = send_req(path)
    html = bs(str(res), 'html.parser')

    data = {
        'name': html.select('#name')[0].text.replace('name:', '').strip(),
        'author': html.select('#author')[0].text.replace('author:', '').strip(),
        'price': html.select('#price')[0].text.replace('price:', '').strip(),
        'description': html.select('#desc')[0].text,
    }

    if save_as_json:
        with open('scraped_data.json', 'w') as f:
            json.dump(data, f)

    return data


print(scrape('/products/1', save_as_json=True))
# print(parse_page('/'))
# print(parse_page('/about'))
# print(parse_page('/contacts'))