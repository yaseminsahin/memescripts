import env, os
import csv
import shlex
from subprocess import Popen, PIPE
from random import shuffle
import re
import itertools

global data, memeoutput

data = []
memeoutput = None


def csvToFasta(infile, outfile):
    print "-- Extracting data from: " + infile
   
    infile = os.path.abspath(os.path.join(env._env['DATA_PATH'] , infile) )
    outfile = os.path.abspath(os.path.join(env._env['DATA_PATH'] , outfile) )
   
    outf = open(outfile, 'w')
    
    with open(infile, 'r') as csvfile:
        seqreader = csv.reader(csvfile, delimiter=',', quotechar="\"")
        seqreader.next()
        for row in seqreader:
            outf.write('>' + row[0] + '\n' + row[1] + '\n')
    
    outf.close()
    
    print "-- Fatsa file is created: " + outfile
    
# run meme to collect motif data
def runmeme(datafile, mod="zoops", minw=4, maxw=4, nmotifs=100, minsites=10, maxsites=100):
    global memeoutput    
    cmd = env._env['MEME_EXE_PATH'] + " " + env._env['DATA_PATH']    
    cmd += "/{} -text -mod {}".format(datafile, mod)
    cmd += " -minw {} -maxw {}".format(minw, maxw) 
    cmd += " -nmotifs {} -minsites {} -maxsites {} ".format(nmotifs, minsites, maxsites)     
    print "-- Running command: "    
    print cmd    
    args = shlex.split(cmd)
    p = Popen(args, stdout=PIPE, stderr=PIPE)
    out, err = p.communicate()
    memeoutput = out
    return out

   
class Motif:
    def __init__(self, name='', regex='', width=0, sites=0, llr=0, evalue=0 ):
        self.name = name
        self.regex = regex
        self.width = width
        self.sites = sites
        self.llr = llr
        self.evalue = evalue
    def __str__(self):
        return self.name + " : " + self.regex + " :w " + str(self.width) + " :s " + str(self.sites) + " :e " + str(self.evalue) + " :llr " + str(self.llr) 

def match_motif_properties(string):
    return re.match(r"(MOTIF\s+\d+)\s+width\s+=\s+(\d+)\s+sites\s+=\s+(\d+)\s+llr\s+=\s+(\d+)\s+E-value\s+=\s+(\d+\.\d+e\+\d+).*", string, re.IGNORECASE)

def match_motif_regex_header(string):
    return re.match(r"\s*(Motif\s+\d+)\s+regular\s+expression",string,re.IGNORECASE)

def match_motif_regex(string):
    return re.match(r"([AGTC\[\]]+)\s*",string,re.IGNORECASE)

# extract motif data from meme results    
def parseresult(result=None):
    if result is None:
        if memeoutput is None:
            raise Exception("You should run meme to get output data, then parse result")
        else:
            result = memeoutput
            
    lines = result.strip().split('\n')
    motifs = {}
    state = 0
    motif_name = ''
    for line in lines:
        if state == 0:
            motif_match = match_motif_properties(line)
            if not motif_match:
                continue
            motif_name = motif_match.group(1)
            motif = Motif(motif_name,'',motif_match.group(2),motif_match.group(3),motif_match.group(4), float(motif_match.group(5)) )
            motifs[motif_name] = motif
            state = 1
        elif state == 1:
            motif_regex_header = match_motif_regex_header(line)
            if not motif_regex_header:
                continue
            state = 2
        elif state == 2:
            motif_regex_match = match_motif_regex(line)
            if not motif_regex_match:
                continue
            motifs[motif_name].regex = motif_regex_match.group(1)
            motif_name = ''
            state = 0
            
    return motifs

def print_motifs(motifs):
    for m in motifs:
        print motifs[m].__str__()    
    
def match_motif_with_seq(motif_regex, sequence):
    motif_regex = ".*" + motif_regex + ".*"
    pattern = re.compile(motif_regex, re.IGNORECASE)
    return re.match(pattern, sequence)

def check_motif_in_seq_file(motif_regex, sequences):

    sequences[0].append(motif_regex)

    for row in sequences[1:]:
        regex_match = match_motif_with_seq(motif_regex,row[1])
        if regex_match:
            row.append("1")
        else:
            row.append("0")
            
    return sequences 

# read sequence file into memory to generate feature vectors
# if you do not delete current data, it appends each file to the end 
def read_sequence_data(filename):
    print "-- Reading sequence data from: " + filename
    filename = os.path.abspath(os.path.join(env._env['DATA_PATH'] , filename) )
    with open(filename, 'r') as csvfile:
        seqreader = csv.reader(csvfile, delimiter=',', quotechar="\"")
        for row in seqreader:
            data.append(row)

# print current data you have        
def print_current_data():
    for d in data:
        print ",".join(d)


def delete_current_data():
    global data
    data = []           

def shuffle_current_data():
    global data
    header = data[0]
    rows = data[1:]
    shuffle(rows)
    data = []
    data.append(header)
    data = data + rows

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

    
def feature_vector_generator(motifs, min_e_value = 0):
    print "-- Generating features"    
    for m in motifs:
        if (motifs[m].evalue >= min_e_value):
            check_motif_in_seq_file(motifs[m].regex,data)

def save_feature_vectors(filename = "features.csv" ):
    filename = os.path.abspath(os.path.join(env._env['DATA_PATH'] , filename) )
    outf = open(filename, 'w')
    for row in data:
        outf.write( ",".join(row) + '\n')    
    outf.close()

# create custom pairs from alphabet        
def create_pairs(alphabet, pair_size):
    custom_motifs = {} 
    for p in itertools.product(alphabet, repeat=pair_size):
        custom_regex = ''.join(p)
        custom_motifs[custom_regex] = Motif(custom_regex,custom_regex)
        
    return custom_motifs
            
    


        

    