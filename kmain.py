#!/usr/bin/python

from kmedoids import *



    
read_sequence_data('clusterdata.csv')

run_k_medoids(data,10)

print_clusters()
save_clusters()