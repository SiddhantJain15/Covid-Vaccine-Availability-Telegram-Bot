import requests
from datetime import datetime
import time
today = datetime.today()
date = today.strftime('%d-%m-%Y')

url_states = 'https://cdn-api.co-vin.in/api/v2/admin/location/states'
r = requests.get(url_states)
flag = 0
for states in r.json()['states']:
    
    url_district = 'https://cdn-api.co-vin.in/api/v2/admin/location/districts/{}'.format(states['state_id'])
    r1 = requests.get(url_district)
    for district in r1.json()['districts']:
        url = 'https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id={}&date={}.'.format(district['district_id'], '03-05-21')
        r = requests.get(url)
        for center in r.json()['centers']:
            flag = 0
            for session in center['sessions']:
                if session['available_capacity'] > 10 and session['min_age_limit'] == 18:
                    flag = 1 #only 1 notification per centre is sufficient, so breaking loop after 1
                    tele_url = 'https://api.telegram.org/bot1659940043:AAEBiuLtxY1NeUt8Ctw6XaT69NBj02vlfYo/sendMessage?chat_id=-599114522&text=COVID Vaccine for age group 18 and more available in {}, {}. {}. Date- {}. Capacity- {}'.format(district['district_name'], states['state_name'], center['name'], session['date'], session['available_capacity'])
                    requests.get(tele_url)
                    #print("COVID Vaccine for 18+ available in {}, {}. {}.".format(district['district_name'], states['state_name'], center['name']), "Date-", session['date'], "Capacity-", session['available_capacity'])
                if flag == 1:
                    break
            if flag == 1:
                break
