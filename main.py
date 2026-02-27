# To run and test the code you need to update 4 places:
# 1. Change MY_EMAIL/MY_PASSWORD to your own details.
# 2. Go to your email provider and make it allow less secure apps.
# 3. Update the SMTP ADDRESS to match your email provider.
# 4. Update birthdays.csv to contain today's month and day.
# See the solution video in the 100 Days of Python Course for explainations.

import pandas
import datetime as dt
from smtplib import SMTP
from pathlib import Path
import random
import os

# import os and use it to get the Github repository secrets
MY_EMAIL = os.environ.get("MY_EMAIL")
MY_PASSWORD = os.environ.get("MY_PASSWORD")

people_df = pandas.read_csv("birthdays.csv")
now = dt.datetime.now()
current_month = now.month
current_day = now.day

matched_persons = people_df[(people_df.month == current_month) & (people_df.day == current_day)]

for index, person in matched_persons.iterrows():
    name = person["name"]
    email_address = person["email"]
    folder_path = Path("./letter_templates")
    all_files = [file for file in folder_path.iterdir() if file.is_file()]
    file_choice = random.choice(all_files)
    with open(f"./letter_templates/{file_choice.name}") as file:
        contents = file.readlines()
        msg_content = ""
        for word in contents:
            msg_content += word.replace("[NAME]", name)

    username = f"{email_address}"
    port = 587
    mail_server = "smtp.gmail.com"

    with SMTP(host=mail_server, port=port) as connection:
        connection.starttls()
        connection.login(user=MY_EMAIL, password=MY_PASSWORD)
        connection.sendmail(from_addr=username,
                            to_addrs=username,
                            msg=f"Subject: Birthday Wish 🎉🎉🎂\n\n{msg_content}".encode("utf-8"))
