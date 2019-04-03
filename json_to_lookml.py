# Let users know if they're missing any of our hard dependencies
hard_dependencies = ("yaml", "git", "pandas","json","csv","os")
missing_dependencies = []

for dependency in hard_dependencies:
    try:
        __import__(dependency)
    except ImportError as e:
        missing_dependencies.append(dependency)

if missing_dependencies:
    raise ImportError(
        "Missing required dependencies {0}".format(missing_dependencies))
del hard_dependencies, dependency, missing_dependencies



import yaml
from lookerapi import LookerApi
import git
import pandas as pd
import json
import csv
import os



#clones github repository to 'cloned_looker_git_repo' in the working directory
def pull_github_repo(project_name,access_token):
    project = looker.get_project(project_name)
    https_remote_url = 'https://%s:x-oauth-basic%s' % (access_token, project['git_remote_url'][3:])
    
    repo_dir = os.path.join(os.getcwd(), 'cloned_looker_git_repo')
    if os.path.exists(repo_dir):
        repo = git.Repo(repo_dir)
    else:
        repo = git.Repo.clone_from(https_remote_url,repo_dir)
    o = repo.remotes.origin
    o.pull()
    return repo


#connects to Looker instance using the authentication in the config.yml file, in the specified path
def connect_looker(config_path):
    global looker 
    
    #get credentials
    f = open(config_path)
    params = yaml.load(f)
    host = 'localhost'
    f.close()
    my_host = params['hosts'][host]['host']
    my_secret = params['hosts'][host]['secret']
    my_token = params['hosts'][host]['token']
    
    #connect to Looker
    looker = LookerApi(host=my_host,
    token=my_token,
    secret = my_secret)
    
    return 



#detects columns with JSON objects
def find_json_cols(query_result):
    key_list = []
    for i in range(len(query_result)):
        for key,value in zip(query_result[i].keys(),query_result[i].values()):
            try:
                json.loads(value)
                key_list.append(key)
            except:
                None
    return list(set(key_list))


#gets data type of the dimension
def get_data_type(value):
    try:
        int(value)
        return 'number','INTEGER'
    except:
        try:
            float(value)
            return 'number','DECIMAL'
        except:
            try:
                pd.Timestamp(value)
                return 'time', 'TIMESTAMP'
            except:
                try:
                    value.keys()
                    return 'dictionary','VARCHAR()'
                except:
                    if value == 'True' or value == 'False':
                        return 'yesno', 'BOOLEAN'
            #         elif '[' and ']' in value:
            #             return 'list',  'VARIANT'
                    else:
                        return 'string','VARCHAR()'



#converts dictionary of dimension values into list of dictionaries with LookML metadata (name, type, sql)
def convert_lookml(dictionary,is_json = False, json_column_name = None):
    ##enter in the type logic
    dictionary_list = []
    for idx,key in enumerate(dictionary.keys()):
        definition_dictionary = {}
        definition_dictionary['name'] = key
        data_type,sql_data_type = get_data_type(dictionary[key])
        if data_type == 'dictionary':
            dictionary_list = dictionary_list + convert_lookml(dictionary[key],key)
            data_type = 'string'
        definition_dictionary['type'] = data_type
        if is_json is True:
            definition_dictionary['sql'] = '${%s}:%s::%s' %(json_column_name, key, sql_data_type)
        else:
            definition_dictionary['sql'] = '${TABLE}.%s' %key 
        dictionary_list.append(definition_dictionary)
    return dictionary_list


#formats LookML text appropriately from metadata
def format_lookml(name_dictionary):
    if name_dictionary['type'] == 'time':
        return '\tdimension_group: %s {\n \ttype: %s\n\tsql: %s;;\n\ttimeframes: [raw,date,week,month] \n\t}' %(name_dictionary['name'],name_dictionary['type'],name_dictionary['sql'])
    else:
        return '\tdimension: %s { \n\ttype: %s \n\t sql: %s;; \n\t}' %(name_dictionary['name'],name_dictionary['type'],name_dictionary['sql'])
        

#formats LookML for each row in the JSON sample, uses multiple samples to properly detect data type in case of null values
def parse_jsons(json_query_result,json_column_name):
    name_list  = []
    master_string = ''
    
    for json_string in json_query_result:
        dictionary = json.loads(json_string)
        dictionary_list = convert_lookml(dictionary,True,json_column_name)
        for name_dictionary in dictionary_list:
            if name_dictionary['name'] not in name_list:
                name_list.append(name_dictionary['name'])
                if master_string == '':
                    master_string = format_lookml(name_dictionary)
                else:
                    master_string += '\n\n' + format_lookml(name_dictionary)
    return master_string


#formats view file for non-JSON columns
def parse_other_dimensions(query_result):
    name_list  = []
    master_string = ''
    
    for col in query_result:
        dictionary_list = convert_lookml(col)
        for name_dictionary in dictionary_list:
            if name_dictionary['name'] not in name_list:
                name_list.append(name_dictionary['name'])
                if master_string == '':
                    master_string = format_lookml(name_dictionary)
                else:
                    master_string += '\n\n' + format_lookml(name_dictionary)
                    
    return master_string


#pushes the new view file to the github repository
def push_new_view(repo,master_string):
    new_file_path = os.path.join(repo.working_tree_dir, '%s.view.lkml' %view_name)
    f = open(new_file_path, 'w')
    f.write(master_string)
    f.close()                             
    repo.index.add([new_file_path])                      
    repo.index.commit("Added new parsed json view file")
    o= repo.remote(name='origin')
    o.push()
    return


#takes in yaml file with necessary inputs, selects top 25 rows of table as sample, and calls helper functions to create the view file
def main():
    print('Please specify the path to the JSON_to_LookML config file')
    json_config_path = input()
    f = open(json_config_path)
    params = yaml.load(f)
    f.close()
    config_path = params['config_path']
    connection_id = params['connection_id']
    project_id = params['project_id']
    table_name = params['table_name']
    view_name = params['view_name']
    github_access_token = params['github_access_token']

    connect_looker(config_path)
    repo = pull_github_repo(project_id,github_access_token)
    query_body = {}
    query_body['connection_id'] = connection_id
    query_body['sql'] = 'select * from %s limit 100' %table_name
    query = looker.create_sql_query(query_body)
    query_result = looker.run_sql_query(query['slug'])
    json_cols = find_json_cols(query_result)
    master_string = 'view: %s {\n\tsql_table_name: %s ;;' %(view_name,table_name)
    master_string += '\n\n' + parse_other_dimensions(query_result)
    for col_name in json_cols:
        json_query_result = [query_result[i][col_name] for i in range(len(query_result))]
        master_string += '\n\n' + parse_jsons(json_query_result,col_name)
    master_string += '\n\n' + '\tmeasure: count { \n\ttype: count \n\t} \n\n}' 
    push_new_view(repo,master_string)
    return 


if __name__ == "__main__":
    main()

