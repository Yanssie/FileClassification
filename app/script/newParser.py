#!/usr/bin/python3
import xml.etree.ElementTree as ET
import json
#import Queue
import os
import queue
import sys

def add_attributes(children, souce_dict):
    for child in children:
        souce_dict[child.tag] = child.text

def add_nodes(group, souce_list, return_dict):
    for obj in souce_list:
        node = {}
        node["name"] = obj.get("{http://www.w3.org/ns/prov#}id")  # prov:id
        node["group"] = group
        children = obj.getchildren()
        if len(children) > 0:
            node["attributes"] = {}
            add_attributes(children, node["attributes"])
        return_dict["nodes"].append(node)

def add_links(group, source_list, return_dict):
    # 0: source, 1: target
    links_details = {"used": ["activity", "entity"],
                     "wasGeneratedBy": ["entity", "activity"],
                     "wasAssociatedWith": ["activity", "agent"],
                     "wasAttributedTo": ["entity", "agent"],
                     "actedOnBehalfOf": ["delegate", "responsible"],
                     "wasDerivedFrom": ["generatedEntity", "usedEntity"],
                     "specializationOf": ["specificEntity", "generalEntity"],
                     "alternateOf": ["alternate1", "alternate2"]}

    for obj in source_list:
        link = {}
        link["name"] = group
        link["weight"] = 1
        children = obj.getchildren()  # get source and target
        for child in children:
            node = child.tag[28:]
            if node in links_details[group]:
                node_index = links_details[group].index(node)
            else:
                node_index = -1  # some attributes

            if node_index == 0:  # add source
                link["source"] = child.get("{http://www.w3.org/ns/prov#}ref")
            elif node_index == 1:  # add target
                link["target"] = child.get("{http://www.w3.org/ns/prov#}ref")
            else:  # the attributes
                if link.get("attributes") is not None:
                    link["attributes"][child.tag] = child.text
                else:
                    link["attributes"] = {}
                    link["attributes"][child.tag] = child.text
        return_dict["links"].append(link)

def xml_to_dict(path):
    # read xml file and return a xml string
    xml_file = open(path, 'r')
    xml_string = xml_file.read()
    xml_file.close()

    # return object
    obj = {"nodes": [], "links": []}

    # xml tree
    tree = ET.fromstring(xml_string)
    entity_list = tree.findall('{http://www.w3.org/ns/prov#}entity')  # prov:entity
    activity_list = tree.findall('{http://www.w3.org/ns/prov#}activity')  # prov:activity
    agent_list = tree.findall('{http://www.w3.org/ns/prov#}agent')  # prov:agent

    # add entity nodes; entity:0
    add_nodes(0, entity_list, obj)
    # add activity nodes; activity: 1
    add_nodes(1, activity_list, obj)
    # add agent nodes; agent: 2
    add_nodes(2, agent_list, obj)

    used_list = tree.findall('{http://www.w3.org/ns/prov#}used')
    wasGeneratedBy_list = tree.findall('{http://www.w3.org/ns/prov#}wasGeneratedBy')
    wasAssociatedWith_list = tree.findall('{http://www.w3.org/ns/prov#}wasAssociatedWith')
    actedOnBehalfOf_list = tree.findall('{http://www.w3.org/ns/prov#}actedOnBehalfOf')
    wasDerivedFrom_list = tree.findall('{http://www.w3.org/ns/prov#}wasDerivedFrom')
    specializationOf_list = tree.findall('{http://www.w3.org/ns/prov#}specializationOf')
    alternateOf_list = tree.findall('{http://www.w3.org/ns/prov#}alternateOf')

    add_links("used", used_list, obj)
    add_links("wasGeneratedBy", wasGeneratedBy_list, obj)
    add_links("wasAssociatedWith", wasAssociatedWith_list, obj)
    add_links("actedOnBehalfOf", actedOnBehalfOf_list, obj)
    add_links("wasDerivedFrom", wasDerivedFrom_list, obj)
    add_links("specializationOf", specializationOf_list, obj)
    add_links("alternateOf", alternateOf_list, obj)
    
    return obj
    
def xml_to_json(path):
    obj = xml_to_dict(path)
    return json.dumps(obj, sort_keys=False, indent=4, separators=(',', ': '))

def json_to_file(json_string, file_name):
    # create a file to write
    json_file = open(file_name, "w")
    json_file.write(json_string)
    json_file.close()
    
    
#######################
## Functions above are compatible with Rebecca's parser.py
## Functions below are defined by Leshang
#######################

