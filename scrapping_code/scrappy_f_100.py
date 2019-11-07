##
##
##
##

from splinter import Browser
from selenium import webdriver
import time
import datetime
import sys

start_letter = ""

def get_limits(year_start = -1,year_end = -1):
	if year_start == -1 and year_end == -1:
		date_limits = []
		date_limits.append(("1800/01/01","1890/01/01")) #0
		date_limits.append(("1890/01/01","1900/01/01")) #1
		date_limits.append(("1900/01/01","1902/01/01")) #2
		date_limits.append(("1902/01/01","1904/01/01")) #3
		date_limits.append(("1904/01/01","1906/01/01")) #4
		date_limits.append(("1906/01/01","1908/01/01")) #5
		date_limits.append(("1908/01/01","1910/01/01")) #6 
		date_limits.append(("1910/01/01","1915/01/01")) #7
		date_limits.append(("1915/01/01","1920/01/01")) #8
		date_limits.append(("1920/01/01","1925/01/01")) #9
		date_limits.append(("1925/01/01","1930/01/01")) #10
		date_limits.append(("1930/01/01","1940/01/01")) #11
		date_limits.append(("1940/01/01","1950/01/01")) #12
		date_limits.append(("1950/01/01","1960/12/31")) #13
		return date_limits

	else:
		date_limits = []
		for y in range(year_start, year_end):
			date_limits.append((str(y) + "/01/01",str(y+1) + "/01/01"))
		return date_limits

	return "KAKA"

def get_limits_2(name):

	if "_0_" in name:
		year = 1800
	if "_1_" in name:
		year = 1890
	if "_2_" in name:
		year = 1900
	if "_3_" in name:
		year = 1902
	if "_4_" in name:
		year = 1904
	if "_5_" in name:
		year = 1906
	if "_6_" in name:
		year = 1908
	if "_7_" in name:
		year = 1910
	if "_8_" in name:
		year = 1915
	if "_9_" in name:
		year = 1920
	if "_10_" in name:
		year = 1925
	if "_11_" in name:
		year = 1930
	if "_12_" in name:
		year = 1940
	if "_13_" in name:
		year = 1950
	
	shift = int(name[name.rfind("_")+1:])
	year = year + shift
    
	date_limits = []
	date_limits.append((str(year) + "/1/1",str(year) + "/4/1"))
	date_limits.append((str(year) + "/4/1",str(year) + "/7/1"))
	date_limits.append((str(year) + "/7/1",str(year) + "/10/1"))
	date_limits.append((str(year) + "/10/1",str(year+1) + "/1/1"))

	return date_limits


def get_limits_3(name):

	nnn = name.split("_")
	#print(nnn)

	if nnn[1] == "0" in name:
		year = 1800
	elif nnn[1] == "1" in name:
		year = 1890
	elif nnn[1] == "2" in name:
		year = 1900
	elif nnn[1] == "3" in name:
		year = 1902
	elif nnn[1] == "4" in name:
		year = 1904
	elif nnn[1] == "5" in name:
		year = 1906
	elif nnn[1] == "6" in name:
		year = 1908
	elif nnn[1] == "7" in name:
		year = 1910
	elif nnn[1] == "8" in name:
		year = 1915
	elif nnn[1] == "9" in name:
		year = 1920
	elif nnn[1] == "10" in name:
		year = 1925
	elif nnn[1] == "11" in name:
		year = 1930
	elif nnn[1] == "12" in name:
		year = 1940
	elif nnn[1] == "13" in name:
		year = 1950
	shift = int(nnn[2])
	year = year + shift

	if nnn[3] == "0":
		month = 1
	elif nnn[3] == "1":
		month = 4
	elif nnn[3] == "2":
		month = 7
	elif nnn[3] == "3":
		month = 10

	date_limits = []
	date_limits.append((str(year) + "/" + str(month) + "/1",str(year) + "/" + str(month+1) + "/1"))
	date_limits.append((str(year) + "/" + str(month+1) + "/1",str(year) + "/" + str(month+2) + "/1"))
	if month == 10:
		date_limits.append((str(year) + "/" + str(month+2) + "/1",str(year+1) + "/1/1"))
	else:
		date_limits.append((str(year) + "/" + str(month+2) + "/1",str(year) + "/" + str(month+3) + "/1"))

	return date_limits

def get_limits_4(name):

	last = name[name.rfind("_")+1:]
	name_old = name[:name.rfind("_")]

	date_limits_old = get_limits_3(name_old)
	date_limits_old = date_limits_old[int(last)]

	dstart = date_limits_old[0]
	dstart = dstart[:dstart.rfind("/")]

	dend = date_limits_old[1]
	dend = dend[:dend.rfind("/")]

	date_limits = []
	date_limits.append((dstart + "/01",dstart + "/05"))
	date_limits.append((dstart + "/06",dstart + "/10"))
	date_limits.append((dstart + "/11",dstart + "/15"))
	date_limits.append((dstart + "/16",dstart + "/20"))
	date_limits.append((dstart + "/21",dstart + "/25"))
	date_limits.append((dstart + "/26",dend + "/01"))

	#print(date_limits)
	#assert(False)
	return date_limits





def log_(file, message):
	if not file.endswith(".log"):
		file = file + ".log"
	logfile = open(file,"a+",encoding="UTF-8")
	logfile.write(message)
	logfile.close()

