import requests
from concurrent.futures import ThreadPoolExecutor
import colorama
from colorama import Fore
import os
import re
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from filelock import FileLock
colorama.init(autoreset=True)
import argparse

folder = os.path.dirname(__file__)
visited_pages = []

lock1 = FileLock("thread_1.lock", timeout=1)
lock2 = FileLock("thread_2.lock", timeout=1)

ports = [
  "80",
  "8080",
  "8081",
  "443",
  "4434",
  "8443",
  "4434"
]

def main():
  with open(input_file, "r") as myfile:
    content = myfile.readlines()

    with ThreadPoolExecutor(max_workers = 5) as executor:
      for line in content:
        for port in ports:
          http = "https://"
          if "80" in port:
            http = "http://"
          executor.submit(start_crawler, http + line.strip() +":" + port)

def start_crawler(url):
  try:
    site_result = request_url(url)
    if site_result is not False:
      get_banner(site_result[0], site_result[1])
  except Exception as e:
    print(e)

def request_url(url):
  try:
    session = requests.session()
    session.headers['User-Agent'] = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.152 Safari/537.36"
    response = session.get(url=url, timeout=10)
    session.close()

    if response.status_code >= 400:
      return False

    soup = BeautifulSoup(response.text, 'html.parser')
    visited_pages.append(url)
  except Exception as e:
    return False
  return (response, soup)

def get_banner(request, soup):
    banner_array = []
    banner_array.append(request.url)
    banner_array.append(request.headers.get("Server"))
    try:
      title = soup.find("title").get_text().strip().replace("\n", "")
      banner_array.append(title)
      meta_tags = soup.find_all("meta", attrs={"name": "generator"})
      if len(meta_tags) > 0:
        for meta_tag in meta_tags:
          banner_array.append(meta_tag.attrs.get("content"))
    except Exception as e:
      print(e)

    fullstring = ', '.join(str(item) for item in banner_array)
    print(Fore.GREEN + fullstring)

    with lock1:
      open(output_file + '_banner.txt', "a").write(fullstring +'\n')
    with lock2:
      open(output_file, "a").write(request.url +'\n')

if __name__ == "__main__":
  parser = argparse.ArgumentParser(description='Crawl websites from subdomain/domain list')
  parser.add_argument('-i', type=str, default="./input.txt", help='Path to input file')
  parser.add_argument('-o', type=str, default="./output.txt", help='Path to output file')
  args = parser.parse_args()
  input_file = args.i
  output_file = args.o
  main()