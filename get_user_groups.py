import configparser
import tableauserverclient as TSC
import csv
import pandas as pd
import objectpath
import re
from datetime import date, datetime, timezone
from dateutil.relativedelta import relativedelta

import configparser
import tableauserverclient as TSC
import csv
import pandas as pd
import objectpath
import re
from datetime import date, datetime, timezone
from dateutil.relativedelta import relativedelta


timelookback = date.today() + relativedelta(months=-3)
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


    all_users, pagination_item = server.users.get()
    print("\nThere are {} user on site: ".format(pagination_item.total_available))
   # print([user.name for user in all_users])


    for user in all_users:
        page_n = server.users.populate_groups(user)
        #print("\nUser {0} is a member of {1} groups".format(all_users[0].name, page_n.total_available))
        print("\nThe groups are:")
        
        for group in user.groups :
            print(group.name)

        #for user in users:
            #print(user.name)
        #for user in TSC.Pager(server.users, request_options):
            #users.append(user)