def get_family_name_html(family_name, browser_instance, date_from = "1800/01/01", date_to = "1960/12/31"):
	
	browser_instance.visit("https://search.cemla.com")

	## Add Cookie of Session ID, that allows us to bypass the captcha
	browser.cookies.add({'ASP.NET_SessionId': 'bu0fuu4s24byfhegcrs1izro'})

	## Search name
	browser_instance.fill('Lastname', family_name)
	browser_instance.fill('DateFrom', date_from)
	browser_instance.fill('DateTo', date_to)
	browser_instance.find_by_value('Buscar').click()
	## Choose "Show all" to get all the records
	browser_instance.find_by_value("-1").click()

	htmlcode = browser_instance.execute_script("return document.documentElement.outerHTML;")

	if "Debe ingresar el código Captcha correctamente" in htmlcode:
		raise Error("Session ID is no longer valid. Get new ID!")
		return ""

	return htmlcode

## Load possible family names

browser = Browser()
html_code_from_cemla = get_family_name_html('hola', browser)


print("LOADING NAMES")

already_ = []
empty_count = 0
with open("frikin_all_100_log.log","r",encoding="utf-8") as f:
	for line in f:
		try:
			if "(empty)" in line:
				empty_count += 1
			line = line.replace("\n","").replace(" (empty)","")
			already_.append(line.split("Downloaded ")[1])
		except:
			print(line)
			raise
	f.close()

possible_names = []
with open("family_names_frikin_all_100_3.txt","r",encoding="UTF-8") as f:
	for line in f:
		possible_names.append(line.replace("\n","").replace('"',"''"))
	f.close()

alset = set(already_)
print("All : " + str(len(alset) + empty_count))
possible_names = list(set(possible_names) - alset)
possible_names.append(already_[-1])
possible_names.sort()

total = len(possible_names)
print(total)
print("START")

#possible_names = []
#possible_names.append("maiolo")

date_limits = get_limits()

## Create browser instance
i = 0
j = 0
t1 = datetime.datetime.now()
t2 = datetime.datetime.now()
log_buffer = ""
essaies = 4

for name in possible_names:
	i += 1

	if name.count("_") > 4:
		print("REACHED FILE LIMIT: " + str(name))
		continue
	elif name.count("_") == 4:
		date_limits = get_limits_4(name)
	elif name.count("_") == 3:
		date_limits = get_limits_3(name)
	elif name.count("_") == 2:
		date_limits = get_limits_2(name)
	elif name.endswith("_0"):
		date_limits = get_limits(1800,1890)
	elif name.endswith("_1"):
		date_limits = get_limits(1890,1900)
	elif name.endswith("_2"):
		date_limits = get_limits(1900,1902)
	elif name.endswith("_3"):
		date_limits = get_limits(1902,1904)
	elif name.endswith("_4"):
		date_limits = get_limits(1904,1906)
	elif name.endswith("_5"):
		date_limits = get_limits(1906,1908)
	elif name.endswith("_6"):
		date_limits = get_limits(1908,1910)
	elif name.endswith("_7"):
		date_limits = get_limits(1910,1915)
	elif name.endswith("_8"):
		date_limits = get_limits(1915,1920)
	elif name.endswith("_9"):
		date_limits = get_limits(1920,1925)
	elif name.endswith("_10"):
		date_limits = get_limits(1925,1930)
	elif name.endswith("_11"):
		date_limits = get_limits(1930,1940)
	elif name.endswith("_12"):
		date_limits = get_limits(1940,1950)
	elif name.endswith("_13"):
		date_limits = get_limits(1950,1960)
	name_ = name
	if "_" in name:
		name = name[0:name.find("_")]

	for k in range(0,len(date_limits)):

		##
		##time.sleep(7)
		##

		date_from = date_limits[k][0]
		date_to = date_limits[k][1]
		essai = 4
		j += 1

		while essai > 0:
			try:
				#if essai > 1:
				#	time.sleep(10)
				if j % 10 == 0:
					print(str(i) + "/" + str(total) + "  " + str((datetime.datetime.now() - t1).total_seconds()) + "  " + str((datetime.datetime.now() - t2).total_seconds()))
					log_("frikin_all_100_log",log_buffer)
					log_buffer = ""

				t2 = datetime.datetime.now()

				#time.sleep(0.2)
				if j % 1000 == 0:
					time.sleep(10)

				html_code_from_cemla = get_family_name_html(name, browser, date_from, date_to)

				if html_code_from_cemla == "":
					log_("frikin_all_100_log","Error in name " + name)
					print("ERROR IN NAME " + name + ". ABORTING ...")
					essai = 0
					break

				if name.upper() not in html_code_from_cemla: 
					#log_("frikin_all_100_log","Downloaded " + name + " (empty)")
					log_buffer += "> " + str(datetime.datetime.now()) + "  " + "Downloaded " + name_ + " (empty)" + "\n"
					essai = 0
					continue

				#log_("frikin_all_100_log","Downloaded " + name)
				log_buffer += "> " + str(datetime.datetime.now()) + "  " + "Downloaded " + name_ + "\n"
				output = open("frikin_all_100/" + name_.replace("?","_q") + "_" + str(k) + ".html","w+",encoding="UTF-8")
				output.write(html_code_from_cemla)
				output.close()
				essai = 0
			except:
				essai = essai - 1
				print("   essai = " + str(essai))
				if essai == 1:
					time.sleep(60*30)
				#if essai == 2:
				#	time.sleep(60*15)
				if essai == 0:
					raise
				
log_("frikin_all_100_log",log_buffer)
print("FINISHED")
