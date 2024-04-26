import configparser
import tableauserverclient as TSC
import csv
import pandas as pd
import objectpath
import re
from datetime import date, datetime, timezone
from dateutil.relativedelta import relativedelta


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

        print(user.name)