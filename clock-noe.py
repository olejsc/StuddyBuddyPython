# -*- coding:utf-8 -*_

from tkinter import *
from datetime import *

# Koden starter herfra. 

master = Tk()
variable = IntVar(master)
variable.set("Frequency")
options = {1: 5, 2: 2, 3: 3}
OptionMenu(master, variable, *options.keys()).pack()


def shut_down():
    master.quit()

button = Button(master, text="OK", command=shut_down)
button.pack()


def time_when_notified(choice):
    for key, value in options.items():  # Går gjennom elementene i dictionary
        if key == choice:  # Hvis key er lik valget brukeren velger
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Finner ut tiden nå.
            solve = datetime.strptime(now, "%Y-%m-%d %H:%M:%S")  # Finner ut og legger til når personen vil bli varslet
            solve += timedelta(seconds=value)  # -''-
            notification_time = solve.strftime("%Y-%m-%d %H:%M:%S")  # Variabel for senere bruk
            return notification_time


#  Sender varsel når nåtid er lik varseltid.


def check_vol2():
    last_notification = time_when_notified(variable.get())  # Lager variabel med angitt varseltid. Tid i framtiden.
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    datetime_young = datetime.strptime(now, "%Y-%m-%d %H:%M:%S")  # Formatvalg
    datetime_older = datetime.strptime(last_notification, "%Y-%m-%d %H:%M:%S")  # Formatvalg
    time_since_last = datetime_older - datetime_young
    difference = (time_since_last.total_seconds() / 3600)
    while True:
        if difference == 0:
            break
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        datetime_young = datetime.strptime(now, "%Y-%m-%d %H:%M:%S")  # Formatvalg
        time_since_last = datetime_older - datetime_young
        difference = (time_since_last.total_seconds()/3600)
    print("Du skal få varsel nå")  # Kjør notifikasjonskode


'''
idle-varsler. Finne ut når programmet avsluttes.
def check():
    last_notification = time_when_notified(valg)  # Lager variabel med angitt varseltid. Tid i framtiden.
    if funksjon for å sjekke om det er varsel???
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        datetime_young = datetime.strptime(now, "%Y-%m-%d %H:%M:%S")  # Formatvalg
        datetime_older = datetime.strptime(last_notification, "%Y-%m-%d %H:%M:%S")  # Formatvalg
        time_since_last = datetime_older - datetime_young  # Regner ut differansen ved hjelp av timedelta
        hours = time_since_last.total_seconds()/3600  # Gjør om timedelta til totalt sekunder, gjør dermed om til time
        if hours > frequency.get(valg):  # Hvis brukeren burde ha blitt varslet, send varsel. #  Hvis programmet er idle.
            print("HALLLLLOOOO, NOTIFIKASJON LZZZZM. DU MÅ HUSKE Å LESE")
'''

print("Program started at:", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
mainloop()
time_when_notified(variable.get())
check_vol2()
print("Program finished at:", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
# Lagre denne i en fil, finn ut når programmet ble slått av, hent den fra fil, bruk som verdi i check(). if-statement.

