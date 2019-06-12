import sys, queue

# for data graph (G)
global vnum_G               # number of vertices in G
global list_G               # adjacent list representing G
global label_G              # list of labels (renamed version) of vertices in G
global label_freq_G         # list of frequency of each label (renamed version) in G
global degree_G             # list of degrees of vertices in G
global renamedlabel_G       # mapping function for renaming label name in G
global sorted_v             # sorted version of V(G) : sort by label first, and within the same label sort by degree
global sorted_v_index       # sorted_v_index[l] : first index (in sorted_v array) of vertice among the vertices with label l

# for query graph (q)
global vnum_q               # k-th element : the number of vertices in k-th query graph
global list_q               # k-th element : adjacent list representing k-th query graph
global label_q              # k-th element : list of labels of vertices in k-th query graph
global label_freq_q         # k-th element : list of frequency of each label in k-th query graph'
global degree_q             # k-th element : list of degrees of vertices in k-th query graph
global renamedlabel_q       # k-th element : list of degrees of vertices in k-th query graph'
global num_q                # total number of query graphs
global visited              # visit flag for BFS
global list_dag             # data structure for constructing query DAG while executing BFS

def read_G(input_G) :
    global vnum_G, list_G, label_G, label_freq_G, degree_G, renamedlabel_G, sorted_v, sorted_v_index

    # read input_G file
    with open(input_G, 'r') as f :
        largest_label = -1
        label_set = set()
        input_line = ""

        # read "t 1 [#v]"
        vnum_G = int(f.readline().split()[2])   # number of vertices in G
        list_G = [[] for _ in range(vnum_G)]    # adjacent list representing the data graph
        label_G = [-1 for _ in range(vnum_G)]   # list of labels of vertices in G
        degree_G = [0 for _ in range(vnum_G)]   # list of degrees of vertices in G

        # read every "v [v_id] [label]"
        for i in range(vnum_G) :
            label = int(f.readline().split()[2])
            label_set.add(label)
            if (label > largest_label) :
                largest_label = label
        label_num = len(label_set)

        # read every "e [src] [des] [label]"
        while (True) :
            line_e = f.readline()
            if (not line_e) :
                break
            info_e = line_e.split()
            src = int(info_e[1])
            des = int(info_e[2])
            list_G[src].append(des)
            list_G[des].append(src)
            degree_G[src] = degree_G[src] + 1
            degree_G[des] = degree_G[des] + 1

    # second read (rename label, set label for each vertex, set frequency for each label)
    with open(input_G, 'r') as f :
        renamedlabel_G = [-1 for _ in range(largest_label + 1)]
        label_freq_G = [0 for _ in range(label_num)]
        label_id = 0

        f.readline() # ignore the first line
        for i in range(vnum_G) :
            label = int(f.readline().split()[2])
            try :
                if (renamedlabel_G[label] == -1) :
                    renamedlabel_G[label] = label_id
                    label_id = label_id + 1
            except :
                print(label, len(renamedlabel_G))
            label_G[i] = renamedlabel_G[label]
            label_freq_G[renamedlabel_G[label]] = label_freq_G[renamedlabel_G[label]] + 1

    sorted_v = [i for i in range(vnum_G)]
    sorted_v_index = [-1 for _ in range(label_num + 1)]

    sorted_v.sort(key = lambda v:degree_G[v])
    sorted_v.sort(key = lambda v:label_G[v])

    sorted_v_index[label_G[sorted_v[0]]] = 0
    for i in range(1, vnum_G) :
        if (label_G[sorted_v[i-1]] != label_G[sorted_v[i]]) :
            sorted_v_index[label_G[sorted_v[i]]] = i
    sorted_v_index[label_num] = vnum_G

def read_q(input_q, n) :
    global renamedlabel_G, vnum_q, list_q, label_q, degree_q, num_q
    vnum_q = []
    list_q = []
    label_q = []
    degree_q = []
    num_q = n

    # read input_q file
    with open(input_q, 'r') as f :

        # for each query graph (start from reading "t [id] [#v] [#e]")
        for k in range(num_q) :
            vnum_q.append(int(f.readline().split()[2]))
            list_q.append([[] for _ in range(vnum_q[k])])
            label_q.append([-1 for _ in range(vnum_q[k])])
            degree_q.append([0 for _ in range(vnum_q[k])])

            # read every "[v_id] [label] [degree] [des 1] [des 2] . . . [des n]"
            for i in range(vnum_q[k]) :
                line = f.readline()
                info = line.split()
                try :
                    label_q[k][i] = renamedlabel_G[int(info[1])]
                except :
                    print(len(renamedlabel_G))
                    exit(0)
                degree_q[k][i] = int(info[2])
                for j in range(degree_q[k][i]) :
                    des = int(info[j+3])
                    list_q[k][i].append(des)

def select_root(k) :
    global vnum_q, label_q, degree_q, sorted_v, sorted_v_index
    root = -1
    min = float('inf')

    for u in range(vnum_q[k]) :
        label = label_q[k][u]
        degree = degree_q[k][u]
        left = sorted_v_index[label]
        right = sorted_v_index[label + 1]
        new_left = find_new_left(left, right - 1, degree)
        size_C = right - new_left

        rank = size_C/(float(degree))
        if (rank < min) :
            min = rank
            root = u
    return root

def find_new_left(left, right, degree_u) :
    global degree_G, sorted_v
    i = left
    j = right
    while (i < j) :
        mid = i + (j - i) // 2
        if (degree_G[sorted_v[mid]] < degree_u) :
            i = mid + 1
        else :
            j = mid
    return i

def BFS(r, k) :
    global visited, vnum_q, list_q, list_dag, degree_q
    q = queue.Queue()
    visited = [False for _ in range(vnum_q[k])]
    visited[r] = True
    list_dag = [[] for _ in range(vnum_q[k])]
    level = [0 for _ in range(vnum_q[k])]
    level[r] = 0
    q.put(r)

    i = 1
    while (q.qsize() != 0) :
        u = q.get()
        print(u, end=" ")
        for v in list_q[k][u] :
            if (not visited[v]) :
                visited[v] = True
                q.put(v)
                list_dag[u].append(v)
                level[v] = i
            elif (level[u] == level[v]) :
                if (label_freq_G[u] < label_freq_G[v]) :
                    list_dag[u].append(v)
                elif (label_freq_G[u] > label_freq_G[v]) :
                    list_dag[v].append(u)
                else :
                    if (degree_q[k][u] >= degree_q[k][v]) :
                        list_dag[u].append(v)
                    else :
                        list_dag[v].append(u)
        i = i + 1
    print()

if __name__=="__main__":
    ### sys.argv[1] : name of data graph file
    ### sys.argv[2] : name of query graph file
    ### sys.argv[3] : the number of query in query graph file
    read_G(sys.argv[1])                     # read the data graph file
    read_q(sys.argv[2], int(sys.argv[3]))   # read the query graph file
    # print the dag for each query file
    for k in range(num_q) :
        root = select_root(k)
        BFS(root, k)
