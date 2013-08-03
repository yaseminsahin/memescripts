#!/usr/bin/python

from memescript import *

custom_motifs = create_pairs(['A', 'C', 'G', 'T'], 2)
  
    
runmeme('brightness.fa')
motifs = parseresult()

#print_motifs(motifs)
    
read_sequence_data('brightness.csv')
#pread_sequence_data('darkness.csv')

feature_vector_generator(custom_motifs) 

save_feature_vectors()     



