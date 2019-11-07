import os
from bs4 import BeautifulSoup
import time
import datetime

## ID
## Surname
## Name
## Year of arrival
## Month of arrival
## Day of arrival
## Ship
## Port
## Origin
## Age
## Gender
## Martial Satus
## Relgion
## Profession
## Place of birth

def log_(file, message):
	if not file.endswith(".log"):
		file = file + ".log"
	logfile = open(file,"a+",encoding="UTF-8")
	logfile.write(message)
	logfile.close()

def is_hundred(filename):
	if os.path.isfile("frikin_all/" + filename + ".hund"):
		os.remove("frikin_all/" + filename)
		print("REMOVED FILE: " + filename)
	
	os.rename("frikin_all/" + filename,"frikin_all/" + filename + ".hund")
	
	output = open("family_names_frikin_all_100_3.txt","a+",encoding="UTF-8")
	output.write(filename.replace(".html","") + "\n")
	output.close()

print("Loading...")
already_ = []
with open("tablerizer.log","r",encoding="utf-8") as f:
	for line in f:
		already_.append(line.split("Tablerized ")[1].replace("\n",""))
	f.close()
print("Already logged " + str(len(already_)) + " names")

files_ = []
for filename in os.listdir("frikin_all"):
	if filename.endswith("html"):
		files_.append(filename)

files_ = list(set(files_) - set(already_))
files_.sort()

print("Loaded " + str(len(files_)) + " files")
print("Start...")

#############################################################################################

DATA = []
i = 0
lendata = 0
t1 = datetime.datetime.now()

for filename in files_:
	i += 1
	try:
		input_f = open('frikin_all/' + filename,"r",encoding="UTF-8")
		content = input_f.read()
		input_f.close()
		
		if "Se obtuvieron 100 resultados" in content:
			is_hundred(filename)
			continue

		soup = BeautifulSoup(content,features="lxml")
		

		soup = soup.find("table")
		rows = soup.findAll("tr")

		for r in rows:
			cols = list(r.findAll("td"))
			if len(cols) < 1:
				continue

			new_ = {}

			new_["filename"] = filename
			new_["surname"] = cols[0].text.strip()
			new_["name"] = cols[1].text.strip()
			new_["age"] = cols[2].text.strip()
			new_["marital_status"] = cols[3].text.strip()
			new_["origin"] = cols[4].text.strip()
			new_["place_of_birth"] = cols[5].text.strip()
			new_["profession"] = cols[6].text.strip()

			date_of_arrival = cols[7].text.strip().split("/")
			new_["year_of_arrival"] = date_of_arrival[0]
			new_["month_of_arrival"] = date_of_arrival[1]
			new_["day_of_arrival"] = date_of_arrival[2]

			new_["ship"] = cols[8].text.strip()
			new_["port"] = cols[9].text.strip()
			new_["religion"] = ""
			new_["gender"] = ""

			DATA.append(new_)
			lendata += 1
			continue

	except:
		print("ERROR IN FILE: " + filename)


	if i % 1E3 == 0:
		print("Saving   i=" + str(i) + "   len(data)=" + str(lendata) + "   ETA=" + str((datetime.datetime.now() - t1).total_seconds()))

		log_buffer = ""
		output_buffer = ""
		
		for item in DATA:
			output_buffer += item["surname"].upper() + ","
			output_buffer += item["name"].upper() + ","
			output_buffer += item["year_of_arrival"].upper().replace(" ","") + ","
			output_buffer += item["month_of_arrival"].upper().replace(" ","") + ","
			output_buffer += item["day_of_arrival"].upper().replace(" ","") + ","
			output_buffer += item["ship"].upper() + ","
			output_buffer += item["port"].upper() + ","
			output_buffer += item["origin"].upper() + ","
			output_buffer += item["age"].upper().replace(" ","") + ","
			output_buffer += item["gender"].upper() + ","
			output_buffer += item["marital_status"].upper() + ","
			output_buffer += item["religion"].upper() + ","
			output_buffer += item["profession"].upper() + ","
			output_buffer += item["place_of_birth"].upper() + "\n"

			log_buffer += "> Tablerized " + item["filename"] + "\n"
		
		DATA.clear()
		output = open("output.csv","a+",encoding = "UTF-8")
		output.write(output_buffer)
		output.close()
		log_("tablerizer.log",log_buffer)

## 
## 
##

print("Saving   i=" + str(i) + "   len(data)=" + str(lendata) + "   ETA=" + str((datetime.datetime.now() - t1).total_seconds()))

log_buffer = ""
output = open("output.csv","a+",encoding = "UTF-8")
for item in DATA:
	output.write(item["surname"].upper() + ",")
	output.write(item["name"].upper() + ",")
	output.write(item["year_of_arrival"].upper().replace(" ","") + ",")
	output.write(item["month_of_arrival"].upper().replace(" ","") + ",")
	output.write(item["day_of_arrival"].upper().replace(" ","") + ",")
	output.write(item["ship"].upper() + ",")
	output.write(item["port"].upper() + ",")
	output.write(item["origin"].upper() + ",")
	output.write(item["age"].upper().replace(" ","") + ",")
	output.write(item["gender"].upper() + ",")
	output.write(item["marital_status"].upper() + ",")
	output.write(item["religion"].upper() + ",")
	output.write(item["profession"].upper() + ",")
	output.write(item["place_of_birth"].upper() + "\n")

	log_buffer += "> Tablerized " + item["filename"] + "\n"
output.close()
DATA.clear()
log_("tablerizer.log",log_buffer)

print("Finished")
