import requests


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


def pln_chosen(currency_1, currency_2, date_1, date_2):
    if currency_1 == "PLN":
       url1 = "http://api.nbp.pl/api/exchangerates/rates/A/" + f"{currency_2}/{date_1}/{date_2}"
    if currency_2 == "PLN":
       url1 = "http://api.nbp.pl/api/exchangerates/rates/A/" + f"{currency_1}/{date_1}/{date_2}"
    return url1


def only_ones(url):
    currency_list = get_currency_as_list(url)
    lista = []
    for i in range(0, len(currency_list)):
        lista.append(1)
    return lista


def get_currency_ratio(currency_1, currency_2):  # returns ratio of any currencies as a list in specific time period
    ratio = []
    for i in range(0, len(currency_1)):
        ratio.append(round(currency_1[i] / currency_2[i], 4))
    return ratio