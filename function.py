from datetime import datetime, timedelta
import requests
from twilio.rest import Client
from dateutil.parser import parse
import matplotlib.pyplot as plt
def main():
    country = "germany"
    today = datetime.now().date()
    week_ago = today - timedelta(days=14)
    print("Getting COVID data")
    cases = get_country_confirmed_infected(country, week_ago, today)
    latest_day = cases[-1]
    earliest_day = cases[0]
    percentage_increase = (latest_day['Cases'] - earliest_day['Cases']) / (earliest_day['Cases'] / 100)
    msg = f"There were {latest_day['Cases']} confirmed COVID cases in {country} " \
          f"on {parse(latest_day['Date']).date()}\n"
    if percentage_increase > 0.0:
        msg += f"This is *{round(abs(percentage_increase), 2)}%* increase over the last week. " \
               f"\nTravel is not recommended ✈️ ❌"
        msg += "\n*Stay Inside and stay safe*"
    else:
        msg += f"This is *{round(abs(percentage_increase), 2)}%* decrease over the last week. " \
               f"Travel may be OK ✈️ ✅"
    print("Sending Whatsapp message")
    send_whatsapp_message(msg)
    print("Job finished successfully")


def get_country_confirmed_infected(country, start_date, end_date):
    resp = requests.get(f"https://api.covid19api.com/country/{country}/status/confirmed", params={"from": start_date, "to": end_date})
    return resp.json()

def send_whatsapp_message(msg):
    account_sid = '<YOUR_OWN_TWILIO_SID>'
    auth_token = '<YOUR_OWN_TWILIO_AUTH_TOKEN'
    Client(account_sid, auth_token).messages.create(
        from_='whatsapp:+14155238886',
        to='whatsapp:<YOUR_MOBILE_NUMBER>',
        body=msg
    )
