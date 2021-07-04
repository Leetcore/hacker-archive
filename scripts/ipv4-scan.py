# simple webserver scanner for IPv4
from datetime import date
import requests
from concurrent.futures import ThreadPoolExecutor
import colorama
colorama.init(autoreset=True)
import os
import time
from bs4 import BeautifulSoup

folder = os.path.dirname(__file__)
ports = [
  "80",
  "8080",
  "8081",
  "443",
  "4434",
  "8443",
  "4434"
]
path = ""

def get_banner(response, soup):
	banner_array = []
	banner_array.append(response.url)
	banner_array.append(response.headers.get("Server"))
	try:
		title = soup.find("title").get_text().strip()
		banner_array.append(title.replace("\n", ""))
		meta_tags = soup.find_all("meta", attrs={"name": "generator"})
		if len(meta_tags) > 0:
			for meta_tag in meta_tags:
				banner_array.append(meta_tag.attrs.get("content"))
		banner_array.append("password: " + str(len(soup.find_all("input", attrs={"type": "password"}))))
	except Exception as e:
		print(e)

	fullstring = ', '.join(str(item) for item in banner_array)
	print(colorama.Fore.GREEN + fullstring)
	return fullstring

def scan(oct1, oct2, oct3, oct4, port, path):
	# build full url with port
	ip = returnIP(oct1, oct2, oct3, oct4)
	proto = "https://"
	if "80" in port:
		proto = "http://"
	url = proto + ip +':'+ port + '/'+ path

	try:
		# try the request with timeout
		session = requests.session()
		session.headers['User-Agent'] = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.152 Safari/537.36"
		response = session.get(url=url, timeout=10, verify=False)
		session.close()
		if response.status_code >= 400:
			return

		soup = BeautifulSoup(response.text, 'html.parser')
		response.close()

		resultstring = get_banner(response, soup)

		with open(folder + "/results/ipv4/results_" + date.today() +".csv", "a") as myfile:
			myfile.write(resultstring +'\n')

	except (TimeoutError, requests.exceptions.ConnectTimeout, requests.exceptions.SSLError):
		return
	
	except Exception as e:
		print(e)
		time.sleep(1)

def returnIP(oct1, oct2, oct3, oct4):
	return str(oct1) + '.' + str(oct2) + '.' + str(oct3) + '.' + str(oct4)

# try all ipv4 ips
with ThreadPoolExecutor(max_workers = 5) as executor:
	for oct1 in [2, 3, 5, 18, 45, 46, 77, 78, 80, 84, 86, 87, 91, 93, 95, 109, 132, 134, 141, 144, 149, 157, 161, 176, 185, 188, 196, 217]:
		for oct2 in range(1, 254):
			print('Progress: ' + returnIP(oct1, oct2, 0, 0))
			for oct3 in range(1, 254):
				for oct4 in range(1, 254):
					# start scanning
					for port in ports:
						executor.submit(scan, oct1, oct2, oct3, oct4, port, path)
