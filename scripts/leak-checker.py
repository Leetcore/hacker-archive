import requests
from concurrent.futures import ThreadPoolExecutor
import colorama
colorama.init(autoreset=True)
import os
from filelock import FileLock
import argparse

folder = os.path.dirname(__file__)
visited_pages = []

lock = FileLock("main_thread.lock", timeout=1)
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
  global leaky_filenames, exts

  with open(input_file, "r") as myfile:
    content = myfile.readlines()

  with open(ext_file_path, "r") as myfile:
    exts = myfile.readlines()

  with open(leak_file_path, "r") as myfile:
    leaky_filenames = myfile.readlines()

  with ThreadPoolExecutor(max_workers = 50) as executor:
    for line in content:
      if line.startswith("http"):
        executor.submit(start_crawler, line.strip())
      else:
        for port in ports:
          http = "https://"
          if "80" in port:
            http = "http://"
        executor.submit(start_crawler, http + line.strip() +":"+ port)

def start_crawler(url):
  try:
    site_result = request_url(url)
    if not type(site_result) == bool:
      url_comps = site_result.url.split("/")
      for folder_index in range(3, len(url_comps)):
        for leaky_filename in leaky_filenames:
          for ext in exts:
            new_url = []
            filename = leaky_filename.strip() + "." + ext.strip()
            for index, comp in enumerate(url_comps):
              if len(url_comps) <= 3 or index < len(url_comps) - (len(url_comps) - folder_index):
                new_url.append(comp)
            new_url.append(filename)
            new_site_response = request_url("/".join(new_url))
            if not type(new_site_response) == bool:
              if len(new_site_response.history) > 0:
                print("Redirect: \t" + "/".join(new_url))
              if "<html" in new_site_response.text.lower():
                print("HTML: \t\t" + "/".join(new_url))
              if "<html" not in new_site_response.text.lower():
                get_banner(new_site_response)

  except Exception as e:
    print(e)

def get_banner(request):
    url = request.url
    print(colorama.Fore.GREEN + url)

    with lock:
      open(output_file, "a").write(url +'\n')

def request_url(url):
  try:
    if url not in visited_pages:
      session = requests.session()
      session.headers['User-Agent'] = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.152 Safari/537.36"
      response = session.get(url=url, timeout=3)
      session.close()

      if response.status_code >= 400:
        return False

      visited_pages.append(url)
    else:
      return False
  except Exception as e:
    return False
  return response

if __name__ == "__main__":
  parser = argparse.ArgumentParser(description='Check leaky urls from subdomain/domain list.')
  parser.add_argument('-i', type=str, default="./input.txt", help='Path to input file')
  parser.add_argument('-o', type=str, default="./output.txt", help='Path to output file')
  parser.add_argument('-ext', type=str, default="./ext.txt", help='Path to extension file')
  parser.add_argument('-leaky', type=str, default="./leaky.txt", help='Path to leaky names')
  args = parser.parse_args()
  input_file = args.i
  output_file = args.o
  ext_file_path = args.ext
  leak_file_path = args.leaky
  main()