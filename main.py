#!/usr/bin/python

from memescript import *

#custom_motifs = create_pairs(['A', 'C', 'G', 'T'], 2)
  
    
runmeme('brightness.fa')
motifs1 = parseresult()

runmeme('darkness.fa')
motifs2 = parseresult()

motifs3 = merge_motifs(motifs1, motifs2)

    
read_sequence_data('brightness.csv')
read_sequence_data('darkness.csv')
feature_vector_generator(motifs3) 
save_feature_vectors('combinedfeatures.csv') 


delete_current_data()
read_sequence_data('brightness.csv')
feature_vector_generator(motifs3) 
save_feature_vectors('brightfeatures.csv') 


delete_current_data()
read_sequence_data('darkness.csv')
feature_vector_generator(motifs3) 
save_feature_vectors('darkfeatures.csv')       



