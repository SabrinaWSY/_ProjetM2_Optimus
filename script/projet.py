# -*- coding: utf-8 -*-
# projet_optimus.py
# Ce script appartient au groupe de Siyu WANG, Shuai GAO et Chen SUN
# Le programme génere un fichier xml et 1 fenêtre de graphe avec les données choisies depuis les fichiers de sources
# Sources de Données: API: https://data.iledefrance.fr/explore/dataset/immeubles-proteges-au-titre-des-monuments-historiques/api/
#					  CSV: https://data.iledefrance.fr/explore/dataset/salle_de_cinema_ile-de-france/table/
#					  CSV: https://opendata.paris.fr/explore/dataset/tournagesdefilmsparis2011/information/
# Résultat: OUTPUT.xml généré dans le répertoire 'xml'
#			Data_par_arrondissement.png
##############################################################

from time import sleep
import json
import requests
from collections import Counter
import re
import csv
from decimal import Decimal
import matplotlib.pyplot as plt
import numpy as np


def read_csv_file(csv_file, sep=";"):
	"""
	Read the csv file and return the content as a list
	"""
	data = list()
	with open(csv_file) as csv_input:
		d_reader = csv.DictReader(csv_input, delimiter=sep)
		for line in d_reader:
			data.append(line)
	return data


def data2counter_cinema(data):
	"""
	Turn data into a Counter object based on the column 'code_insee'
	"""
	paris_cinema = list()
	cpt = Counter()
	for item in data:
		code_insee = item['code INSEE']
		c = code_insee[2].replace('1', '0')
		code_insee = str(code_insee[0]+code_insee[1]+c+code_insee[3]+code_insee[4])
		if re.match("75+", code_insee):
			paris_cinema.append(item)
			cpt[code_insee] += 1
	return cpt, paris_cinema


def data2counter_tournage_paris(data):
	"""
	Turn data into a Counter object based on the column 'Arrondissement'
	"""
	entries = set()
	cpt = Counter()
	for item in data:
		adresse = item['Adresse']
		arrondissement = item['Arrondissement']
		key = (adresse, arrondissement)
		if re.match("75+", arrondissement):
			entries.add(key)
	for k, v in entries:
		cpt[v] += 1
	return entries, cpt


def data2counter_tournage_type(data):
	"""
	Turn data into a Counter object based on the column 'Arrondissement' and 'type de tournage'
	"""
	entries = set()
	cpt_total = Counter()
	cpt_TELEFILM = Counter()
	cpt_SERIE_TELEVISEE = Counter()
	cpt_LONG_METRAGE = Counter()
	for item in data:
		adresse = item['Adresse']
		arrondissement = item['Arrondissement']
		type_tournage = item['Type de tournage']
		key = (adresse, arrondissement, type_tournage)
		if re.match("75*", arrondissement):
			entries.add(key)
	for k, v, x in entries:
		cpt_total[x] += 1
	return entries, cpt_total


def get_api(lien):
	"""
	Get data from the link API and return the content as a python object
	"""
	# Make a get request with parameters
	response = requests.get(lien)
	# Get the response data as a python object.  Verify that it's a dictionary.
	data = response.json()
	# print(type(data))
	# print(data.keys())
	return data


def traitement_json(data):
	"""
	Data processing and get the total number of 'monument historique' in Paris, and the number of hotels and religious monuments
	"""
	record = data['records']
	cpt_total = Counter()
	cpt_hotel = Counter()
	cpt_religieux = Counter()
	Mo_total = set()
	Mo_hotel = set()
	Mo_religieux = set()
	for i in record:
		recordid = i['recordid']
		field = i['fields']
		code = field['insee']
		c = code[2].replace('1', '0')
		code_insee = str(code[0]+code[1]+c+code[3]+code[4])
		# Unifier les appelations des lieus en minuscule
		description = field['tico'].lower()
		monuments = (recordid, code_insee, description)
		Mo_total.add(monuments)  # set de tous les monuments historiques
	# comptage basé sur la colonne 'b' code_insee
	for a, b, c in Mo_total:
		cpt_total[b] += 1
	return cpt_total


