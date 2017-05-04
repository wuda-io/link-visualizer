import requests
from bs4 import BeautifulSoup
from collections import Counter, OrderedDict
from urllib.parse import urlparse

def crawl_links(url, only_ext=True):
    links = []
    this_url = urlparse(url).netloc
    if this_url.find(".") < 0:
        return {}

    # Parse
    links_total = []
    try:
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')
        links_total = soup.find_all('a')
    except:
        print("Error while loading or parsing")

    links = []
    for link in links_total:
        try:
            l = link["href"]
            # parse only domain
            o = urlparse(l)
            base_url = o.netloc
            base_url = base_url.replace("www.", "") #replace www
            links.append(base_url)
        except:
            continue

    #reformat,count
    cnt = Counter()
    for x in links:
        # only add not empty links
        if len(x) > 0:
            # only external links
            if x != this_url:
                cnt[x] += 1
    #sort
    return OrderedDict(sorted(cnt.items(), key=lambda x: x[1], reverse=True))

def save(inputData, url, append="a"):    
    if append != "a":
        txt = 'source,target,weight\n'
    else:
        txt = ''
    if inputData is not None:
        for link in inputData:
            txt += '"'+url+'","'+link+'",'+str(inputData[link])+'\n'
        f = open("firm.csv", append)
        f.write(txt)
        f.close()

def goCrawl(url, layers=1):
    # exit
    if layers == 0:
        return
    #start
    url = url.replace("www.", "") #replace www
    this_url = urlparse(url).netloc
    a = crawl_links(url)
    save(a, this_url)
    layers -= 1  
    for i in a:
        tabs = '\t'*layers
        print(tabs+str(a[i]), i)
        goCrawl("http://"+i, layers)
    

# MAIN
save({}, "", "w")
goCrawl("http://www.wuda.at", 3)


