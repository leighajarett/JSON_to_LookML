# -*- coding: UTF-8 -*-
import requests
from pprint import pprint as pp
import json
import re

from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

class LookerApi(object):

    def __init__(self, token, secret, host):

        self.token = token
        self.secret = secret
        self.host = host

        self.session = requests.Session()
        self.session.verify = False

        self.auth()

    def auth(self):
        url = '{}{}'.format(self.host,'login')
        params = {'client_id':self.token,
                  'client_secret':self.secret}
        r = self.session.post(url,params=params)
        access_token = r.json().get('access_token')
        # print(access_token)
        self.session.headers.update({'Authorization': 'token {}'.format(access_token)})


# POST /dashboards/{dashboard_id}/prefetch
    def create_prefetch(self, dashboard_id, ttl):
        url = '{}{}/{}/prefetch'.format(self.host,'dashboards',dashboard_id)
        params = json.dumps({'ttl':ttl,
                  })
        print(url)
        print(params)
        r = self.session.post(url,data=params)
        pp(r.request.url)
        pp(r.request.body)
        pp(r.json())

# GET
    def get_dashboard(self, dashboard_id,fields=''):
        url = '{}{}/{}'.format(self.host,'dashboards',dashboard_id)
        params = {"fields":fields}
        r = self.session.get(url,params=params)
        if r.status_code == requests.codes.ok:
            return r.json()
# PATCH
    def update_dashboard(self,dashboard_id,body={}):
        url = '{}{}/{}'.format(self.host,'dashboards',dashboard_id)
        body = json.dumps(body)
        print(" --- updating dashboard --- ")
        r = self.session.patch(url,data=body)
        if r.status_code == requests.codes.ok:
            return r.json()

    def get_look_info(self,look_id,fields=''):
        url = '{}{}/{}'.format(self.host,'looks',look_id)
        print(url)
        params = {"fields":fields}
        r = self.session.get(url,params=params)
        if r.status_code == requests.codes.ok:
            return r.json()

# POST /sql_queries/

    def create_sql_query(self,query_body):
        url = '{}{}'.format(self.host,'sql_queries')
        # print(url)
        params = json.dumps(query_body)
        print(" --- creating query --- ")
        r = self.session.post(url,data=params)
        # print(r.text)
        print(r.status_code)
        if r.status_code == requests.codes.ok:
            return r.json()

# GET sql_queries/

    def run_sql_query(self,slug):
        url = '{}{}/{}/run/json'.format(self.host,'sql_queries', slug)
        print(url)
        r = self.session.post(url)
        #print(r.text)
        print(r.status_code)
        if r.status_code == requests.codes.ok:
            return r.json()

 # GET /queries/slug/{slug}  

    def get_sql_query(self,slug):
        url = '{}{}/slug/{}'.format(self.host,'queries', slug)
        print(url)
        r = self.session.get(url)
        # print(r.text)
        print(r.status_code)
        if r.status_code == requests.codes.ok:
            return r.json()

# GET /queries/
    def get_query(self,query_id,fields=''):
        url = '{}{}/{}'.format(self.host,'queries',query_id)
        print(url)
        params = {"fields":fields}
        r = self.session.get(url,params=params)
        if r.status_code == requests.codes.ok:
            return r.json()

    # POST /queries/
    def create_query(self,query_body, fields=[]):
        url = '{}{}'.format(self.host,'queries')
        # print(url)
        params = json.dumps(query_body)
        print(" --- creating query --- ")
        r = self.session.post(url,data=params, params = json.dumps({"fields": fields}))
        # print(r.text)
        # print(r.status_code)
        if r.status_code == requests.codes.ok:
            return r.json()


      #GET      queries/run/
    def run_query(self,query_id):
            url = '{}{}/{}/run/json'.format(self.host,'queries',query_id)
            # print(url)
            params = {}
            print(" --- running query --- ")
            r = self.session.get(url,params=params)
            if r.status_code == requests.codes.ok:
                return r.json()

      #GET      queries/run/
    def run_inline_query(self,body={}):
            url = '{}{}/run/json'.format(self.host,'queries')
            # print(url)
            params = json.dumps(body)
            # print(" --- running query --- ")
            r = self.session.post(url,data=params)
            # print(url)
            print(r.status_code)
            if r.status_code == requests.codes.ok:
                return r.json()



# GET /looks/<look_id>/run/<format>
    def get_look(self,look_id, format='json', limit=500):
        url = '{}{}/{}/run/{}'.format(self.host,'looks',look_id, format)
        print(url)
        params = {limit:100000}
        r = self.session.get(url,params=params, stream=True)
        if r.status_code == requests.codes.ok:
            return r.json()