def write_xml_file(cinemas, lieus, cpt_cinemas, paris_cinema, tournages, monuments, cpt_total_mo, cpt_tournages, cpt_total, arrons, file):
	"""
	Write an output xml file
	"""
	with open(file, 'w', encoding='utf-8') as xmlfile:
		xmlfile.write("<Data>\n")
		# write the first line
		xmlfile.write(
			f"<Paris>\n\t<lieu_tournage>\n\t\t<nombre>{len(lieus)}</nombre>\n\t\t<pourcentage>100%</pourcentage>\n\t</lieu_tournage>\n\t<cinema>\n\t\t<nombre>{len(paris_cinema)}</nombre>\n\t\t<pourcentage>100%</pourcentage>\n\t</cinema>\n\t<monument>\n\t\t<nombre>{monuments['nhits']}</nombre>\n\t\t<pourcentage>100%</pourcentage>\n\t</monument>\n</Paris>")
		# write the following lines with a loop
		for i in arrons:
			#if cpt_cinemas[i] != 0:
			xmlfile.write(f"\n<arron{i}>\n\t<lieu_tournage>\n\t\t<nombre>{cpt_tournages[i]}</nombre>\n\t\t<pourcentage>{str(round((cpt_tournages[i]/len(lieus))*100, 2)) + '%'}</pourcentage>\n\t</lieu_tournage>\n\t<cinema>\n\t\t<nombre>{cpt_cinemas[i]}</nombre>\n\t\t<pourcentage>{str(round((cpt_cinemas[i]/len(paris_cinema))*100, 2)) + '%'}</pourcentage>\n\t</cinema>\n\t<monument>\n\t\t<nombre>{cpt_total_mo[i]}</nombre>\n\t\t<pourcentage>{str(round((cpt_total_mo[i]/monuments['nhits'])*100, 2)) + '%'}</pourcentage>\n\t</monument>\n</arron{i}>")
			#else:
				#xmlfile.write(f"\t<Arrondissement>{i}</Arrondissement>\n\t<lieu_tournage>\n\t\t<Nombre>{cpt_tournages[i]}</Nombre>\n\t\t<pourcentage>{str(round((cpt_tournages[i]/len(lieus))*100, 2)) + '%'}</pourcentage>\n\t</lieu_tournage>\n\t<cinema>\n\t\t<nombre>{cpt_cinemas[i]}</nombre>\n\t\t<pourcentage>{str(round((cpt_cinemas[i]/len(paris_cinema))*100, 2)) + '%'}</pourcentage>\n\t</cinema>\n\t<monument>\n\t\t<nombre>{cpt_total_mo[i]}</nombre>\n\t\t<pourcentage>{str(round((cpt_total_mo[i]/monuments['nhits'])*100, 2)) + '%'}</pourcentage>\n\t</monument>")
		xmlfile.write("\n</Data>")


