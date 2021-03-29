from requests_html import HTMLSession


class Item:
    def __init__(self, sku, product, atc_url, product_url):
        self.sku = sku
        self.product = product
        self.atc_url = atc_url
        self.product_url = product_url


# Wrapper for `fetchData`, automatically handles pages by stopping once a 404 response is encountered
def fetchDataMulti(url):
    index = 1
    result = []

    # Splits url at location expecting current page (cp) value
    t_url = url.split('.c?')
    res_url = ''

    # Big loop, ends when all pages have been scraped
    while True:
        try:
            if 'cp=' in url:
                res_url = t_url[0] + f'.c?cp={ index }&' + t_url[1][5:]
            else:
                res_url = t_url[0] + f'.c?cp={ index }&' + t_url[1]

            res = fetchData(url=res_url, index=index)
            if res:
                result += res
            index += 1
        except Exception as err:
            print("Done")
            print(err)
            break

    return result


def fetchData(url=None, index=1):
    print(f'-----Fetching-----')

    target = 'https://www.bestbuy.com/site/computer-cards-components/video-graphics-cards/abcat0507002.c?cp=3&id=abcat0507002&qp=gpusv_facet%3DGraphics%20Processing%20Unit%20(GPU)~NVIDIA%20GeForce%20RTX%203060%5Egpusv_facet%3DGraphics%20Processing%20Unit%20(GPU)~NVIDIA%20GeForce%20RTX%203060%20Ti%5Egpusv_facet%3DGraphics%20Processing%20Unit%20(GPU)~NVIDIA%20GeForce%20RTX%203070%5Egpusv_facet%3DGraphics%20Processing%20Unit%20(GPU)~NVIDIA%20GeForce%20RTX%203080%5Egpusv_facet%3DGraphics%20Processing%20Unit%20(GPU)~NVIDIA%20GeForce%20RTX%203090'

    if url:
        target = url

    session = HTMLSession()
    r = session.get(target)

    print(r.status_code)
    print(target)
    if r.status_code == 404:
        raise Exception('status code: 404, could not load page')

    # Grab all links from target page and filter them into product page links
    links = r.html.absolute_links

    filtd = filter(filt, links)

    items = []
    in_stock = []

    # Creates Item objects for each filtered URL
    for url in list(filtd):
        # Extract SKU from product page URLs
        sku = url.split('?skuId=')[1].split('#')[0]

        # Extracts name of products from product page URL
        name = prettifyName(
            url.split('https://www.bestbuy.com/site/')[1].split('.p?')[0])

        atc_url = generateATCUrl(sku)

        items.append(Item(sku, name, atc_url, url.split('#')[0]))

    # Filter all Item objects by sold out/coming soon & everything else
    #   This way if wording is weird or they change something up, alerts should still be sent
    for item in items:

        # Select the cart button for each product, 'stock' is the html element
        selector = f'button[data-sku-id="{sku}"], a[data-sku-id="{sku}"]'
        stock = r.html.find(selector, first=True)

        try:
            if (stock.text != 'Sold Out' and stock.text != 'Coming Soon'):
                data = {}
                data['sku'] = item.sku
                data['product'] = item.product
                data['atc_url'] = item.atc_url
                data['product_url'] = item.product_url

                in_stock.append(data)
        except:
            print(f'ERROR LOADING INFO SKU: {sku}')

    print("successfully fetched inventory data")
    return in_stock if in_stock != [] else None


# Makes names prettier, returns just the GPU name from link text
def prettifyName(name):
    compare = ['3060 Ti', '3060', '3070 Ti', '3070',
               '3080 Ti', '3080', '3090 Ti', '3090', 'i5-10600k']

    for i in compare:
        if i in name:
            return i

    return name


# Filter for all page links => product page links
def filt(url):
    brands = ['pny', 'asus', 'evga', 'nvidia',
              'msi', 'xfx', 'gigabyte', 'amd', 'intel']

    t_url = url.lower()
    if t_url[:29] == 'https://www.bestbuy.com/site/':
        t_url = t_url.split('https://www.bestbuy.com/site/')[1]
        t_url = t_url.split('-')[0]
        for brand in brands:
            if brand == t_url:
                return True
    return False


def generateATCUrl(sku):
    if sku:
        return f'https://api.bestbuy.com/click/-/{sku}/cart'
