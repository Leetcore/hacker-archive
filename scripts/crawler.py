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
output_strings = []
max_crawl_depth = 2

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

    with ThreadPoolExecutor(max_workers = 50) as executor:
      for line in content:
        for port in ports:
          http = "https://"
          if "80" in port:
            http = "http://"
          executor.submit(start_crawler, http + line.strip() +":" + port, 0)

def start_crawler(url, limit):
  limit = limit + 1
  if limit > max_crawl_depth:
    return

  # filter filename urls
  match = re.search("\.\w+$", url) 
  if match:
    return

  try:
    site_result = request_url(url)
    if site_result is not False:
      # find links and start crawling!
      response = site_result[0]
      soup = site_result[1]
      parsed_url = urlparse(response.url)
      base_tag = soup.find("base")
      link_array = re.findall(r'(http|ftp|https):\/\/([\w\-_]+(?:(?:\.[\w\-_]+)+))([\w\-\.,@?^=%&:/~\+#]*[\w\-\@?^=%&/~\+#])?', response.text)
      get_banner(response, soup)

      # get html links
      a_tags = soup.find_all("a")
      for a_tag in a_tags:
        link = a_tag.attrs.get("href")
        
        if link and link.startswith("/"):
          port = ""
          if parsed_url.port:
            port = ":" + str(parsed_url.port)
          full_link = parsed_url.scheme + "://" + parsed_url.hostname + port + link
          start_crawler(full_link, limit)

        # check base tag urls
        if base_tag:
          base = base_tag.attrs.get("href")
          port = ""
          if parsed_url.port:
            port = ":" + str(parsed_url.port)
          full_link = parsed_url.scheme + "://" + base + port + link
          start_crawler(full_link, limit)

        # absolut urls to same domain
        if link and link.startswith("http:"):
          if parsed_url.hostname in link:
            start_crawler(link, limit)

      # get http links
      for link_parts in link_array:
        full_url = link_parts[0] + "://" + link_parts[1] + "/" + link_parts[2]
        if parsed_url.hostname in full_url:
          start_crawler(full_url, limit)
  except Exception as e:
    print(e)

def request_url(url):
  try:
    if url not in visited_pages:
      session = requests.session()
      session.headers['User-Agent'] = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.152 Safari/537.36"
      response = session.get(url=url, timeout=3)
      session.close()

      visited_pages.append(url)
      if response.status_code >= 400:
        return False

      soup = BeautifulSoup(response.text, 'html.parser')
      
    else:
      return False
  except Exception as e:
    return False
  return (response, soup)

def get_banner(response, soup):
    banner_array = []
    banner_array.append(response.url)
    banner_array.append(response.headers.get("Server"))
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
    if fullstring not in output_strings:
      output_strings.append(fullstring)
      print(Fore.GREEN + fullstring)
      with lock1:
        open(output_file + '_banner.txt', "a").write(fullstring +'\n')
      with lock2:
        open(output_file, "a").write(response.url +'\n')

if __name__ == "__main__":
  parser = argparse.ArgumentParser(description='Crawl websites from subdomain/domain list')
  parser.add_argument('-i', type=str, default="./input.txt", help='Path to input file')
  parser.add_argument('-o', type=str, default="./output.txt", help='Path to output file')
  args = parser.parse_args()
  input_file = args.i
  output_file = args.o
  main()