import configparser
import tableauserverclient as TSC
import csv
import pandas as pd
import objectpath
import re
from datetime import date, datetime, timezone
from dateutil.relativedelta import relativedelta

XXXXXXXX

timelookback = date.today() + relativedelta(months=-2)
config = configparser.ConfigParser()
config.read('config.ini')
cred = config['config']
url, token_name, token = cred["url"], cred["token_name"], cred["token"]
tableau_auth = TSC.PersonalAccessTokenAuth(token_name, token, '')
server = TSC.Server(url, use_server_version=True)
user_list = []
data_list = []
result_list = []


with server.auth.sign_in(tableau_auth):
    request_options = TSC.RequestOptions(pagesize=1000)
    users=[]
    for user in TSC.Pager(server.users, request_options):
        users.append(user)

    for user in users:

        data_list.append({
            'username': user.name,
            'last_login': user.last_login,
            'role': user.site_role
        })

        #if user.site_role == 'Viewer' or user.site_role == 'Unlicensed':
        if user.site_role == 'Unlicensed':

            server.users.populate_groups(user)        
            add_to_list = True

            for group in user.groups:
                #print(group.name)
                if group.name == "ACL_SSO_TableauCloud":
                    add_to_list = False
                    break

            #print(add_to_list)
            if add_to_list == True:
                result_list.append({
                    'username': user.name,
                    'last_login': user.last_login,
                    'role': user.site_role,
                    'user_id': user.external_auth_user_id,
                    'id': user.id
                })
                user_list.append(user.id)

    df = pd.DataFrame(data_list, columns=['username', 'last_login', 'role'])
    resultdataframe = pd.DataFrame(result_list, columns=['username', 'last_login', 'role', 'user_id', 'id'])
    resultdataframe.to_csv('all_user_details.csv')

    request_options = TSC.RequestOptions(pagesize=1000)
    groups = TSC.Pager(server.groups, request_options)
    allgroups = [(group.id, group.name) for group in groups]

    # Getting group object
    all_groups, pagination_item = server.groups.get(request_options)
    for group in all_groups:
        if group.name == "ACL_SSO_TableauCloud":
            add_group = group
            break
        
    for user_id in user_list:
            user_item = server.users.get_by_id(user_id)
            server.groups.add_user(add_group, user_id)
            user_item = server.users.update(user_item)
