import urllib2

class SwissGrid:
	
	def __init__(self):
		pass
	
	def get_frequencies(self):
		datfile = urllib2.urlopen("https://data.swissgrid.ch/wam/scripts/getData.php")
		data = [[v for v in line.split('!') if v != ''] for line in datfile.read().split('//') if line != '']
		datfile.close()
		
		for d in data:
			if len(d) == 3:
				d[2] = float(d[2])
		
		return data
  
sg = SwissGrid()
frequencies = sg.get_frequencies()

print(frequencies)




		