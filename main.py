import json
from urllib.request import Request, urlopen

from bs4 import BeautifulSoup

def main():
    with open('controles.json') as file:
        data = json.load(file)
        precio_objetivo = 35000
        precio = ""

        for tienda in data['controles']:
            comercio = tienda['tienda']
            for control in tienda['items']:
                if comercio == 'paris':
                    precio = paris(control['link'])
                elif comercio == 'pcfactory':
                    precio = pcfactory(control['link'])
                elif comercio == 'microplay':
                    precio = microplay(control['link'])
                elif comercio == 'zmart':
                    precio = zmart(control['link'])
                elif comercio == 'ripley':
                    precio = ripley(control['link'])
                else:
                    continue

                # Para pruebas
                # if comercio == 'test':
                #     precio = ripley(control['link'])
                # else:
                #     continue
                
                if precio.isdigit():
                    if int(precio) <= precio_objetivo:
                        informacion = "{} tiene un control de {} al precio buscado (${}): {}"
                        print("|||||||||||||||||||||||||||||||||||||||")
                        print(informacion.format(comercio.capitalize(), control['consola'], precio, control['link']))
                        print("|||||||||||||||||||||||||||||||||||||||")
                else:
                    print("Error al obtener el precio")

def setupBS4(link):
    # print(link)
    req = Request(link, headers={'User-Agent': 'Mozilla/5.0'})
    with urlopen(req) as page:
        soup = BeautifulSoup(page, 'html.parser')
        return soup

def paris(link):
    soup = setupBS4(link)

    try:
        precio = soup.find('div', {'class': 'item-price offer-price price-tc default-price'}).text.strip()
    except Exception as e:
        precio = soup.find('div', {'class': 'item-price offer-price price-tc cencosud-price'}).text.strip()
        print(e)

    precio = precio.replace('$', '')
    precio = precio.replace('.', '')
    return precio

def pcfactory(link):
    soup = setupBS4(link)
    precio = soup.find('meta', {'itemprop': 'price'})['content'].strip()
    precio = precio.replace('.0000', '')
    return precio

def microplay(link):
    soup = setupBS4(link)
    precio = soup.find('div', {'class': 'precios'}).strong.text.strip()
    precio = precio.replace('$', '').replace('.', '')
    precio = precio[:6].strip()
    return precio

def zmart(link):
    soup = setupBS4(link)
    precio = soup.find('div', {'id': 'PriceProduct'}).text.strip()
    precio = precio.replace('$', '').replace('.', '')
    return precio

def ripley(link):
    soup = setupBS4(link)
    precio = soup.find_all('span', {'class': 'product-price'})
    precios = []
    for p in precio:
        p = p.text.strip()
        p = p.replace('$', '').replace('.', '')
        if p.find('RipleyPuntos') == -1:
            precios.append(p)
        else:
            continue
    precios = sorted(precios)
    precio = precios[0]
    return precio

def falabella():
    pass


if __name__ == '__main__':
    main()
    # input('Presiona Enter para cerrar')