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


  
#main
    
with server.auth.sign_in(tableau_auth):
    request_options = TSC.RequestOptions(pagesize=1000)
    users=[]

    #yesterday_users = get_yesterday_users()
    #with open('all_users.csv', 'r') as file:
        # Creating a csv reader object
        #yesterday_users = csv.DictReader(file)

    yesterday_users = pd.read_csv('all_users.csv', index_col='username')
    print(yesterday_users)

        #for row in yesterday_users:
            #print(row["username"])

    for user in TSC.Pager(server.users, request_options):
           users.append(user)

            #print(user.name)

            #if user.name == row["username"]:
                #print("New User")
                #print(user.name)
            #else:
                #print("False")

    result_list.append({
        'username': user.name,
        'role': user.site_role,
    })
        
    #df = pd.DataFrame(data_list, columns=['username', 'role'])
    resultdataframe = pd.DataFrame(result_list, columns=['username', 'role'])
    resultdataframe.to_csv('all_users_new.csv')



    

def post_to_teams(message):
    # Replace with your actual Teams webhook URL
    webhook_url = "https://your-teams-webhook-url"

    # Create a payload with the message
    payload = {
        "text": message
    }