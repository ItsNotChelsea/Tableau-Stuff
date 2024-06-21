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

    #wkb=server.workbooks.get_by_id('workbook_luid_here')

    #server.workbooks.populate_views(wkb)

    #server.workbooks.populate_connections(wkb)

    server.workbooks.download('workbook-luid', filepath='C:/Temp/Tableau', include_extract=True)