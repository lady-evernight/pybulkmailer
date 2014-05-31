import csv, os
filepath = os.path.abspath('data/nameslist.csv')

with open(filepath, 'rb') as csvfile:
	spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
	for row in spamreader:
		print row[0]