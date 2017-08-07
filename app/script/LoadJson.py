# -*- coding: utf-8 -*-
"""
Created on Thu Mar 16 13:21:27 2017

@author: Leshang

This script generates features and do ML algorithm
"""
import json
import os
import pandas as pd
import numpy as np
from sklearn import tree
#from sklearn.datasets import load_iris
#from sklearn.cross_validation import KFold
from sklearn.model_selection import KFold
from sklearn import metrics
from sklearn.cluster import KMeans
#from kmodes import kmodes
import matplotlib.pyplot as plt
import pandas as pd
import sys
#import newParser
import warnings

def fxn():
    warnings.warn("deprecated", DeprecationWarning)

with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    fxn()

def read_json_file(filename):
    json_file = open(filename, "r")
    json_str = json_file.read()
    return json_str
    
def json_to_dict(json_string):
    json_dict = json.loads(json_string)
    return json_dict
    
def get_namespace():
    ns_dict = { 'xsi': "http://www.w3.org/2001/XMLSchema-instance", 
        'xsd': "http://www.w3.org/2001/XMLSchema", 
        'prov': "http://www.w3.org/ns/prov#", 
        'foaf': "http://xmlns.com/foaf/0.1/", 
        'pp': "http://www.pennprovenance.net/provDefs/", 
        'kimlab': "http://kim.bio.upenn.edu/provDefs/", 
        'kimlab-sequencing': "http://kim.bio.upenn.edu/provDefs/sequencing#", 
        'kimlab-sample': "http://kim.bio.upenn.edu/provDefs/sample#", 
        'kimlab-star': "http://kim.bio.upenn.edu/provDefs/star#", 
        'kimlab-htseq': "http://kim.bio.upenn.edu/provDefs/htseq#", 
        'kimlab-blast': "http://kim.bio.upenn.edu/provDefs/blast#", 
        'kimlab-trim': "http://kim.bio.upenn.edu/provDefs/trim#"
    }

    return ns_dict
    
def get_lexicon():
    lexicon_dict = dict()
    attrib_list = ['{http://kim.bio.upenn.edu/provDefs/trim#}minimum-length', 
                   '{http://kim.bio.upenn.edu/provDefs/trim#}phred-threshold',
                   '{http://kim.bio.upenn.edu/provDefs/trim#}number-AT',
                   '{http://kim.bio.upenn.edu/provDefs/trim#}contaminants-file',#string
                   '{http://kim.bio.upenn.edu/provDefs/verse#}is-stranded',
                   '{http://kim.bio.upenn.edu/provDefs/verse#}include-introns',
                   '{http://kim.bio.upenn.edu/provDefs/verse#}include-intergenic',
                   '{http://kim.bio.upenn.edu/provDefs/verse#}include-lines-sines',
                   '{http://kim.bio.upenn.edu/provDefs/blast#}kmer'#,
#                   '',
#                   '',
#                   '',
#                   ''
                   ]
    count = 0
    for attrib in attrib_list:
        lexicon_dict[count] = attrib
        count += 1
    return lexicon_dict
    
def get_node_attrib_dict(json_dict):
    attrib_dict = dict()
    for node in json_dict['nodes']:
        attrib_dict = { **attrib_dict, ** node['attributes']}
    return attrib_dict
    
def get_attrib_vector(attrib_dict, lexicon_dict):
    cat_to_int_dict = {
        '/lab/repo/resources/trim/contaminants.fa' : 11,
        'TATAGTGAGT': 21,
        '/home/jshall/lab/repo/resources/trim/contaminants.fa' : 12
    }
    lexicon_size = len(lexicon_dict)
    total_vector = list()
#    print(attrib_dict)
    for index in lexicon_dict:
#        print("lexicon: ", lexicon_dict[index])
        if lexicon_dict[index] in attrib_dict:
            val = attrib_dict[lexicon_dict[index]]
            if(val is not None):
#                total_vector.append(val)
                if(str_is_number(val)):
                    total_vector.append(int(val))
                else:
#                    total_vector.append(val)
                    val_to_int = cat_to_int_dict[val]
                    if(val_to_int is None):
                        val_to_int = 1
                    total_vector.append(val_to_int)
            else:
                total_vector.append(0)
        else:
            total_vector.append(-1)
    
    return total_vector

def get_connectivity_matrix(json_dict, nodes_lexicon_dict, nodes_inv_lexicon_dict):
    lexicon_size = len(nodes_lexicon_dict)
    link_dict = dict()
    link_source_list = []
    link_target_list = []
    for link in json_dict['links']:
        source = link['source']
        target = link['target']
        if(source not in nodes_inv_lexicon_dict):
            nodes_lexicon_dict[lexicon_size] = source
            nodes_inv_lexicon_dict[source] = lexicon_size
            source_id = lexicon_size
            lexicon_size += 1
        else:
            source_id = nodes_inv_lexicon_dict[source]
        if(target not in nodes_inv_lexicon_dict):
            nodes_lexicon_dict[lexicon_size] = target
            nodes_inv_lexicon_dict[target] = lexicon_size
            target_id = lexicon_size
            lexicon_size += 1
        else:
            target_id = nodes_inv_lexicon_dict[target]