# PATCH /looks/<look_id>
    def update_look(self,look_id,body,fields=''):
        url = '{}{}/{}'.format(self.host,'looks',look_id)
        body = json.dumps(body)
        params = {"fields":fields}
        print(" --- updating look --- ")
        r = self.session.patch(url,data=body,params=params)
        if r.status_code == requests.codes.ok:
            return r.json()

    def download_look(self,look_id, format='xlsx'):
        url = '{}{}/{}/run/{}'.format(self.host,'looks',look_id, format)
        params = {}
        r = self.session.get(url,params=params, stream=True)
        print(r.status_code)
        if r.status_code == requests.codes.ok:
            image_name = 'test2.xlsx'
            with open(image_name, 'wb') as f:
                for chunk in r:
                    f.write(chunk)
        else:
            print(r.json())
        return 'done'

    def create_look(self,look_body):
        url = '{}{}'.format(self.host,'looks')
        print(url)
        params = json.dumps(look_body)
        r = self.session.post(url,data=params)
        if r.status_code == requests.codes.ok:
            return r.json()

# GET /users
    def get_all_users(self):
        url = '{}{}'.format(self.host,'users')
        # print("Grabbing Users " + url)
        params = {}
        r = self.session.get(url,params=params)
        if r.status_code == requests.codes.ok:
            return r.json()

# GET /users/id
    def get_user(self,id=""):
        url = '{}{}{}'.format(self.host,'users/',id)
        # print("Grabbing User(s) " + str(id))
        # print(url)
        params = {}
        r = self.session.get(url,params=params)
        if r.status_code == requests.codes.ok:
            return r.json()


# PATCH /users/id
    def update_user(self,id="",body={}):
        url = '{}{}{}'.format(self.host,'users/',id)
        # print("Grabbing User(s) " + str(id))
        print(url)
        params = json.dumps(body)
        r = self.session.patch(url,data=params)
        if r.status_code == requests.codes.ok:
            return r.json()
# DELETE /users/id
    def delete_user(self,id="",body={}):
        url = '{}{}{}'.format(self.host,'users/',id)
        # print("Grabbing User(s) " + str(id))
        # print(url)
        # params = json.dumps(body)
        r = self.session.delete(url)
        if r.status_code == requests.codes.ok:
            return r.json()


# GET /user
    def get_current_user(self):
        url = '{}{}'.format(self.host,'user')
        params = {}
        r = self.session.get(url,params=params)
        if r.status_code == requests.codes.ok:
            return r.json()

# PUT /users/{user_id}/roles
    def set_user_role(self,id="", body={}):
        url = '{}{}{}{}'.format(self.host,'users/',id,'/roles')
        # print("Grabbing User(s) " + str(id))
        # print(url)
        params = json.dumps(body)
        r = self.session.post(url,params=params)
        if r.status_code == requests.codes.ok:
            return r.json()

# GET /users/{user_id}/roles
    def get_user_role(self,id=""):
        url = '{}{}{}{}'.format(self.host,'users/',id,'/roles')
        # print("Grabbing User(s) " + str(id))
        # print(url)
        r = self.session.get(url,params={})
        if r.status_code == requests.codes.ok:
            return r.json()

    def get_roles(self):
        url = '{}{}'.format(self.host,'roles')
        # print("Grabbing role(s) ")
        # print(url)
        r = self.session.get(url,params={})
        if r.status_code == requests.codes.ok:
            return r.json()


# PATCH /users/{user_id}/access_filters/{access_filter_id}
    def update_access_filter(self, user_id = 0, access_filter_id = 0, body={}):
        url = '{}{}/{}/{}/{}'.format(self.host,'users',user_id,'access_filters',access_filter_id)
        params = json.dumps(body)
        r = self.session.patch(url,data=params)
        return r.json()

    def create_access_filter(self, user_id = 0, body={}):
        url = '{}{}/{}/{}'.format(self.host,'users',user_id,'access_filters')
        params = json.dumps(body)
        r = self.session.post(url,data=params)
        return r.json()


# GET /users/me
    def get_me(self):
        url = '{}{}'.format(self.host,'user')
        print("Grabbing Myself: " + url)
        params = {}
        r = self.session.get(url,params=params)
        if r.status_code == requests.codes.ok:
            return r.json()

