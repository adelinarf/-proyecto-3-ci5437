from library import *
from decode import *
import sys
import subprocess
import time

def run(name,dimacs_file):
	data = open_file(name)
	n,z,m = values(data)
	hours_exact = get_hours_exact(data)
	variables,inv_var=get_variables(n,z,m,types_,hours_exact)
	print(n,"players")
	print(z,"days")
	print(m,"hours per day")

	C1 = clausule_play_twice(n,z,m,hours_exact,variables,inv_var)  
	C2 = clausule_play_once_per_day(n,z,m,hours_exact,variables,inv_var)  
	C3 = clausule_non_consecutive_days(n,z,m,hours_exact,variables) 
	C4 = clausule_not_at_same_time(n,m,z,hours_exact,variables,inv_var) 
	C5 = clausule_all(n,m,z,hours_exact,variables) 

	C= C1+C2+C3+C4+C5

	clausulas = clausula_multiple(C)

	create_dimacs_file(clausulas,len(variables),dimacs_file)
	dates_for = dates_list(data)
	return dates_for,hours_exact,inv_var,data

def main():
	if len(sys.argv)<5 or len(sys.argv)>5:
		print("There should be 4 arguments for this file, the name of the json file as: file_name.json and the name of the ")
	else:
		name_json = sys.argv[1]
		dimacs_file = sys.argv[2]
		output_file = sys.argv[3]
		calendar_name = sys.argv[4]
		if ".json" in name_json and ".txt" in dimacs_file and ".txt" in output_file and ".ics" in calendar_name:
			print("RUNNING...")
			try:
				start = time.time()
				dates_for,hours_exact,inv_var,data = run(name_json,dimacs_file)
				subprocess.run(["./glucose", dimacs_file,output_file]) 
				decode(output_file,calendar_name,inv_var,dates_for,hours_exact,data)
				end = time.time()
				print("The ics file:",calendar_name,"has been created")
				print("The program ran",end-start,"seconds")
			except:
				print("The file",name_json,"doesn't exist")
		else:
			print("The arguments needs to include the full name of the file i.e. file.json, including the extension")

main()

