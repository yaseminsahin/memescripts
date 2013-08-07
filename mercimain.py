#!/usr/bin/python

from merciscript import *


runmerci('brightness.fa', 'darkness.fa')
motifs1  = parseoutputfile()

runmerci('darkness.fa', 'brightness.fa')
motifs2  = parseoutputfile()

motifs3 = merge_motifs(motifs1, motifs2)
    
read_sequence_data('brightness.csv')
read_sequence_data('darkness.csv')
feature_vector_generator(motifs3) 
save_feature_vectors('combinedfeatures.csv') 



