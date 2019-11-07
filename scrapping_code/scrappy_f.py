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
if len(sys.argv) == 2:
	start_letter = sys.argv[1]
	print("Start letter : " + start_letter)

def log_(file, message):
	if not file.endswith(".log"):
		file = file + ".log"
	logfile = open(file,"a+",encoding="UTF-8")
	logfile.write(message)
	logfile.close()

def get_family_name_html(family_name, browser_instance):
	
	browser_instance.visit("https://search.cemla.com")

	## Add Cookie of Session ID, that allows us to bypass the captcha
	browser.cookies.add({'ASP.NET_SessionId': 'bu0fuu4s24byfhegcrs1izro'})

	## Search name
	browser_instance.fill('Lastname', family_name)
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
with open("frikin_all_log.log","r",encoding="utf-8") as f:
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
with open("family_names_frikin_all_3.txt","r",encoding="UTF-8") as f:
	for line in f:
		if start_letter == "" or line.startswith(start_letter):
			possible_names.append(line.replace("\n","").replace('"',""))
	f.close()

alset = set(already_)
print("All : " + str(len(alset) + empty_count))
possible_names = list(set(possible_names) - alset)
possible_names.sort()

total = len(possible_names)
print(total)
print("START")


## Create browser instance
i = 0
t1 = datetime.datetime.now()
t2 = datetime.datetime.now()
log_buffer = ""
essaies = 4

for name in possible_names:
	i += 1
	essai = 4

	if name == "":
		continue

	while essai > 0:
		try:
			#if essai > 1:
			#	time.sleep(10)
			if i % 10 == 0:
				print(str(i) + "/" + str(total) + "  " + str((datetime.datetime.now() - t1).total_seconds()) + "  " + str((datetime.datetime.now() - t2).total_seconds()))
				log_("frikin_all_log",log_buffer)
				log_buffer = ""

			t2 = datetime.datetime.now()

			####
			##time.sleep(7)
			####

			if i % 1000 == 0:
				time.sleep(10)

			html_code_from_cemla = get_family_name_html(name, browser)

			if html_code_from_cemla == "":
				log_("frikin_all_log","Error in name " + name)
				print("ERROR IN NAME " + name + ". ABORTING ...")
				essai = 0
				break

			if name.upper() not in html_code_from_cemla: 
				#log_("frikin_all_log","Downloaded " + name + " (empty)")
				log_buffer += "> " + str(datetime.datetime.now()) + "  " + "Downloaded " + name + " (empty)" + "\n"
				essai = 0
				continue

			#log_("frikin_all_log","Downloaded " + name)
			log_buffer += "> " + str(datetime.datetime.now()) + "  " + "Downloaded " + name + "\n"
			output = open("frikin_all/" + name.replace("?","_q") + ".html","w+",encoding="UTF-8")
			output.write(html_code_from_cemla)
			output.close()
			essai = 0
		except:
			essai = essai - 1
			print("   essai = " + str(essai))
			if essai == 1:
				time.sleep(60*40)
			if essai == 0:
				raise
				
log_("frikin_all_log",log_buffer)
print("FINISHED")