#        print(source_id, " ", target_id)
#        link_dict[source_id] = target_id
#        link_dict[target_id] = source_id
        link_source_list.append(source_id)
        link_target_list.append(target_id)
#        link_source_list.append(target_id)
#        link_target_list.append(source_id)
#        print(link_dict)
    
    node_num_max = len(link_source_list)
#    print(link_dict)
    connectivity_matrix = np.zeros((lexicon_size, lexicon_size))
    for index in range(node_num_max):
        connectivity_matrix[link_source_list[index], link_target_list[index]] = 1
        connectivity_matrix[link_target_list[index], link_source_list[index]] = 1
    return connectivity_matrix
    
#def test_json_to_vector:
    
def str_is_number(str):
    try:
        int(str)
        return True
    except Exception:
        return False
    
def matchCluster(result_df):
    val1_df = result_df[[0]].drop_duplicates()
    val2_df = result_df[[1]].drop_duplicates()
#    result_df['y'].merge(val1_df, )
#    result_df[[0]].groupby(['y'])
    accu_array = np.zeros((len(result_df[[0]].drop_duplicates()) * len(result_df[[1]].drop_duplicates()), 3))
    row_num = 0
    for left_label in result_df['y'].drop_duplicates().tolist():
        for right_label in result_df['y_pred'].drop_duplicates().tolist():
#            print(left_label, 
#                  right_label,
#                  len(result_df[(result_df['y'] == left_label) & (result_df['y_pred'] == right_label)])
#                  /len(result_df[(result_df['y'] == left_label)]))
            accu_array[row_num, 0] = left_label
            accu_array[row_num, 1] = right_label
            accu_array[row_num, 2] = len(result_df[(result_df['y'] == left_label) & (result_df['y_pred'] == right_label)])\
                  /len(result_df[(result_df['y'] == left_label)])
            row_num += 1
    
#    print(np.argmax(accu_array, axis = 1))
    accu_df = pd.DataFrame(accu_array, columns=['num1','num2', 'accu'])
    match_df = (accu_df.groupby(['num1', 'num2']).max())#[['num1', 'num2']]
    print(match_df)
    
#    return match_df

if __name__ == '__main__':
    print()
#==============================================================================
# #    print(json_to_dict(read_json_file('updated/split/release1.samples.xml-1.xml.json')))
#     sample_dict_12a = json_to_dict(read_json_file('updated/split/pipeline12a.samples.xml-1.xml.json'))
#     sample_vector_12a = get_attrib_vector(get_node_attrib_dict(sample_dict_12a), 
#                                       get_lexicon())
#                                       
#     sample_dict_2 = json_to_dict(read_json_file('updated/split/release2.samples.xml-1.xml.json'))
#     sample_vector_2 = get_attrib_vector(get_node_attrib_dict(sample_dict_2), 
#                                       get_lexicon())
#                                       
#     sample_dict_3 = json_to_dict(read_json_file('updated/split/release3.samples.xml-1.xml.json'))
#     sample_vector_3 = get_attrib_vector(get_node_attrib_dict(sample_dict_3), 
#                                       get_lexicon())                                     
#     print(get_lexicon())
#     print (sample_vector_12a)
#     print (sample_vector_2)
#     print (sample_vector_3)
#     
#     nodes_lexicon_dict_12a = dict()
#     nodes_inv_lexicon_dict_12a = dict()
#     conn_mat_12a = get_connectivity_matrix(sample_dict_12a, nodes_lexicon_dict_12a, nodes_inv_lexicon_dict_12a)
# #    print(nodes_lexicon_dict_12a)
# #    print(conn_mat_12a)
#     conn_mat_2 = get_connectivity_matrix(sample_dict_12a, nodes_lexicon_dict_12a, nodes_inv_lexicon_dict_12a)
# 
#==============================================================================
    
#    print(np.linalg.eig(conn_mat_12a))
#    print(np.linalg.eig(conn_mat_2))
#    rootdir = "../uploads"
    rootdir = sys.argv[1]
    samples_list = []
    feature_names = []
    for parent,dirnames,filenames in os.walk(rootdir):  
        for filename in filenames:
#            temp_sample_vector = []
            if((filename.split('.').pop() == "json")):
#            & (filename.split('.')[0] == "pipeline12a")):#pipeline12a
                temp_sample_dict = json_to_dict(read_json_file(rootdir+'/'+filename))
                temp_sample_vector = get_attrib_vector(get_node_attrib_dict(temp_sample_dict), 
                                      get_lexicon())
                
                temp_sample_vector.append(1)
#                print(temp_sample_vector)
                samples_list.append(temp_sample_vector)
                feature_names.append(filename)
                
                
            elif((filename.split('.').pop() == "json") 
            & (filename.split('.')[0] == "release2")):#pipeline12a
#                print(filename)
                temp_sample_dict = json_to_dict(read_json_file(rootdir+'/'+filename))
                temp_sample_vector = get_attrib_vector(get_node_attrib_dict(temp_sample_dict), 
                                      get_lexicon())
                
                temp_sample_vector.append(2)
