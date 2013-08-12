import env, os
import csv
import shlex
from subprocess import Popen, PIPE
from random import shuffle
import re

global data, output

data = []
output = None

# converts csv file into fasta format
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
    
# run merci to collect motif data
def runmerci(positivefile, negativefile, topK=50, length=5, fp=20, fn=10, g=2, gl=2):
    global output    
   
    cmd = "perl " + env._env['MERCI_EXE_PATH'] + " "  
    cmd += "-p " +env._env['MERCI_DATA_PATH'] + "/{} ".format(positivefile)
    cmd += "-n " +env._env['MERCI_DATA_PATH'] + "/{} ".format(negativefile)
    cmd += "-k {} -l {} ".format(topK, length)
    cmd += "-fp {} -fn {} ".format(fp, fn)
    cmd += "-g {} -gl {} ".format(g, gl)
    cmd += "-c " + env._env['MERCI_CLASSIFICATION_PATH'] + " " 
    cmd += "-o " + env._env['MERCI_OUTPUT_PATH']
    
    print "-- Running command: "    
    print cmd    
    args = shlex.split(cmd)
    p = Popen(args, stdout=PIPE, stderr=PIPE)
    out, err = p.communicate()
    output = out
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


def match_motif_regex(string):
    return re.match(r"\s*\*\s+motif:\s+([AGTC\[\] p]+).*",string,re.IGNORECASE)

def match_motif_regex_header(string):
    return re.match(r"\s*(Motifs:)\s*",string,re.IGNORECASE)

def match_top_motif_regex(string):
    return re.match(r"\s*([AGTC\[\] p]+)\s*",string,re.IGNORECASE)
 
def match_gl_param_regex(string):
    return re.match(r"\s+-gl\s+(?P<param_gl>\d+)\s*", string, re.IGNORECASE)
# extract motif data from merci results    
def parseresult(result=None):
    global output
    if result is None:
        if output is None:
            raise Exception("You should run merci to get output data, then parse result")
        else:
            result = output
            
    lines = result.strip().split('\n') 
    motifs = []
    motif = None
    for line in lines:
        motif_regex_match = match_motif_regex(line)
        if not motif_regex_match:
            continue
        motif = Motif()
        motif.regex = motif_regex_match.group(1).replace(" ", "")
        motifs.append(motif)
        motif = None
    return motifs
    
# read output data from merci
def parseoutputfile():
    resultfile =  env._env['MERCI_OUTPUT_PATH']
    motifs = []
    motif = None
    state = 0;
    gl = 0;
    with open(resultfile, 'r') as f:
        for line in f:
            if state == 0:
                param_match = match_gl_param_regex(line)
                if not param_match:
                    continue
                gl = param_match.group('param_gl')
                state = 1
            if state == 1:
                motif_match = match_motif_regex_header(line)
                if not motif_match:
                    continue
                state = 2
            elif state == 2:
                motif_regex_match = match_top_motif_regex(line)
                if not motif_regex_match:
                    continue
                motif = Motif()
                motif.regex = ''
                motif.name = motif_regex_match.group(1).replace(" ", "")
                gaps = motif_regex_match.group(1).split()

                for ch in gaps:
                    if ch == 'gap':
                        motif.regex += "([AGTC]){0," + str(gl) + "}"
                    else:
                        motif.regex += ch
                
                motifs.append(motif)
                #print motif.name
                #print motif.regex
                motif = None
    return motifs 
    
    
    
def merge_motifs(motif1, motif2):
    return motif1 + motif2

def print_motifs(motifs):
    for m in motifs:
        print m.__str__()    
    
def match_motif_with_seq(motif_regex, sequence):
    motif_regex = ".*" + motif_regex + ".*"
    pattern = re.compile(motif_regex, re.IGNORECASE)
    return re.match(pattern, sequence)

def check_motif_in_seq_file(motif_regex, sequences):

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
    filename = os.path.abspath(os.path.join(env._env['MERCI_DATA_PATH'] , filename) )
    with open(filename, 'r') as csvfile:
        seqreader = csv.reader(csvfile, delimiter=',', quotechar="\"")
        header = seqreader.next()
        if not data:
            data.append(header)
        for row in seqreader:
            data.append(row)

# print current data you have        
def print_current_data():
    for d in data:
        print ",".join(d)


def delete_current_data():
    global data
    data = []

# deletes feature vectors from data
def reset_current_data():
    for row in data:
        del row[2:]
           

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

    
def feature_vector_generator(motifs):
    print "-- Generating features" 
    for m in motifs:
        data[0].append(m.name)
        check_motif_in_seq_file(m.regex,data)

def save_feature_vectors(filename = "features.csv" ):
    filename = os.path.abspath(os.path.join(env._env['MERCI_DATA_PATH'] , filename) )
    outf = open(filename, 'w')
    for row in data:
        outf.write( ",".join(row) + '\n')    
    outf.close()

            
    


        

    