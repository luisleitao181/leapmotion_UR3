################################################################################
# Script to Analise the data of hand gesture                                   #
################################################################################

import numpy, csv

files = ['L0.csv','L1.csv','L2.csv','L3.csv','L4New.csv','L5.csv','R0.csv','R1.csv','R2.csv','R3.csv','R4.csv','R5.csv']

def main():
	for file in files:
		#initialize the occurance cases in each dataset
		case = [0,0,0,0,0,0]
		percent = [0.0,0.0,0.0,0.0,0.0,0.0]
		#read the dataset
		myCsv = csv.reader(open(file))
		#to avoid 
		for row in myCsv:
			if row[0] == '0':
				case[0] += 1
			elif row[0] == '1':
				case[1] += 1
			elif row[0] == '2':
				case[2] += 1
			elif row[0] == '3':
				case[3] += 1
			elif row[0] == '4':
				case[4] += 1
			elif row[0] == '5':
				case[5] += 1

		percent = [case[0]/2000.0,case[1]/2000.0,case[2]/2000.0,case[3]/2000.0,case[4]/2000.0,case[5]/2000.0]
		print "#######################"
		print file
		print "Types   | Occurence | % "
		print "cases 0: %4d ---- %.3f" % (case[0],percent[0])
		print "cases 1: %4d ---- %.3f"	 % (case[1],percent[1])
		print "cases 2: %4d ---- %.3f"  % (case[2],percent[2])
		print "cases 3: %4d ---- %.3f"  % (case[3],percent[3])
		print "cases 4: %4d ---- %.3f"  % (case[4],percent[4])
		print "cases 5: %4d ---- %.3f"  % (case[5],percent[5])


if __name__ == "__main__":
    main()