def write_csv_file(cinemas, lieus, cpt_cinemas, paris_cinema, tournages, monuments, cpt_total_mo, cpt_tournages, cpt_total, arrons, file):
	"""
	Write an output csv file
	"""
	with open(file, 'w', encoding='utf-8') as csvfile:
		fieldnames = ['Departement', 'Arrondissement', 'Nb lieu de tournage 2016', 'Nb lieus de tournage / Nb total', 'Nb de cinéma',
		'Nb de cinéma / Nb total', 'Nb monuments historiques', 'Nb monuments historiques / Nb total',
		'Nb lieus de tournage / Nb monuments historiques', 'Nb monuments historiques / Nb de cinémas',
		'Nb lieus de tournage / Nb de cinémas']
		writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=";")
		writer.writeheader()

		# écriture du première ligne
		writer.writerow({'Departement': 'Paris', 'Arrondissement': 'Tout Paris', 'Nb lieu de tournage 2016': len(lieus),
		'Nb lieus de tournage / Nb total': '100%', 'Nb de cinéma': len(paris_cinema), 'Nb de cinéma / Nb total': '100%',
		'Nb monuments historiques': monuments['nhits'], 'Nb monuments historiques / Nb total': '100%',
		'Nb lieus de tournage / Nb monuments historiques': round((len(lieus)/monuments['nhits']), 2),
		'Nb monuments historiques / Nb de cinémas': round((monuments['nhits']/len(cinemas)), 2),
		'Nb lieus de tournage / Nb de cinémas': round((len(lieus)/len(cinemas)), 2)})

		# écriture des lignes suivantes
		for i in arrons:
			if cpt_cinemas[i] != 0:
				writer.writerow({'Departement': 'Paris', 'Arrondissement': i, 'Nb lieu de tournage 2016': cpt_tournages[i],
				'Nb lieus de tournage / Nb total': str(round((cpt_tournages[i]/len(lieus))*100, 2)) + '%',
				'Nb de cinéma': cpt_cinemas[i], 'Nb de cinéma / Nb total': str(round((cpt_cinemas[i]/len(paris_cinema))*100, 2)) + '%',
				'Nb monuments historiques': cpt_total_mo[i], 'Nb monuments historiques / Nb total': str(round((cpt_total_mo[i]/monuments['nhits'])*100, 2)) + '%',
				'Nb lieus de tournage / Nb monuments historiques': round((cpt_tournages[i]/cpt_total_mo[i]), 2),
				'Nb monuments historiques / Nb de cinémas': round((cpt_total_mo[i]/cpt_cinemas[i]), 2),
				'Nb lieus de tournage / Nb de cinémas': round((cpt_tournages[i]/cpt_cinemas[i]), 2)})
			else:
				writer.writerow({'Departement': 'Paris', 'Arrondissement': i, 'Nb lieu de tournage 2016': cpt_tournages[i],
				'Nb lieus de tournage / Nb total': str(round((cpt_tournages[i]/len(lieus))*100, 2)) + '%',
				'Nb de cinéma': cpt_cinemas[i], 'Nb de cinéma / Nb total': str(round((cpt_cinemas[i]/len(paris_cinema))*100, 2)) + '%',
				'Nb monuments historiques': cpt_total_mo[i], 'Nb monuments historiques / Nb total': str(round((cpt_total_mo[i]/monuments['nhits'])*100, 2)) + '%',
				'Nb lieus de tournage / Nb monuments historiques': round((cpt_tournages[i]/cpt_total_mo[i]), 2),
				'Nb monuments historiques / Nb de cinémas': 'Pas de cinéma dans cet arrondissement',
				'Nb lieus de tournage / Nb de cinémas': 'Pas de cinéma dans cet arrondissement'})


def get_nb_for_graphes(arrons, cpt_tournages, cpt_cinemas, cpt_total_mo):
	"""
	Create lists of values for graph generation
	"""
	valeur_cinema = list()
	valeur_tournage = list()
	valeur_monument = list()
	for i in arrons:
		valeur_cinema.append(cpt_cinemas[i])
		valeur_tournage.append(cpt_tournages[i])
		valeur_monument.append(cpt_total_mo[i])
	return valeur_cinema, valeur_tournage, valeur_monument


