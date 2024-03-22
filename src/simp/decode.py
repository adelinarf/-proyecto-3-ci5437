from ics import Calendar, Event
import datetime

def get_model_from_file(name):
	file = open(name, "r")
	content = file.read()
	file.close()
	zp = content.split(" ")
	model = []
	for x in range(len(zp)-1):
		model.append(int(zp[x]))
	return model


def find_type(t):
	if t=="V":
		return "visitor"
	else:
		return "local"


def imprimir(i,d,f,ff,t):
	print("El jugador",i,"juega el dia",d,"de",f,"a",ff,"como",t)

def get_solutions(model,dates_for,hours_exact,inv_var,data):
	positives = []
	for n in model:
		if n>0:
			(i,d,f,ff,t) = inv_var[n]
			dt = dates_for[d]
			t = hours_exact[f].time()
			combined = datetime.datetime.combine(dt, t)
			combined2 = combined + datetime.timedelta(hours=2)
			al = [data['participants'][i],combined,combined2,find_type(t)]
			positives.append(al)
	return positives

def get_events_list_from_solutions(positives):
	eventos=[]
	for p in positives:
		for x in positives:
			if p[1]==x[1] and p[2]==x[2]:
				nombre="Partido: "+p[0]+"("+p[3]+")"+" vs "+x[0]+"("+x[3]+")"
				horainicio = p[1]
				horafinal = p[2]
				eventos.append([nombre,horainicio,horafinal])
	return eventos


def create_calendar_file(name,eventos):
	c = Calendar()
	for evento in eventos:
		e = Event()
		e.name = evento[0]
		e.begin = evento[1]
		e.end = evento[2]
		c.events.add(e)

	with open(name, 'w') as my_file:
		my_file.writelines(c.serialize_iter())


def decode(name,calendar_name,inv_var,dates_for,hours_exact,data):
	model = get_model_from_file(name)
	sols = get_solutions(model,dates_for,hours_exact,inv_var,data)
	events = get_events_list_from_solutions(sols)
	create_calendar_file(calendar_name,events)