def extract_activity_from_schema(path):  
    xml_file = open(path, 'r')
    xml_string = xml_file.read()
    xml_file.close()
    obj = {}
    tree = ET.fromstring(xml_string)
    activity_list = tree.findall('{http://www.w3.org/ns/prov#}activity')  # prov:activity
    
    for activity in activity_list:
        node = {}
        node["name"] = activity.get("{http://www.w3.org/ns/prov#}id")  # prov:id
        node["group"] = 1
        children = activity.getchildren()
        if len(children) > 0:
            node["attributes"] = {}
            add_attributes(children, node["attributes"])
        obj[activity.get("{http://www.w3.org/ns/prov#}id")] = node
        
    return obj
    
def extract_activities(json_dict, schema_activity_dict = None):
    activity_dict = {"nodes": [], "links": []}
    used_dict = dict()
    gen_dict = dict()
    all_activity_set = set()
    sample_activity_set = set()
    
#    json_dict = {**json_dict, **schema_dict}
    

    for node in json_dict["nodes"]:
#        print(node)
        if(node["group"] == 1):
            activity_dict["nodes"].append(node)
            sample_activity_set.add(node["name"])
            
    for link in json_dict["links"]:
#        print(link)
        if(link["name"] == "used"):
#            print(link["source"])
            used_dict[link["source"]] = link["target"]
        elif(link["name"] == "wasGeneratedBy"):
            gen_dict[link["source"]] = link["target"]
        
    for used_key in used_dict:
        used_val = used_dict[used_key]
        if(used_val in gen_dict):
            edge = {}
            edge["source"] = used_key
            edge["target"] = gen_dict[used_val]
            edge["name"] = "linkto"
            edge["weight"] = 1
            activity_dict["links"].append(edge) ## add an edge
            all_activity_set.add(used_key)
            all_activity_set.add(gen_dict[used_val]) ## add all nodes needed to appear
    
    if(schema_activity_dict is not None):
        for node in all_activity_set:
            if(node not in sample_activity_set):
                if(node in schema_activity_dict):
                    activity_dict["nodes"].append(schema_activity_dict[node])
#                print(node)

#    print(activity_dict)
    return activity_dict

def combine_nodes_links_dict(dict_one, dict_two):
    all_dict = {"nodes": [], "links": []}
    all_dict["nodes"] = dict_one["nodes"] + dict_two["nodes"]
    all_dict["links"] = dict_one["links"] + dict_two["links"]
    
    return all_dict
    
def flatten_dict(org_dict):
    flat_dict = dict()
    for node in org_dict["nodes"]:
        sequence_node = {"nodes": [], "links": []}
        sequence_node["nodes"].append(node)
        flat_dict[node["name"]] = sequence_node
    for link in org_dict["links"]:
        (flat_dict[link["source"]])["links"].append(link)

    return flat_dict
    
## Getting all nodes with attributes and without link information:
def flatten_node_only_dict(org_dict):
    flat_dict = dict()
    for node in org_dict["nodes"]:
        sequence_node = {"nodes": [], "links": []}
        sequence_node["nodes"].append(node)
        flat_dict[node["name"]] = sequence_node
#    for link in org_dict["links"]:
#        (flat_dict[link["source"]])["links"].append(link)

    return flat_dict
    
def get_all_nodes(org_dict):
    ## get all nodes in whole dictionary
    nodes_set = set()
    for node in org_dict["nodes"]:
        nodes_set.add(node["name"])
    for link in org_dict["links"]:
#        print(link)
        nodes_set.add(link["source"])
        nodes_set.add(link["target"])
    
#    print (nodes_set)
    return nodes_set

def get_all_nodes_in_node_list(org_dict):
    ## get all nodes in node list of a dict
    nodes_set = set()
    for node in org_dict["nodes"]:
        nodes_set.add(node["name"])
    return nodes_set
    
def get_all_links_in_dict(org_dict):
    new_links = dict()
    ## TODO:
    for link in org_dict["links"]:
        new_links[link["source"]] = link["target"]
#        new_links[link["target"]] = link["source"]
    return new_links
    
def reorganize_samples(json_dict, sequencing_dict = None, schema_dict = None):
    complete_sample_dict = {"nodes": [], "links": []}
    all_activity_set = set()
    sample_activity_set = set()
#    all_nodes_set = set()
    
    sequencing_flat_dict = flatten_dict(sequencing_dict)
    all_nodes_in_sample_set = get_all_nodes(json_dict)
