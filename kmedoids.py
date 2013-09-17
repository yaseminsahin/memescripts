import env, os
import csv
from random import shuffle
import operator
from itertools import imap
from random import randint

global data, distance_matrix

data = []
distance_matrix = {}
medoids = []
clusters = []
total_cost = 0

class Cluster:
    def __init__(self):
        self.medoid = ""
        self.cost = 0
        self.items = []
    def get_distance(self, item):
        return distance_matrix[self.medoid][item]
    def add_item(self, item):
        d = self.get_distance(item)
        self.cost += d
        self.items.append(item)
    def remove_item(self,item):
        d = self.get_distance(item)
        self.cost -= d
        self.items.remove(item)
    def clear(self):
        del self.items[:]
        self.cost = 0
    def change_medoid(self):
        global distance_matrix
        print "current cost : %s (%s), checking for medoid update" % (self.medoid, self.cost)
        for x in self.items:
            curr_cost = 0
            for y in self.items:
                curr_cost += distance_matrix[x][y]
            print "------> new cost : %s (%s) " % (x,curr_cost)
            if curr_cost < self.cost:
                print "medoid changing: %s (%s) -> %s (%s)" % (self.medoid, self.cost, x, curr_cost)
                self.medoid = x
                self.cost = curr_cost
        

        
        
def run_k_medoids(data, k = 10):
    global clusters
    global medoids
    global total_cost    
    #step 1: initialization phase    
    calculate_distance_matrix()
    for m in initialize_medoids(k):
        medoids.append(m)
        c = Cluster()
        c.medoid = m
        clusters.append(c)
        
    cluster_items()
    total_cost = get_total_cost()
    print "initial cost: %s" % total_cost
    new_cost = 0
    while (total_cost != new_cost):
        total_cost = new_cost
        #step 2: update medoids
        for c in clusters:
            c.change_medoid()
        
        for c in clusters:
            c.clear()
            
        #step 3: cluster again
        cluster_items()
        new_cost = get_total_cost()
        print "new cost: %s" % new_cost
        
    
    
    
def cluster_items():
    global data
    global clusters

    for x in data:
        index = 0
        dx = 11 # our max distance is 10
        for i,c in enumerate(clusters):
            if c.get_distance(x) < dx:
                index = i
                dx = c.get_distance(x)
        #add item to the closest cluster
        clusters[index].add_item(x)

        
def get_total_cost():
    global clusters
    t_cost = 0
    for c in clusters:
        t_cost += c.cost
    return t_cost                
    

def print_clusters():
    global clusters
        
    for i,c in enumerate(clusters):
        print "%s. cluster:" % (i+1)
        print "\tmedoid: %s" % c.medoid
        print "\tcost  : %s" % c.cost
        print "\titems : %s" % len(c.items)
        for i in c.items:
            print "\t%s" % i
        print "\n--------------------------------------\n"

def save_clusters(filename = "clusters.out"):
    global clusters
    filename = os.path.abspath(os.path.join(env._env['DATA_PATH'] , filename) )
    outf = open(filename, 'w')
    for i,c in enumerate(clusters):
        outf.write( str(i+1) + ". cluster:\n")
        outf.write( "\tmedoid:" + c.medoid  + "\n")
        outf.write( "\tcost  : " + str(c.cost)  + "\n")
        outf.write( "\titems : " + str(len(c.items))  + "\n")
        for i in c.items:
            outf.write( "\t" + i + "\n")
        outf.write( "\n--------------------------------------\n")   
    outf.close()    
        
    

def calculate_distance_matrix():
    global distance_matrix
    other = data
    for x in data:
        distance_matrix[x] = {}
        for y in other:            
            distance_matrix[x][y] = hamming_distance(x,y)


def initialize_medoids(k):
    global distance_matrix
    v = {}
    for x in data:
        vx = 0
        for y in data:
            dxy = distance_matrix[x][y]
            dyall = sum(distance_matrix[y].values())
            vx += float(dxy)/dyall
        v[x] = vx
    
    sorted_v = sorted(v.iteritems(), key=lambda (k,v): (v,k))     
    return [el[0] for el in sorted_v[:k]]
    
    
            
    
#hamming distance, our sequence len is fixed and same for all
def hamming_distance(x, y):
   return sum(imap(operator.ne, x, y))   

def read_sequence_data(filename):
    print "-- Reading sequence data from: " + filename
    filename = os.path.abspath(os.path.join(env._env['DATA_PATH'] , filename) )
    with open(filename, 'r') as csvfile:
        seqreader = csv.reader(csvfile, delimiter=',', quotechar="\"")
        #header = seqreader.next()
#        if not data:
#            data.append(header[1])
        for row in seqreader:
            data.append(row[0])
    
# print current data you have        
def print_current_data():
    for d in data:
        print d


def delete_current_data():
    global data
    data = []

         

def shuffle_current_data():
    global data
    shuffle(data)


# get some part of data    
def slice_current_data(begin=None, end=None):
    global data
    if begin is None:
        if end is None:
            return data
        else:
            data = data[:end]
    elif end is None:
        data = data[begin:]
    else:
        data = data[begin:end]

            
    


        

    