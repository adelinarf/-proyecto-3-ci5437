import json
import datetime

def open_file(name):
	f = open(name)
	data = json.load(f)
	f.close()
	return data


def values(data):
	sd = datetime.date.fromisoformat(data["start_date"])
	ed = datetime.date.fromisoformat(data["end_date"])
	st = datetime.time.fromisoformat(data["start_time"])
	et = datetime.time.fromisoformat(data["end_time"])

	n = len(data['participants'])  #cantidad de participantes
	z = (ed-sd).days    #cantidad de dias

	m = datetime.datetime.strptime(formatted(data["end_time"]), '%H:%M:%SZ')-datetime.datetime.strptime(formatted(data["start_time"]), '%H:%M:%SZ')
	m = int(m.seconds/3600)  #cantidad de horas por dia
	return n,z,m


def formatted(data):
	SH = datetime.time.fromisoformat(data)
	return (str(SH.hour)+":"+str(SH.minute)+":"+str(SH.second)+"Z")

def get_hours_exact(data):	
	starting_hour = datetime.datetime.strptime(formatted(data["start_time"]), '%H:%M:%SZ')
	ending_hour = datetime.datetime.strptime(formatted(data["end_time"]), '%H:%M:%SZ')
	new = 0
	if starting_hour.minute!=0:
		new=60-starting_hour.minute
	starting_hour = starting_hour + datetime.timedelta(minutes=new)

	hours_exact=[]
	ending = ending_hour.hour
	hour = None
	while hour!=ending:
		hour = starting_hour.hour
		hours_exact.append(starting_hour)
		starting_hour = starting_hour + datetime.timedelta(hours=1)
	return hours_exact

#fecha inicial y final
def dates_list(data):
	sd = datetime.date.fromisoformat(data["start_date"])
	ed = datetime.date.fromisoformat(data["end_date"])
	dates_for = []
	starting_day = sd
	ending_day = ed
	day = None
	while day!=ending_day:
		day = starting_day
		dates_for.append(starting_day)
		starting_day = starting_day + datetime.timedelta(days=1)
	return dates_for


types_ = ["L","V"]


def getFinal(h,hours_exact):
	if h+2<=len(hours_exact):
		return [h + 2]
	else:
		return []


def getString(i,d,f,ff,t):
	return "P"+str(i)+"_"+str(d)+"_"+str(f)+"_"+str(ff)+"_"+str(t)

def get_variables(n,z,m,types_,hours_exact):
	variables={}
	inv_var = {}
	count=1
	for i in range(n):
		for d in range(z):
			for f in range(m):
				for t in types_:
					for ff in getFinal(f,hours_exact):
						string=getString(i,d,f,ff,t)
						variables[string]=count
						inv_var[count] = (i,d,f,ff,t)
						count+=1
	return variables,inv_var

def return_variables(n,z,m,types_,hours_exact):
	variables={}
	inv_var = {}
	count=1
	variab = []
	for i in range(n):
		for d in range(z):
			for f in range(m):
				for t in types_:
					for ff in getFinal(f,hours_exact): 
						variab.append(tuple([i,d,f,ff,t]))
	return variab

def getContrary(t):
	if t=="V":
		return "L"
	elif t=="L":
		return "V"

#Dos juegos no pueden ser al mismo tiempo
def clausule_not_at_same_time(n,m,z,hours_exact,variables,inv_var):
	W=[]
	for i in range(n):
		for d in range(z):
			for f in range(m):
				for ff in getFinal(f,hours_exact):
					for t in types_:
						first = variables[getString(i,d,f,ff,t)]
						l = [-first]
						for ip in range(n):
							if i!=ip:
								x=variables[getString(ip,d,f,ff,getContrary(t))]
								l.append(-x)
							for d2 in range(z):
								for f2 in range(m):
									for ff2 in getFinal(f2,hours_exact):
										for t2 in types_:
											if d2==d and f2==f and ff2==ff and ip!=i and t2==t:
												third = variables[getString(ip,d,f2,ff2,t2)]
												l.append(third)
											#mismo dia pero hace overlap
											if d2==d and (checkOverlap(f,ff,f2,ff2) or checkOverlap(f2,ff2,f,ff)) and f2!=f and ff2!=ff:
												third = variables[getString(ip,d2,f2,ff2,t2)]
												l.append(third)
											if (f2==f and ff2==ff and t!=t2 and d==d2 and i!=ip):
												#print("no",getString(i,d,f2,ff2,t2))
												second = variables[getString(i,d,f2,ff2,t2)]
												l.append(second)
						W.append(l)
	return W

