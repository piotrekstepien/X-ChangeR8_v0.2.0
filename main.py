from datetime import date
import PySimpleGUI as sg
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from functions import *


today = str(date.today())
date_to = today
list_of_currencies = ["USD", "EUR", "BGN", "PLN", "NOK"]
#
# Builds GUI:
layout = [
    [sg.Combo(list_of_currencies, default_value="USD", key="-CURRENCY1-"), sg.Text("to"),
     sg.Combo(list_of_currencies, default_value="EUR", key="-CURRENCY2-"), sg.Text("from"),
     sg.Input(key="-CALENDAR_INPUT_FROM-", enable_events=True, visible=False),
     sg.CalendarButton(button_text=today, target="-CALENDAR_INPUT_FROM-", key="-DATEFROM-", format=("%Y-%m-%d"),
                       enable_events=True),
     sg.Text("to"), sg.Input(key="-CALENDAR_INPUT_TO-", enable_events=True, visible=False),
     sg.CalendarButton(button_text=today, target="-CALENDAR_INPUT_TO-", key="-DATETO-", format=("%Y-%m-%d"),
                       enable_events=True),
     sg.Button("SUBMIT")],
    [sg.Text("Today's exchange rate: "), sg.Text(key="-TODAYRATE-", enable_events=True)],
    [sg.Canvas(key="-CANVAS-")]
]
window = sg.Window("X-changeR8 V0.0.1", layout, finalize=True)

while True:
    event, values = window.read(timeout=5)
    if event == sg.WINDOW_CLOSED:
        break
    if event == "-CALENDAR_INPUT_FROM-":
        date_from = values[
            "-CALENDAR_INPUT_FROM-"]
        window["-DATEFROM-"].update(text=date_from)
        window.refresh()
    if event == "-CALENDAR_INPUT_TO-":
        date_to = values[
            "-CALENDAR_INPUT_TO-"]
        # if date_to == "":
        #     date_to = today
        window["-DATETO-"].update(text=date_to)
        window.refresh()
    if event == "SUBMIT":
        # date_from = values[
        #     "-CALENDAR_INPUT_FROM-"]  # !!!!!!!!!!!SPRAWDZ REFRESH WINDOW --> WINDOW CLOSE -> WINDOW OPEN !!!!!!!!!!!!
        # window["-DATEFROM-"].update(text=date_from)
        # window.refresh()
        # date_to = values[
        #     "-CALENDAR_INPUT_TO-"]  # !!!!!!!!!!!SPRAWDZ REFRESH WINDOW --> WINDOW CLOSE -> WINDOW OPEN !!!!!!!!!!!!1
        # if date_to == "":
        #     date_to = today
        # window["-DATETO-"].update(text=date_to)
        window.refresh()
        currency1 = values["-CURRENCY1-"]
        currency2 = values["-CURRENCY2-"]
        if currency1 != "PLN" and currency2 != "PLN":
            url1 = "http://api.nbp.pl/api/exchangerates/rates/A/" + f"{currency1}/{date_from}/{date_to}"
            url2 = "http://api.nbp.pl/api/exchangerates/rates/A/" + f"{currency2}/{date_from}/{date_to}"
            first_currency = get_currency_as_list(url1)
            second_currency = get_currency_as_list(url2)
        else:
            url1 = pln_chosen(currency1, currency2, date_from, date_to)
            if currency1 == "PLN":
                first_currency = only_ones(url1)
                second_currency = get_currency_as_list(url1)
            else:
                first_currency = get_currency_as_list(url1)
                second_currency = only_ones(url1)
        # today rate:
        today_exchange_rate = round(first_currency[-1] / second_currency[-1], 4)
        window["-TODAYRATE-"].update(today_exchange_rate)

        currency = get_currency_ratio(first_currency, second_currency)
        fig = plt.figure(figsize=(6, 4))
        fig.add_subplot(111).plot(get_date_list(url1), currency)
        figure_canvas_agg = FigureCanvasTkAgg(fig, window["-CANVAS-"].TKCanvas)
        figure_canvas_agg.draw()
        figure_canvas_agg.get_tk_widget().pack()


window.close()