#    print(all_nodes_in_sample_set)
    
    complete_sample_dict = combine_nodes_links_dict(json_dict, complete_sample_dict)

#    if(schema_dict is not None):
#        json_dict = combine_nodes_links_dict(json_dict, schema_dict)  
    
#    print(complete_sample_dict)
    ## Add sequencingRun to related sample
    if(sequencing_flat_dict is not None):
        for node in all_nodes_in_sample_set:
#            print("node: ", node)
#             Assume the structure of sequencingRun
            if(node in sequencing_flat_dict):
                
                ## add the dict of each distinct sequencingRun to complete_sample_dict
                complete_sample_dict = combine_nodes_links_dict(complete_sample_dict, sequencing_flat_dict[node])
#                print("TESTING: ", sequencing_flat_dict[node])
    
#    print("TESTING SEQRUN: ", sequencing_flat_dict)
            
#    link_dict = get_all_links_in_dict(schema_dict)
#    print(complete_sample_dict)
    all_nodes_in_whole_set = get_all_nodes(complete_sample_dict)
    
    ## Adding nodes in schema into related sample
    schema_flat_node_dict = flatten_node_only_dict(schema_dict)
    if(schema_flat_node_dict is not None):
        for node in all_nodes_in_whole_set:
#            print("node: ", node)
            if(node in schema_flat_node_dict):
#                print("node: ", node)
                complete_sample_dict = combine_nodes_links_dict(complete_sample_dict, schema_flat_node_dict[node])
#    print(schema_flat_node_dict)
            
    
    
    
    
#    complete_sample_dict = combine_nodes_links_dict(complete_sample_dict, schema_dict)

#    all_nodes_in_seq_sample_set = get_all_nodes(complete_sample_dict)
#    all_nodes_in_node_list_set = get_all_nodes_in_node_list(complete_sample_dict)
    
#    for node in (all_nodes_in_seq_sample_set - all_nodes_in_node_list_set):
        ## all nodes without detailed info / only in links
        ## do bfs for them
            
    

#    print(complete_sample_dict)
    return complete_sample_dict

def dict_to_json(dict_obj):
    return json.dumps(dict_obj, sort_keys=False, indent=4, separators=(',', ': '))
    
    
def add_xml_to_dict(path, obj):
    # read xml file and return a xml string
    if(not isinstance(obj, dict)):
        print("Warning: obj is not a dictionary!")
        obj = {"nodes": [], "links": []}
        
    xml_file = open(path, 'r')
    xml_string = xml_file.read()
    xml_file.close()

    # return object
#    obj = {"nodes": [], "links": []}

    # xml tree
    tree = ET.fromstring(xml_string)
    entity_list = tree.findall('{http://www.w3.org/ns/prov#}entity')  # prov:entity
    activity_list = tree.findall('{http://www.w3.org/ns/prov#}activity')  # prov:activity
    agent_list = tree.findall('{http://www.w3.org/ns/prov#}agent')  # prov:agent

    # add entity nodes; entity:0
    add_nodes(0, entity_list, obj)
    # add activity nodes; activity: 1
    add_nodes(1, activity_list, obj)
    # add agent nodes; agent: 2
    add_nodes(2, agent_list, obj)

    used_list = tree.findall('{http://www.w3.org/ns/prov#}used')
    wasGeneratedBy_list = tree.findall('{http://www.w3.org/ns/prov#}wasGeneratedBy')
    wasAssociatedWith_list = tree.findall('{http://www.w3.org/ns/prov#}wasAssociatedWith')
    actedOnBehalfOf_list = tree.findall('{http://www.w3.org/ns/prov#}actedOnBehalfOf')
    wasDerivedFrom_list = tree.findall('{http://www.w3.org/ns/prov#}wasDerivedFrom')
    specializationOf_list = tree.findall('{http://www.w3.org/ns/prov#}specializationOf')
    alternateOf_list = tree.findall('{http://www.w3.org/ns/prov#}alternateOf')

    add_links("used", used_list, obj)
    add_links("wasGeneratedBy", wasGeneratedBy_list, obj)
    add_links("wasAssociatedWith", wasAssociatedWith_list, obj)
    add_links("actedOnBehalfOf", actedOnBehalfOf_list, obj)
    add_links("wasDerivedFrom", wasDerivedFrom_list, obj)
    add_links("specializationOf", specializationOf_list, obj)
    add_links("alternateOf", alternateOf_list, obj)
    
    return obj

