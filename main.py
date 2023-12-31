import requests
from datetime import datetime
import smtplib
import time
MY_LAT= 36.778259
MY_LONG= -119.417931

def is_iss_close_to_me():
    response= requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data=response.json()

    iss_latitude=float(data["iss_position"]["latitude"])
    iss_longitude=float(data["iss_position"]["longitude"])

    if (MY_LAT - 5 <= iss_latitude and MY_LAT + 5 >= iss_latitude):
        if (MY_LONG - 5 <= iss_longitude and MY_LONG + 5 >= iss_longitude):
            return True

def is_night():
    parameters={
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0
    }
    response= requests.get("https://api.sunrise-sunset.org/json",params=parameters)
    response.raise_for_status()
    data=response.json()
    sunrise=int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset=int(data["results"]["sunset"].split("T")[1].split(":")[0])

    time_now=datetime.now().hour

    if time_now>=sunset or time_now<=sunrise:
        return True

while True:
    time.sleep(60)
    if is_iss_close_to_me() and is_night():
        with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
            connection.starttls()
            connection.login(user="hihello2405@gmail.com", password="gdwaoiwzpupscepw")
            connection.sendmail(from_addr="hihello2405@gmail.com", to_addrs="harinidonthula@gmail.com",
                                msg=f"Subject:Look Up\n\nThe ISS is above you in the sky")



is_iss_close_to_me()