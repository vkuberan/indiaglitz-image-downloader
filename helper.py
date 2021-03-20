import os
import platform
import subprocess
import requests
import time
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from bs4 import BeautifulSoup
import shutil

# seconds
DEFAULT_TIMEOUT = 5
retry_strategy = Retry(
    total=5,
    backoff_factor=1,
    status_forcelist=[429, 500, 502, 503, 504],  # http://httpstat.us/
    method_whitelist=["HEAD", "GET", "OPTIONS"]
)


# To set default timeout parameter for our scrapper
# Refer: https://findwork.dev/blog/advanced-usage-python-requests-timeouts-retries-hooks/#request-hooks
class IndiaGlitzTimeOutHTTPAdapter(HTTPAdapter):
    def __init__(self, *args, **kwargs):
        self.timeout = DEFAULT_TIMEOUT
        if "timeout" in kwargs:
            self.timeout = kwargs["timeout"]
            del kwargs["timeout"]

        super().__init__(*args, **kwargs)

    def send(self, request, **kwargs):
        timeout = kwargs.get("timeout")
        if timeout is None:
            kwargs["timeout"] = self.timeout

        return super().send(request, **kwargs)


def clear_screen():
    command = "cls" if platform.system().lower() == "windows" else "clear"
    return subprocess.call(command, shell=True)


def print_char_under_string(msg, char='', newline='\n\n'):
    if char != '':
        msg += "\n" + (char * len(msg))
    print(msg, end=newline)


def create_related_dirs(project_dirs):
    # create 2 separate directories to save html and the scraped data
    for dirname, dirpath in project_dirs.items():
        # check weather the dir exists, if not create new one
        if not os.path.exists(dirpath):
            os.makedirs(dirpath)
            print("{}: '{}' directory is created.".format(dirname, dirpath))


def fetch_data_from_url(link_source, html_file_to_save):

    html_source = ''
    try:
        with open(html_file_to_save, 'rb') as hs:
            html_source = hs.read().decode("UTF-16")
            print_char_under_string(
                "Fetching info from the crawled file.", '-', '\n')
    except Exception as e:
        errno, errmsg = e.args
        errmsg = "Error({}): {}, Creating new file {}.".format(
            errno, errmsg, html_file_to_save)
        print_char_under_string(errmsg, '*', '\n\n')
        print_char_under_string(
            "Fetching data from the server using request.", '-', '\n')

        try:
            adapter = IndiaGlitzTimeOutHTTPAdapter(
                max_retries=retry_strategy, timeout=5)
            http = requests.Session()
            http.mount("https://", adapter)
            http.mount("http://", adapter)

            response = http.get(link_source)
            # print(response.headers)

            html_source = response.text
            with open(html_file_to_save, mode='w', encoding='UTF-16') as f:
                f.write(response.text)

        except Exception as e:
            print(e)

    return html_source


def get_list_of_url_links(data):
    soup = BeautifulSoup(data, "lxml")
    list_of_urls = {}
    actors_actresses = soup.find('div', class_='movie_gallery_index').find(
        "ul").find_all('a')

    for actor_actress in actors_actresses:
        if actor_actress.text:
            text_to_key = actor_actress.text.lower().replace(' ', '-')
            list_of_urls[text_to_key] = actor_actress['href']

    return list_of_urls


def save_image_to_disk(link_source, img_file_name):

    if not os.path.isfile(img_file_name):
        print("{:>4s} File does not exists. Creating new one at '{}'\n\n".
              format('', img_file_name))
        try:
            adapter = IndiaGlitzTimeOutHTTPAdapter(
                max_retries=retry_strategy, timeout=5)
            http = requests.Session()
            http.mount("https://", adapter)
            http.mount("http://", adapter)

            response = http.get(link_source, stream=True)
            with open(img_file_name, 'wb') as out_file:
                shutil.copyfileobj(response.raw, out_file)
            del response
            time.sleep(1)

        except Exception as e:
            print("{:>4s} {}".format('', e))
    else:
        print("{:>4s} File already exists at '{}'\n\n".format(
            '', img_file_name))
