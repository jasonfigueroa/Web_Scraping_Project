from bs4 import BeautifulSoup
import urllib
import re
import json

#put url in a string then pass as parameter to urlopen()
url_string = 'https://www.govdeals.com/index.cfm?fa=Main.AdvSearchResultsNew&searchPg=Classic&inv_num=&category=00&kWord=&kWordSelect=2&sortBy=ad&agency=2863&state=&country=&locID=&timing=bySimple&locationType=state&timeType=&timingWithin=1'

r = urllib.urlopen(url_string).read()

#results 1 - 10
#r = urllib.urlopen('https://www.govdeals.com/index.cfm?fa=Main.AdvSearchResultsNew&searchPg=Classic&inv_num=&category=00&kWord=&kWordSelect=2&sortBy=ad&agency=2863&state=&country=&locID=&timing=bySimple&locationType=state&timeType=&timingWithin=1').read()

#results 11 - 20
#r = urllib.urlopen('https://www.govdeals.com/index.cfm?fa=Main.AdvSearchResultsNew&searchPg=Classic&inv_num=&category=00&kWord=&kWordSelect=2&sortBy=ad&agency=2863&state=&country=&locID=&timing=bySimple&locationType=state&timeType=&timingWithin=1&rowCount=10&StartRow=11').read()

#results 21 - 30
#r = urllib.urlopen('https://www.govdeals.com/index.cfm?fa=Main.AdvSearchResultsNew&searchPg=Classic&inv_num=&category=00&kWord=&kWordSelect=2&sortBy=ad&agency=2863&state=&country=&locID=&timing=bySimple&locationType=state&timeType=&timingWithin=1&rowCount=10&StartRow=21').read()

#TODO figure out a way to dynamically build this url, maybe use the "Items 1 through n of n" found at the center of the page just above the table
#testing all results
#r = urllib.urlopen('https://www.govdeals.com/index.cfm?fa=Main.AdvSearchResultsNew&searchPg=Classic&inv_num=&category=00&kWord=&kWordSelect=2&sortBy=ad&agency=2863&state=&country=&locID=&timing=bySimple&locationType=state&timeType=&timingWithin=1&rowCount=49&StartRow=1').read()

soup = BeautifulSoup(r)

divs = soup.find_all('div')

print divs[11].text

total_items = re.search('of \d+', divs[11].text)

print total_items.group(0)

total_items = re.search('\d+', total_items.group(0))

print total_items.group(0)

url_string += '&rowCount=' + total_items.group(0) + '&StartRow=1'

r = urllib.urlopen(url_string).read()

soup = BeautifulSoup(r)

rows = soup.find_all('tr')

rows = rows[1:len(rows) - 2]

#following was for taking a look at the rows returned
#fl = open('test2.html', 'w+')

#following was for taking a look at the rows returned
#for row in rows:
#	print >> fl, row.prettify()

json_dict = {}

#loop rows and iterate tds	
for i in range(len(rows)):
	#print str(i)
	tds = rows[i].find_all('td')

	#value in bids for the following line can be accessed with bids.group(0)
	bids = re.search(' \d+', tds[7].text)
	
	if bids:
		bids = bids.group(0).strip()
	else:
		bids = '0'

	price = re.search('\d+.\d+', tds[7].text)

	price_dict = {'price': price.group(0), 'bids': bids}

	date = re.search('\d/\d/\d{4}', tds[6].text)

	time = re.search('\d{2}:\d{2} \w{2} \w{2}', tds[6].text)

	if time.group(0)[0] == '7':
		date_dict = {'end_date': date.group(0), 'end_time': time.group(0)[1:]}
		#print time.group(0)[1:]
	else:
		date_dict = {'end_date': date.group(0), 'end_time': time.group(0)}

	item_desc = tds[1].text.strip()[:tds[1].text.strip().index('\n')]

	#item_dict = {'item_desc': item_desc}

	#generalize the row number
	json_dict['row_' + str(i + 1)] = {}
	json_dict['row_' + str(i + 1)]['item_desc'] = item_desc
	json_dict['row_' + str(i + 1)]['date_info'] = date_dict
	json_dict['row_' + str(i + 1)]['price_info'] = price_dict
	#"date_info": date_dict, "price_info": price_dict}

#following, I've heard, is the way we should open output files
with open('data.json', 'w') as outfile:
	json.dump(json_dict, outfile)