# GET /lookml_models/
    def get_models(self,fields={}):
        url = '{}{}'.format(self.host,'lookml_models')
        # print(url)
        params = fields
        r = self.session.get(url,params=params)
        if r.status_code == requests.codes.ok:
            return r.json()
# GET /lookml_models/{{NAME}}
    def get_model(self,model_name="",fields={}):
        url = '{}{}/{}'.format(self.host,'lookml_models', model_name)
        print(url)
        params = fields
        r = self.session.get(url,params=params)
        if r.status_code == requests.codes.ok:
            return r.json()

# GET /lookml_models/{{NAME}}/explores/{{NAME}}
    def get_explore(self,model_name=None,explore_name=None,fields={}):
        url = '{}{}/{}/{}/{}'.format(self.host,'lookml_models', model_name, 'explores', explore_name)
        # print(url)
        params = fields
        r = self.session.get(url,params=params)
        if r.status_code == requests.codes.ok:
            return r.json()

#GET /scheduled_plans/dashboard/{dashboard_id}
    def get_dashboard_schedule(self,dashboard_id=0):
        url = '{}{}/{}/{}'.format(self.host,'scheduled_plans', 'dashboard',  dashboard_id)
        # print(url)
        r = self.session.get(url)
        if r.status_code == requests.codes.ok:
            return r.json()


#GET /scheduled_plans
    def get_all_schedules(self, user_id=False):
        url = '{}{}'.format(self.host,'scheduled_plans')
        # print(url)
        params = {'user_id':user_id}
        r = self.session.get(url,params=params)
        if r.status_code == requests.codes.ok:
            return r.json()

#GET /scheduled_plans/look/{dashboard_id}
    def get_look_schedule(self,look_id=0):
        url = '{}{}/{}/{}'.format(self.host,'scheduled_plans', 'look',  look_id)
        # print(url)
        r = self.session.get(url)
        if r.status_code == requests.codes.ok:
            return r.json()


# GET /datagroups
    def get_datagroups(self):
        url = '{}{}'.format(self.host,'datagroups')
        r = self.session.get(url)
        if r.status_code == requests.codes.ok:
            return r.json()



#PATCH /scheduled_plans/{scheduled_plan_id}
    def update_schedule(self, plan_id, body={}):
        url = '{}{}/{}'.format(self.host,'scheduled_plans',plan_id)
        params = json.dumps(body)
        # print(url)
        # print(params)
        r = self.session.patch(url,data=params)
        # pp(r.request.url)
        # pp(r.request.body)
        return r.json()


    def sql_runner(self):
        connection_id = "looker"
        sql = "select * from events limit 10"
        body = {}
        body['sql'] = sql
        body['connection_id'] = connection_id
        url = '{}{}'.format(self.host,'sql_queries')
        params = json.dumps(body)
        r = self.session.post(url,data=params)
        slug = r.json()['slug']

        url = '{}{}/{}'.format(self.host,'sql_queries', slug)
        g = self.session.get(url)
        print(url)
        return g.json()

#DELETE /scheduled_plans/{scheduled_plan_id}
    def delete_schedule(self, plan_id):
        url = '{}{}/{}'.format(self.host,'scheduled_plans', plan_id)
        # print(url)
        r = self.session.delete(url)
        if r.status_code == requests.codes.ok:
            return r.json()

#DELETE /looks/{look_id}
    def delete_look(self,look_id,fields=''):
        url = '{}{}/{}'.format(self.host,'looks',look_id)
        print(url)
        params = {"fields":fields}
        r = self.session.delete(url,params=params)
        if r.status_code == requests.codes.ok:
            return r.json()

#DELETE /dashboards/{dashboard_id}
    def delete_dashboard(self,dashboard_id,fields=''):
        url = '{}{}/{}'.format(self.host,'dashboards',dashboard_id)
        print(url)
        params = {"fields":fields}
        r = self.session.delete(url,params=params)
        if r.status_code == requests.codes.ok:
            return r.json()

# GET /dashboards/dashboard_filters/{dashboard_id}
    def get_dashboard_dashboard_filters(self,dashboard_id,fields=''):
        url = '{}{}/{}/{}'.format(self.host,'dashboards',dashboard_id,'dashboard_filters')
        print(url)
        params = {"fields":fields}
        r = self.session.get(url,params=params)
        if r.status_code == requests.codes.ok:
            return r.json()