# output = xml_to_json("release1.sequencingRuns.xml")
# print output
# json_to_file(output, "parsed.json")
# json_to_file(xml_to_json("typeFiles/Libraries.xml"), "libraries.json")
# json_to_file(xml_to_json("typeFiles/Pipeline.xml"), "pipeline.json")
# json_to_file(xml_to_json("typeFiles/PipelineBLAST.xml"), "pipelineBlast.json")
# json_to_file(xml_to_json("typeFiles/PipelineSTAR.xml"), "pipelineStar.json")
# json_to_file(xml_to_json("typeFiles/PipelineTRIM.xml"), "pipelineTrim.json")
# json_to_file(xml_to_json("typeFiles/PipelineVERSE.xml"), "pipelineVerse.json")
# json_to_file(xml_to_json("typeFiles/Sequencing.xml"), "sequencing.json")

#output = xml_to_json("../../split/release1.samples.xml-2.xml")
#schema_output = xml_to_json("../../library/release1.sequencingRuns.xml")

#json_to_file(output, "../../split/release1.samples.xml-2.all.json")
#print ("[output] " + output)
#print ("[schema_output] " + schema_output)
#act_dict = extract_activities(xml_to_dict("updated/split/release1.samples.xml-1.xml"), 
#                              extract_activity_from_schema("updated/release1.sequencingRuns.xml"))
#print(dict_to_json(act_dict))


librarydir = sys.argv[1]

schema1 = extract_activity_from_schema(librarydir + "/release1.sequencingRuns.xml")
schema2 = extract_activity_from_schema(librarydir + "/release2.sequencingRuns.xml")
schema3 = extract_activity_from_schema(librarydir + "/release3.sequencingRuns.xml")
all_schema = {**schema1, **schema2, **schema3}

totalSchema = {"nodes": [], "links": []}
totalSchema = add_xml_to_dict(librarydir + "/Pipeline.xml", totalSchema)
totalSchema = add_xml_to_dict(librarydir + "/Libraries.xml", totalSchema)
totalSchema = add_xml_to_dict(librarydir + "/Sequencing.xml", totalSchema)
totalSchema = add_xml_to_dict(librarydir + "/Pipeline BLAST.xml", totalSchema)
totalSchema = add_xml_to_dict(librarydir + "/Pipeline TRIM.xml", totalSchema)
totalSchema = add_xml_to_dict(librarydir + "/Pipeline VERSE.xml", totalSchema)
totalSchema = add_xml_to_dict(librarydir + "/Pipeline STAR.xml", totalSchema)
totalSchema = add_xml_to_dict(librarydir + "/Pipeline HTSeq.xml", totalSchema)

totalSequence = {"nodes": [], "links": []}
totalSequence = add_xml_to_dict(librarydir + "/release1.sequencingRuns.xml", totalSequence)
totalSequence = add_xml_to_dict(librarydir + "/release2.sequencingRuns.xml", totalSequence)
totalSequence = add_xml_to_dict(librarydir + "/release3.sequencingRuns.xml", totalSequence)
totalSequence = add_xml_to_dict(librarydir + "/pipeline12a.sequencingRuns.xml", totalSequence)

#json_to_file(dict_to_json(totalSchema), "../../output/totalSchema.json")

#json_to_file(dict_to_json(flatten_dict(totalSequence)), "../../output/flatSequences.json")

#splittedSample = xml_to_dict("../../split/release1.samples.xml-1.xml")
#reorganizedSamples = reorganize_samples(splittedSample, totalSequence, totalSchema)
#json_to_file(dict_to_json(reorganizedSamples), "../../output/release1.samples.xml-1.reorganized.json")
#samples1 = add_xml_to_dict("updated/split/release1.samples.xml-1.xml", None)
#test_dict = extract_activities(samples1)

#json_to_file((dict_to_json(test_dict)), "updated/split/release1.samples.xml-1-mod.json")
upload_dir = sys.argv[2]
for parent,dirnames,filenames in os.walk(upload_dir):  
#    print(filenames)
    for filename in filenames:
        if(filename.split('.').pop() == "xml"):
            if (sys.argv[3] in filename):
                act_dict = extract_activities(xml_to_dict(upload_dir + "/" +filename), all_schema)
        #        print(dict_to_json(act_dict))
                json_to_file(dict_to_json(act_dict), upload_dir + "/" + filename + ".json")
#print (output)
#json_to_file(output, "fake.json")
