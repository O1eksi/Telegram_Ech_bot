import requests
import math
import datetime
import pandas
import matplotlib.pyplot as plt
import asyncio



def ecvhange_race(to_val, from_val="USD", amount="1"):
    """

    :param to_val:
    :param from_val:
    :param amount:
    :return:
    """
    url = "https://fxmarketapi.com/apiconvert"
    querystring = {"api_key":"2lX0mpYgRsSVsQPJ_-ET", "from":from_val, "to":to_val, "amount":amount}
    response = requests.get(url, params=querystring)
    result = response.json()
    result["total"] = math.floor(result["total"]*100)/100
    # return (type(result["total"]))
    otvet = f'amount = {amount} {from_val} \n from {from_val} to {result["to"]} \n equals - {result["total"]} ' \
            f'{result["to"]}'
    return otvet




def course_dynamics_oneWeek(from_val, to_val, now=None):

    if now == None:
        now = datetime.datetime.now()
    last_week = now - datetime.timedelta(days=7)
    url = "https://fxmarketapi.com/apipandas"
    api_key = "2lX0mpYgRsSVsQPJ_-ET"
    currency = from_val + to_val
    start_date = last_week.strftime("%Y-%m-%d")
    end_date = now.strftime("%Y-%m-%d")
    df = pandas.read_json(f"{url}?api_key={api_key}&currency={currency}&start_date={start_date}&end_date={end_date}")
    plt.plot(df.get("close"))
    plt.suptitle(f'{from_val} to {to_val} rate')
    plt.xticks(rotation=90)
    print(df.get("close"))
    print(plt.show())          #Fix Me


def vall(name=None, base=None):
    url = "https://fxmarketapi.com/apicurrencies?api_key=2lX0mpYgRsSVsQPJ_-ET"
    response = requests.get(url)
    result = response.json()
    val = result["currencies"]
    val['USDBTC'] = val.pop('BTCUSD')
    val["USDUSD"] = "United States dollar"
    if base == None:
        if name != None:
            return val["USD" + name]
        else:
            currencies = []
            for i in result["currencies"].keys():
                currencies.append(i[3:])
            return currencies
    else:
        del val["USD" + base]
        if name != None:
            return val["USD" + name]
        else:
            currencies = []
            for i in result["currencies"].keys():
                currencies.append(i[3:])
            return currencies




# print(vall())
# course_dynamics_oneWeek("USD", "RUB")
# print(ecvhange_race("RUB", amount="55 5"))

