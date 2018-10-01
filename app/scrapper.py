from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
import time
from app import dbw
from app.models import Mathematician

def simple_get(url):
    """
    Gets the html body of the url if the content type is HTML/XML
    :param url:
    :return:
    """
    try:
        with closing(get(url, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                return None
    except RequestException as e:
        log_error("Error during requests to {} : {}".format(url, str(e)))

def is_good_response(resp):
    """
    Return True if the response has HTML content
    :param url:
    :return:
    """
    content_type = resp.headers['Content-Type'].lower()
    #print resp.headers
    return (resp.status_code==200
            and content_type is not None
            and content_type.find('html') > -1)

def log_error(err):
    print err

def get_mathematicians(url):
    raw_html = simple_get(url)
    mathematicians = set()
    if raw_html is not None:
        html = BeautifulSoup(raw_html, 'html.parser',from_encoding="utf-8")
        for n, name in enumerate(html.select('ol')):
            for name1 in  name.select('a'):
                mathematicians.add(name1.text.strip())
        return mathematicians
            #for n1, name1 in enumerate(name.select('li')):
             #   print n1, name1.text

def get_score(name):
    base_url = 'https://xtools.wmflabs.org/articleinfo/en.wikipedia.org/{}'
    name1 = name
    name = name.encode('utf-8')
    t1 = time.time()

    html_body = simple_get(base_url.format(name))
    if html_body is not None:
        html = BeautifulSoup(html_body,'html.parser')
        t2 = time.time()

        hit = [ a for a in html.select('a')
                if a['href'].find('latest-60') > -1]
        if hit:
            print "Completed...{} - Output Generated - Took {} secs".format(name, t2-t1)
            return name,int(hit[0].text.replace(",",""))
        else:
            print "Completed...{} - No Output Generated - Took {} secs".format(name, t2-t1)
            return name,None

if __name__ == "__main__":
    mathematicians_list = get_mathematicians('http://www.fabpedigree.com/james/mathmen.htm')
    start_time = time.time()
    name_score = []
    for name in  mathematicians_list:

        detail = get_score(name)
        name_score.append(detail)
        M1 = Mathematician(name=name,hit=detail[1])
        dbw.session.add(M1)
        dbw.session.commit()

    print name_score
    end_time = time.time()

    print "Time taken to complete the task is {} seconds.  :  {} Records ".format(end_time-start_time, len(name_score))