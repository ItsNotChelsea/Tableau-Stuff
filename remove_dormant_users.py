import configparser
import tableauserverclient as TSC
import csv
import pandas as pd
import objectpath
import re
from datetime import date, datetime, timezone
from dateutil.relativedelta import relativedelta

# Rest of the code ...
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
    request_options = TSC.RequestOptions(pagesize=1000)
    users = TSC.Pager(server.users, request_options)

    for user in users:

        data_list.append({
            'username': user.name,
            'last_login': user.last_login,
            'role': user.site_role
        })

        date_time = str(user.last_login)
        match = re.search(r'\d{4}-\d{2}-\d{2}', date_time)

        xxx = str(user.last_login)

        if match:
            date = datetime.strptime(match.group(), '%Y-%m-%d').date()
        else:
            date = None

        #if (date and user.site_role == 'Viewer' and date < timelookback) or (user.site_role == 'Viewer' and date == None):
        if user.site_role == 'Viewer' and date == None:
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
    resultdataframe.to_csv('dormant_user_details.csv')

    request_options = TSC.RequestOptions(pagesize=1000)
    groups = TSC.Pager(server.groups, request_options)
    allgroups = [(group.id, group.name) for group in groups]

    # Getting group object
    all_groups, pagination_item = server.groups.get(request_options)



    for user_id in user_list:
        print(user_id)
        user_item = server.users.get_by_id(user_id)
        #server.groups.remove_user(group, user_id)
        user_item = server.users.update(user_item)
        user_item.site_role = "Unlicensed"
        user_item = server.users.update(user_item)