# PATCH /dashboard_filters/{dashboard_filter_id}
    def update_dashboard_filter(self,dashboard_filter_id,model_name,fields=''):
        url = '{}{}/{}'.format(self.host,'dashboard_filters',dashboard_filter_id)
        print(url)
        body = json.dumps({'model': model_name})
        params = {"fields":fields}
        r = self.session.patch(url,data=body,params=params)
        if r.status_code == requests.codes.ok:
            return r.json()

# POST /groups/{group_id}/users
    def add_users_to_group(self,group_id,user_id):
         url = '{}{}/{}/{}'.format(self.host,'groups',group_id,'users')
         print(url)
         params = json.dumps({'user_id': user_id})
         r = self.session.post(url,data=params)
         if r.status_code == requests.codes.ok:
             return r.json()

# GET spaces
    def get_all_spaces(self,fields=''):
         url = '{}{}'.format(self.host,'spaces')
         print(url)
         params = {'fields':fields}
         r = self.session.get(url,params=params)
         if r.status_code == requests.codes.ok:
             return r.json()

# GET content_metadata_access
    def get_all_content_metadata_access(self,content_metadata_id,fields=''):
         url = '{}{}'.format(self.host,'content_metadata_access')
         print(url)
         params = {'content_metadata_id':content_metadata_id,'fields':fields}
         r = self.session.get(url,params=params)
         if r.status_code == requests.codes.ok:
             return r.json()

# DELETE content_metadata_access
    def delete_content_metadata(self,content_metadata_access_id):
         url = '{}{}/{}'.format(self.host,'content_metadata_access',content_metadata_access_id)
         print(url)
         r = self.session.delete(url)
         if r.status_code == requests.codes.ok:
             return r.json()

#GET /groups/{group_id}
    def get_all_groups(self,fields=''):
        url = '{}{}'.format(self.host,'groups')
        print(url)
        params = {"fields":fields}
        r = self.session.get(url,params=params)
        if r.status_code == requests.codes.ok:
            return r.json()

#GET /groups/{group_id}
    def get_group(self,group_id,fields=''):
        url = '{}{}/{}'.format(self.host,'groups',group_id)
        print(url)
        params = {"fields":fields}
        r = self.session.get(url,params=params)
        if r.status_code == requests.codes.ok:
            return r.json()

#POST /groups
    def create_group(self,group_name,fields=''):
        url = '{}{}'.format(self.host,'groups')
        print(url)
        params = json.dumps({'name': group_name})
        r = self.session.post(url,data=params,params=json.dumps({"fields": fields}))
        if r.status_code == requests.codes.ok:
            return r.json()

# /groups/{group_id}/groups
    def create_group_in_group(self,parent_group_id,child_group_id):
        url = '{}{}/{}/{}'.format(self.host,'groups',parent_group_id,'groups')
        print(url)
        params = json.dumps({'group_id': child_group_id})
        r = self.session.post(url,data=params)
        if r.status_code == requests.codes.ok:
            return "successful addition of group " + str(parent_group_id)

# POST /users/{user_id}/credentials_email
    def create_users_email_credentials(self,user_id,email_address):
        url = '{}{}/{}/{}'.format(self.host,'users',user_id,'credentials_email')
        print(url)
        params = json.dumps({'email': email_address})
        r = self.session.post(url,data=params)
        if r.status_code == requests.codes.ok:
            return r.json()

    def get_users_email_credentials(self,user_id,fields):
        url = '{}{}/{}/{}'.format(self.host,'users',user_id,'credentials_email')
        print(url)
        params = {"fields":fields}
        r = self.session.get(url,params=params)
        if r.status_code == requests.codes.ok:
            return r.json()

    def get_users_saml_credentials(self,user_id,fields):
        url = '{}{}/{}/{}'.format(self.host,'users',user_id,'credentials_saml')
        print(url)
        params = {"fields":fields}
        r = self.session.get(url,params=params)
        if r.status_code == requests.codes.ok:
            return r.json()

    def delete_users_saml_credentials(self,user_id):
        url = '{}{}/{}/{}'.format(self.host,'users',user_id,'credentials_saml')
        print(url)
        r = self.session.delete(url)
        if r.status_code == requests.codes.ok:
            return r.json()
    
    #GET /projects/{project_id}
    def get_active_git_branch(self,project_id):
        url = '{}{}/{}/{}'.format(self.host,'projects',project_id,'git_branch')
        r = self.session.get(url)
        if r.status_code == requests.codes.ok:
            return r.json()

    def get_project(self,project_id):
        url = '{}{}/{}'.format(self.host,'projects',project_id)
        r = self.session.get(url)
        if r.status_code == requests.codes.ok:
            return r.json()