#                print(temp_sample_vector)
                samples_list.append(temp_sample_vector)
                feature_names.append(filename)
#                
            elif((filename.split('.').pop() == "json") 
            & (filename.split('.')[0] == "release3")):#pipeline12a
#                print(filename)
                temp_sample_dict = json_to_dict(read_json_file(rootdir+'/'+filename))
                temp_sample_vector = get_attrib_vector(get_node_attrib_dict(temp_sample_dict), 
                                      get_lexicon())
                
                temp_sample_vector.append(3)
#                print(temp_sample_vector)
                samples_list.append(temp_sample_vector)
                feature_names.append(filename)
    
    sample_data = np.array(samples_list)
    print(feature_names)
    print(samples_list)
#    print(sample_data)
    x_num, y_num = sample_data.shape
       
    X=sample_data[:,0:-1]
    y = sample_data[:,-1]
#       
#    kf = KFold(x_num, n_folds=10, shuffle=True)
    kf = KFold(10, shuffle=True)
#    print(kf)
#    kf.get_n_splits(X)
    i = 0
    for train_index, test_index in kf.split(X):
   #        print("TRAIN:", train_index, "TEST:", test_index)
           X_train, X_test = X[train_index], X[test_index]
           y_train, y_test = y[train_index], y[test_index]
   #        if (i == 2):
           dt = tree.DecisionTreeClassifier(max_depth=2)
           dt.fit(X_train, y_train)
           
           y_pred = dt.predict(X_test)
   #        print(metrics.accuracy_score(y_test, y_pred))
           
   #        kmeans = KMeans(n_clusters = 4, random_state=0).fit(X_train)
   #        y_pred = kmeans.predict(X_test)
#           print(metrics.accuracy_score(y_test, y_pred))
           i += 1
#           
    accuracy_list = []
    param_list = range(1, 6)
    for cluster_num in param_list: 
           fold_accu = []
           i = 0
           for train_index, test_index in kf.split(X):
       #        print("TRAIN:", train_index, "TEST:", test_index)
               X_train, X_test = X[train_index], X[test_index]
               y_train, y_test = y[train_index], y[test_index]
      
               km = KMeans(n_clusters = cluster_num, init='k-means++').fit(X)
               y_pred = km.predict(X_test)
               
               X_transform = km.transform(X_test)
               
   #            print(y_test)
   #            print(y_pred)
   #            print("score: ", km.score(X_test))
   #            print("distortion: ",km.inertia_)
   #            km = kmodes.KModes(n_clusters = cluster_num, init = 'Huang', n_init = 5, verbose = 1)
   #            km.fit_predict(X)
   #            y_pred = km.predict(X_test)
               this_accuracy = km.score(X_test)
   #            this_accuracy = km.inertia_
               
               fold_accu.append(this_accuracy)
               i += 1
#           print(cluster_num, np.mean(fold_accu))
           accuracy_list.append(np.mean(fold_accu))
#           
#    print(accuracy_list)
    plt.figure(1)
    plt.plot(param_list, accuracy_list)     
       
    plt.savefig('cluster-accu.png')
           
    km = KMeans(n_clusters = 3, init='k-means++').fit(X)
    y_pred = km.predict(X)
    print(*y_pred)
       
    org_df = pd.DataFrame(y, columns=['y'])
    pred_df = pd.DataFrame(y_pred, columns=['y_pred'])
    result_df = pd.concat([org_df, pred_df], axis=1)
       
   #    matchCluster(result_df)
   
    accu_array = np.zeros((len(result_df['y'].drop_duplicates()) * len(result_df['y_pred'].drop_duplicates()), 3))
    row_num = 0
    for left_label in result_df['y'].drop_duplicates().tolist():
           for right_label in result_df['y_pred'].drop_duplicates().tolist():
   #            print(left_label, 
   #                  right_label,
   #                  len(result_df[(result_df['y'] == left_label) & (result_df['y_pred'] == right_label)])
   #                  /len(result_df[(result_df['y'] == left_label)]))
               accu_array[row_num, 0] = left_label
               accu_array[row_num, 1] = right_label
               accu_array[row_num, 2] = len(result_df[(result_df['y'] == left_label) & (result_df['y_pred'] == right_label)])\
                     /len(result_df[(result_df['y'] == left_label)])
               row_num += 1
       
   #    print(np.argmax(accu_array, axis = 1))
    accu_df = pd.DataFrame(accu_array, columns=['num1','num2', 'accu'])
    match_df = accu_df.loc[accu_df.groupby(['num1'])['accu'].idxmax()]#[['num1', 'num2']]
    print(match_df)
       
    match_accu = len(result_df.merge(match_df, left_on=['y','y_pred'], right_on = ['num1','num2'], how='inner'))\
                        /len(result_df)
    print(match_accu)
       
       
   #    print(y)
   #    print(y_pred)
   #    for pos in range(len(y)):
   #        print(y[pos], ",", y_pred[pos])
   #        print(np.array(samples_list))




