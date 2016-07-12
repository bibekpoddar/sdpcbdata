# Author : ace139
# Author Email : soumyodey@live.com
# This script is for educational purpose only, Author is NOT LIABLE for any misuse

import urllib.request
from bs4 import BeautifulSoup

url = ['http://www.dpccairdata.com/dpccairdata/display/avView15MinData.php',
     'http://www.dpccairdata.com/dpccairdata/display/mmView15MinData.php',
     'http://www.dpccairdata.com/dpccairdata/display/pbView15MinData.php',
     'http://www.dpccairdata.com/dpccairdata/display/rkPuramView15MinData.php',
     'http://www.dpccairdata.com/dpccairdata/display/airpoView15MinData.php',
     'http://www.dpccairdata.com/dpccairdata/display/civilLinesView15MinData.php',]

av, mm, pb, rk, igi, cl = ([] for i in range(6))
pool = [av, mm, pb, rk, igi, cl]
op = ['av.csv', 'mm.csv', 'pb.csv', 'rk.csv', 'igi.csv', 'cl.csv']

headers = {}
headers['User-Agent'] = "Mozilla/5.0 (X11; Linux x86_64; rv:47.0) Gecko/20100101 Firefox/47.0"

for i in range(6):
	data = urllib.request.urlopen(urllib.request.Request(url[i], headers = headers)).read()
	soup = BeautifulSoup(data, 'html5lib')
	tbody = soup.find_all('tbody')
	# pass_gas : table for Gas Concentration
	pass_gas = tbody[4]
	tr = pass_gas.find_all('tr')
	pass_gasA = (tr[2].find_all('td'))
	date = pass_gasA[1].text#.replace(", ", "','").replace(" ", "','")
	date = date.split(',')
	date_num = date[1][-2:]
	date_month = date[1].rstrip(date_num)
	time = pass_gasA[2].text
	pool[i].append(date[0])
	pool[i].append(date_month)
	pool[i].append(date_num)
	pool[i].append(date[2])
	pool[i].append(time)
	for j in tr[2:]:
		val = (j.find_all('td')[3].text).split(' ')[0].split('µg/m')[0]
		if len(val) < 1 or val == '-':
			pool[i].append('NA')
		else:
			pool[i].append(val)
	# pass_pm : table for Particulate Matter and Meteorological Concentration
	# try catch : no data avaibale for Civil Lines
	try:
		pass_pm = tbody[8]
		tr = pass_pm.find_all('tr')
		for l in tr[1:]:
			val = (l.find_all('td')[3].text).split(' ')[0].strip('Data').split('µg/m')[0]
			if len(val) < 1 or val == '-':
				pool[i].append('NA')
			else:
				pool[i].append(val)	
	except IndexError:
		pass

	with open(op[i], 'a') as f:
		f.write(str(pool[i]).strip('[]').replace(' ','') + '\n')