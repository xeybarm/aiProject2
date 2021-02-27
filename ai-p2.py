from collections import deque

edges = []
assign = []
domain = []
adj = []
neighbours = 0

#finding minimum remaining value 
def heuristic_mrv(domain, assign):
    m = 10001 #minimum number
    for i in range(neighbours):
        if (len(domain[i]) < m and assign[i] != 1):
            m = len(domain[i])
            mrv = i
    return mrv

#finding least constraining value
def heuristic_lcv(node, edges, domain):
    lcv = []
    for i in domain[node]:
        m = 10001 #minimum number
        for j in edges[node]:
            if(len(domain[j]) < m):
                m = len(domain[j])
        lcv.append([i, m])
        color = [c[0] for c in lcv]    
    return color

#backtracking algorithm 
def csp(assign, edges, domain):
    
    if 'value' not in assign: #until all neighbours are checked
        return edges
    
    node = heuristic_mrv(domain, assign) #find next node with mrv
    colors = heuristic_lcv(node, edges, domain)  #find next color with lcv

    for color in colors:
        for k in [k for k in edges[node] if k in edges[node]]: #check if it is safe
            if color == edges[k]: #if not safe quit 
                return 0
            else: #if safe
                domain[node] = [i for i in domain[node] if i == color]
                
                for j in edges[node]:
                    if assign[j] != 1:
                        adj.append([j, node])

                q = deque(adj)
                while len(q) != 0:
                    p = q.popleft() #remove-first(queue)
                    if domain[p[1]][0] in domain[p[0]]:
                        domain[p[0]].remove(domain[p[1]][0])
                edges[node] = color
                assign[node] = 1
                answer = csp(assign, edges, domain)

                if answer != 0:
                    return answer
                return 0

#input text file
text = input("Enter name of the input file: (sample file names are numbers between 1 and 3): ") 

#reading txt file 
file = open(str(text) + '.txt', 'r') 
f = file.readlines()

for line in f:
    if not line.startswith("#"):  #neglect comments
        if line.startswith("c"): #find color line 
            n = int(line.split("=")[1]) #store the number of colors 
        else:
            if neighbours < int(line.split(',')[1]):
                neighbours = int(line.split(',')[1]) #store the value of maximum node  

for i in range(neighbours):
    assign.append('value') # create assignment array with dumb values
    edges.append([]) #create empty edges array 
    domain.append([]) #create empty domain array 
    
for line in f:
    if not line.startswith("#") and not line.startswith("c"):
       node1 = int(line.split(',')[0])-1 #find vertex1
       node2 = int(line.split(',')[1])-1 #find vertex2
       edges[node1].append(node2) #create neighbours
       edges[node2].append(node1) #create neighbours
    
for i in range(0, neighbours):
    for j in range(1, n + 1):
        domain[i].append(j) #create domain array

res = csp(assign, edges, domain)
    
if res == 0:
    print("No solution!")
else:
    for i in range(len(res)):
        print("vertex = " + str (i) + ", color = " + str(res[i]))
