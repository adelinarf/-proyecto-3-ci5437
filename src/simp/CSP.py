from library import *
import subprocess
import time

class CSP: 
    def __init__(self, variables, Domains,constraints): 
        self.variables = variables 
        self.domains = Domains 
        self.constraints = constraints 
        self.solution = None

    def solve(self): 
        assignment = {} 
        self.solution = self.backtrack(assignment) 
        return self.solution 

    def backtrack(self, assignment): 
        if len(assignment) == len(self.variables): 
            return assignment 
        var = self.select_unassigned_variable(assignment) 
        for value in self.order_domain_values(var, assignment): 
            if self.is_consistent(var, value, assignment): 
                assignment[var] = value 
                result = self.backtrack(assignment) 
                if result is not None: 
                    return result 
                del assignment[var] 
        return None

    def select_unassigned_variable(self, assignment): 
        unassigned_vars = [var for var in self.variables if var not in assignment]
        return min(unassigned_vars, key=lambda var: len(self.domains[var[0]])+len(self.domains[var[1]])) 

    def order_domain_values(self, var, assignment): 
        return self.domains[var[0]].intersection(self.domains[var[1]])

    def is_consistent(self, var, value, assignment): 
        for constraint_var in (self.constraints[var[0]] and self.constraints[var[1]]):
            if constraint_var in assignment and assignment[constraint_var] == value: 
                return False
        return True

data = open_file('file.json')
n,z,m = values(data)
hours_exact = get_hours_exact(data)
variables,inv_var=get_variables(n,z,m,types_,hours_exact)

def rival_exists(P,Q):
    (i,d,j,k,t) = inv_var[variables[P]]
    (i2,d2,j2,k2,t2) = inv_var[variables[Q]]
    return (i!=i2 and d==d2 and j==j2 and k==k2 and t!=t2)

def non_consecutive_days(P,Q):
    (i,d,j,k,t) = inv_var[variables[P]]
    (i2,d2,j2,k2,t2) = inv_var[variables[Q]]
    return (d!=d2 and (d2==d+1 or d2==d-1) and t==t2)

def once_per_day(P,Q):
    (i,d,j,k,t) = inv_var[variables[P]]
    (i2,d2,j2,k2,t2) = inv_var[variables[Q]]
    return (i==i2 and d==d2 and (j!=j2 and k!=k2) or (j==j2 and k==k2 and t!=t2))

def not_at_the_same_time(P,Q):
    (i,d,j,k,t) = inv_var[variables[P]]
    (i2,d2,j2,k2,t2) = inv_var[variables[Q]]
    not_overlap = j<k<j2<k2 or j2<k2<j<k
    return ((d==d2 and not_overlap) or (d!=d2))

def play_twice_with_everyone(P,Q,P2,Q2):
    (i,d,j,k,t) = inv_var[variables[P]]
    (i2,d2,j2,k2,t2) = inv_var[variables[Q]]

    (i3,d3,j3,k3,t3) = inv_var[variables[P2]]
    (i4,d4,j4,k4,t4) = inv_var[variables[Q2]]

    jugadores = (i==i3 and i2==i4 and d==d2 and d3==d4)
    fechas = (j==j2 and k==k2 and k3==k4)
    tipos = (t==t3 and t2==t4)
    return (jugadores and fechas and tipos)

def solution(variables):
    VARS=[]
    for key in variables:
        VARS.append(key)

    arcos = []
    for var in VARS:
        for var2 in VARS:
            if var!=var2:
                arcos.append(tuple([var,var2]))
    dominio={}
    for var in VARS:
        dominio[var] = {0,1}

    r1,r2,r3,r4,r5={},{},{},{},{}
    for x in VARS:
        r1[x],r2[x],r3[x],r4[x],r5[x] = [],[],[],[],[]
        for y in VARS:
            if x!=y and rival_exists(x,y):
                r1[x].append(tuple([x,y]))
            if x!=y and non_consecutive_days(x,y):
                r2[x].append(tuple([x,y]))
            if x!=y and once_per_day(x,y):
                r3[x].append(tuple([x,y]))
            if x!=y and not_at_the_same_time(x,y):
                r4[x].append(tuple([x,y]))
            if x!=y:
                for z in VARS:
                    for w in VARS:
                        if play_twice_with_everyone(x,y,z,w):
                            r5[x].append(tuple([x,y]))
                            r5[x].append(tuple([z,w]))

    csp = CSP(arcos, dominio, r1) 
    sol1 = csp.solve()
    sol2,sol3,sol4=[],[],[]
    csp2 = CSP(arcos, dominio, r2) 
    sol2 = csp2.solve()
    csp3 = CSP(arcos, dominio, r3) 
    sol3 = csp3.solve()
    csp4 = CSP(arcos, dominio, r4) 
    sol4 = csp4.solve()
    csp5 = CSP(arcos, dominio, r5) 
    sol5 = csp5.solve()
    return (sol1,sol2,sol3,sol4,sol5)

def get_clausules(variables):
    (sol1,sol2,sol3,sol4,sol5) = solution(variables)
    C=[]
    for x in sol1:
        first = variables[x[0]]
        second = variables[x[1]]
        C.append([-first,-second])
    for x in sol2:
        first = variables[x[0]]
        second = variables[x[1]]
        C.append([-first,second])

    for x in sol3:
        first = variables[x[0]]
        second = variables[x[1]]
        C.append([-first,second])

    for x in sol4:
        first = variables[x[0]]
        second = variables[x[1]]
        C.append([-first,second])
    for x in sol5:
        first = variables[x[0]]
        second = variables[x[1]]
        C.append([-first,-second])
    return C

start = time.time()
C = get_clausules(variables)

clausulas = clausula_multiple(C)

create_dimacs_file(clausulas,len(variables),"dimacs2.txt")

subprocess.run(["./glucose", 'dimacs2.txt','output.txt']) 
end = time.time()
print("The program ran",end-start,"seconds")