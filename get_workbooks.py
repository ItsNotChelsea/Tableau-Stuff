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
    #request_options = TSC.RequestOptions(pagesize=1000)

    all_flow_items, pagination_item = server.flows.get()

    #print("There are {} flows on site:" .format(pagination_item.total_available))
    #print([[flow.id, flow.name] for flow in all_flow_items])

    for flow in all_flow_items:
        if flow.id == "72xx0b55-a71f-433b-bb65-7a7346a95e95":
            job = server.flows.refresh(flow)