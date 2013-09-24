#!/usr/bin/python

from kmedoids import *



    
read_sequence_data('clusterdata.csv')

run_k_medoids(data,10)

read_classification_data('class_clust_results.csv')

print_clusters()
save_clusters()