def checkOverlap(s1,e1,s2,e2): 
	if s1<s2<e1 or s2<s1<e2<e1:
		return True
	else:
		return False


def clausule_all(n,m,z,hours_exact,variables):
	l=[]
	for i in range(n):
		for d in range(z):
			for f in range(m):
				for t in types_:
					for ff in getFinal(f,hours_exact):
						first = variables[getString(i,d,f,ff,t)]
						for ip in range(n):
							second = variables[getString(ip,d,f,ff,getContrary(t))]
							l.append([-first,-second])
	return l

#Cada participante juega 2 veces como visitante
def clausule_play_twice(n,z,m,hours_exact,variables,inv_var):	
	Z=[]
	for i in range(n):
		for d in range(z):
			for f in range(m):
				for ff in getFinal(f,hours_exact):
					for t in types_:
						first = variables[getString(i,d,f,ff,t)]
						nfirst = variables[getString(i,d,f,ff,getContrary(t))]
						for ip in range(n):
							second = variables[getString(ip,d,f,ff,getContrary(t))]
							for d2 in range(z):
								for f2 in range(m):
									for t2 in types_:
										if d!=d2:
											for ff2 in getFinal(f2,hours_exact):
												third = variables[getString(i,d2,f2,ff2,t)]
												fourth = variables[getString(ip,d2,f2,ff2,getContrary(t))]
												lista=[first,second,third,fourth] #poner negativos
												for d3 in range(z):
													for f3 in range(m):
														for ff3 in getFinal(f3,hours_exact):
															if d3==d and f3!=f and ff3!=ff and f3!=f2 and ff3!=ff2:
																third = variables[getString(i,d3,f3,ff3,t)]
																lista.append(third)
															if d3==d2 and f3!=f and ff3!=ff and f3!=f2 and ff3!=ff2:
																third = variables[getString(i,d3,f3,ff3,t)]
																lista.append(third)
															if d3!=d and d3!=d2:
																third = variables[getString(i,d3,f3,ff3,t)]
																lista.append(third)
												Z.append(lista)
	return Z

#Cada participante juega 1 vez por dia
def clausule_play_once_per_day(n,z,m,hours_exact,variables,inv_var):
	C2=[]
	for i in range(n):
		for d in range(z):
			for f in range(m):
				for t in types_:
					for ff in getFinal(f,hours_exact):
						first = variables[getString(i,d,f,ff,t)]
						lista=[-first] 
						for f2 in range(m):
							for ff2 in getFinal(f2,hours_exact):
								for t2 in types_:
									if (f2!=f and ff2!=ff):
										second = variables[getString(i,d,f2,ff2,t2)]
										lista.append(-second)
									if (f2==f and ff2==ff and t!=t2):
										second = variables[getString(i,d,f2,ff2,t2)]
										lista.append(-second)
						C2.append(lista)
										
	return C2

#Un participante no puede jugar de "visitante" en dos días consecutivos, ni de "local" dos días seguidos.
def clausule_non_consecutive_days(n,z,m,hours_exact,variables):
	C=[]
	for i in range(n):
		for d in range(z):
			for f in range(m):
				for ff in getFinal(f,hours_exact):
					for t in types_:
						first = variables[getString(i,d,f,ff,t)]
						for f2 in range(m):
							for ff2 in getFinal(f2,hours_exact):
								if d+1<z:
									second = variables[getString(i,d+1,f2,ff2,t)]
									C.append([-first,second])
	return C

def clausula_multiple(C):
	claus1 = []
	for x in C:
		clausula1 = ""
		for y in x:
			clausula1+= str(y) + " "
		claus1.append(clausula1+"0")
	return claus1

def create_dimacs_file(clausulas,nvar,name):
	comments = "c Comments are ignored\n"
	cnf = "p cnf "+str(nvar)+" "+str(len(clausulas))+"\n"
	with open(name, 'a') as the_file:
		the_file.write(comments)
		the_file.write(cnf)
		for clausula in clausulas:
			the_file.write(clausula+"\n")
