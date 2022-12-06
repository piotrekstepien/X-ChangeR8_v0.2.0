from datetime import date
import PySimpleGUI as sg
import requests
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def get_date_list(url):  # returns period of time as a list of strings
    date_dict = get_exchange_data_from_nbp(url)
    date_list = list(date_dict)
    return date_list


def get_exchange_data_from_nbp(url):
    response = requests.get(url)
    dictionary_ = response.json()
    list_ = dictionary_["rates"]
    dict_ = {}
    date_ = []
    value_ = []
    for item in list_:
        date_.append(item["effectiveDate"])
        value_.append(item["mid"])
    for item in range(0, len(value_)):
        dict_[date_[item]] = value_[item]
    return dict_


def get_currency_as_list(
        url):  # reformats currency exchange rate from a dictionary to a list -> useful for current value of exchange reate
    currency_dict = get_exchange_data_from_nbp(url)
    currency_list = list(currency_dict.values())
    return currency_list


def get_currency_ratio(currency_1, currency_2):  # returns ratio of any currencies as a list in specific time period
    ratio = []
    for i in range(0, len(currency_1)):
        ratio.append(round(currency_1[i] / currency_2[i], 4))
    return ratio


today = date.today()

# url = "http://api.nbp.pl/api/exchangerates/rates/A/USD/2022-01-01/" + f"{today}"


# currency = get_currency_as_list(url)

list_of_currencies = ["USD", "EUR", "BGN", "PLN"]
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
    [sg.Canvas(key="-CANVAS-")]
]
window = sg.Window("X-changeR8 V0.0.1", layout, finalize=True)

while True:
    event, values = window.read(timeout=5)
    if event == sg.WINDOW_CLOSED:
        break
    if event == "SUBMIT":
        date_from = values[
            "-CALENDAR_INPUT_FROM-"]  # !!!!!!!!!!!SPRAWDZ REFRESH WINDOW --> WINDOW CLOSE -> WINDOW OPEN !!!!!!!!!!!!1
        window["-DATEFROM-"].update(text=date_from)
        date_to = values[
            "-CALENDAR_INPUT_TO-"]  # !!!!!!!!!!!SPRAWDZ REFRESH WINDOW --> WINDOW CLOSE -> WINDOW OPEN !!!!!!!!!!!!1
        if date_to == "":
            date_to = today
        window["-DATETO-"].update(text=date_to)
        #if values["-CURRENCY1-"]=="PLN":
        ##################################################
        #KILL THE BUG!
        ##################################################

        currency1 = values["-CURRENCY1-"]
        currency2 = values["-CURRENCY2-"]
        url1 = "http://api.nbp.pl/api/exchangerates/rates/A/" + f"{currency1}/{date_from}/{date_to}"
        url2 = "http://api.nbp.pl/api/exchangerates/rates/A/" + f"{currency2}/{date_from}/{date_to}"
        first_currency = get_currency_as_list(url1)
        second_currency = get_currency_as_list(url2)
        currency = get_currency_ratio(first_currency, second_currency)
        fig = plt.figure(figsize=(6, 4))
        fig.add_subplot(111).plot(get_date_list(url1), currency)
        figure_canvas_agg = FigureCanvasTkAgg(fig, window["-CANVAS-"].TKCanvas)
        figure_canvas_agg.draw()
        figure_canvas_agg.get_tk_widget().pack()

window.close()