def draw_graph_bar(arrons, valeur_cinema, valeur_tournage, valeur_monument):
	"""
	Show 1 bar graph of numbers of cinema, lieu de tournage and monument historique by each arrondissement
	"""
	N = 20  # nombre de arrondissement
	ind = np.arange(N)  # the x locations for the groups
	width = 0.17	   # the width of the bars

	fig = plt.figure()
	ax = fig.add_subplot(111)

	yvals = valeur_cinema
	rects1 = ax.bar(ind, yvals, width, color='r')
	zvals = valeur_tournage
	rects2 = ax.bar(ind+width, zvals, width, color='g')
	kvals = valeur_monument
	rects3 = ax.bar(ind+width*2, kvals, width, color='b')

	ax.set_ylabel('Nombre')
	ax.set_xticks(ind+width)
	ax.set_xticklabels(('1er', '2me', '3me', '4me', '5me', '6me', '7me', '8me', '9me', '10me',
					   '11me', '12me', '13me', '14me', '15me', '16me', '17me', '18me', '19me', '20me'))
	ax.legend((rects1[0], rects2[0], rects3[0]), ('cinema',
			  'lieu de tournage', 'monuments historiques'))

	def autolabel(rects):
		for rect in rects:
			h = rect.get_height()
			ax.text(rect.get_x()+rect.get_width()/2., 1.05*h, '%d' % int(h),
					ha='center', va='bottom')

	autolabel(rects1)
	autolabel(rects2)
	autolabel(rects3)
	# plt.savefig('Data_par_arrondissement.png', bbox_inches='tight')
	plt.show()


def main():
	monuments = get_api(
		"https://data.iledefrance.fr/api/records/1.0/search/?dataset=immeubles-proteges-au-titre-des-monuments-historiques&rows=1844&refine.code_departement=75")
	print("*"*70)
	print("Projet Document 2019/20 de Siyu WANG, Shuai GAO et Chen SUN")
	print("*"*70)
	#sleep(1.5)
	print(f"Il y a {monuments['nhits']} monuments historiques à Paris")

	print("-"*50)
	#sleep(1)
	cpt_total_mo = traitement_json(monuments)

	for key, value in cpt_total_mo.items():
		if key != '20020':
			print(f"{key}:{value} monuments historiques")
	print("-"*50)
	#sleep(1)

	cinemas = read_csv_file("./data/CSV/salle_de_cinema_ile-de-france.csv")
	print(f"Il y a {len(cinemas)} cinemas dans le fichier")
	print("-"*50)
	#sleep(1)

	cpt_cinemas, paris_cinema = data2counter_cinema(cinemas)
	print(f"Il y a {len(paris_cinema)} cinemas à Paris")
	print("-"*50)
	#sleep(1)
	for key, value in cpt_cinemas.items():
		print(f"{key}:{value} cinemas")
	print("-"*50)
	#sleep(1)

	tournages = read_csv_file("./data/CSV/tournagesdefilmsparis2016_corrigé.csv")
	print(f"Il y a {len(tournages)} lieus de tournage dans le fichier")
	print("-"*50)
	#sleep(1)

	lieus, cpt_tournages = data2counter_tournage_paris(tournages)
	print(f"Il y a {len(lieus)} lieus de tournage à Paris")
	print("-"*50)
	#sleep(1)
	for key, value in cpt_tournages.items():
		print(f"{key}:{value} lieus de tournage")

	print("-"*50)
	#sleep(1)
	types, cpt_total = data2counter_tournage_type(tournages)
	for key, value in cpt_total.items():
		print(f"{key}:{value} lieus de tournage")
	print("-"*50)
	#sleep(1)

	arrons = cpt_tournages.keys()
	arrons = sorted(arrons)
	
	# write_output_file(cinemas, lieus, cpt_cinemas, paris_cinema, tournages, monuments,
	# 				  cpt_total_mo, cpt_tournages, cpt_total, arrons, "TABLEAUX-OUTPUT.csv")
	# print("Fichier output TABLEAUX-OUTPUT.csv généré!")
	# print("-"*50)
	write_xml_file(cinemas,lieus, cpt_cinemas, paris_cinema, tournages, monuments, cpt_total_mo, cpt_tournages, cpt_total, arrons, "./xml/output.xml")
	print("Fichier output output.xml généré!")
	print("-"*50)
	valeur_cinema, valeur_tournage, valeur_monument = get_nb_for_graphes(arrons, cpt_tournages, cpt_cinemas, cpt_total_mo)
	draw_graph_bar(arrons, valeur_cinema, valeur_tournage, valeur_monument)
	print("Graphes générés!")
	print("-"*50)

if __name__ == "__main__":
	main()
