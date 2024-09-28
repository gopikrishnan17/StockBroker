from jugaad_data.nse import NSELive, index_raw, stock_df
from pprint import pprint
import datetime
from dateutil.relativedelta import relativedelta
nse = NSELive()


def currniftystatus(index):
    nifty = nse.live_index(index)
    data = nifty['metadata']
    data['timeVal'] = nifty['timestamp']
    return data

def convert_to_date(date_str):
    date_obj = datetime.datetime.strptime(date_str, '%d %b %Y')
    return date_obj

def stockdata(symbol, years=1, months=0, days = 7):
    to_date = datetime.date.today()
    from_date = to_date - relativedelta(years=years, months=months, days=days)
    allData = {}
    try:
        df = stock_df(symbol= symbol, from_date = from_date,
                to_date = to_date, series="EQ")
    except Exception as e:
        pass
        # allData = {'Error': e.args}
    else:
        close_price = list(df['CLOSE'])[::-1]
        dates = list(df['DATE'])[::-1]
        q = nse.stock_quote(symbol)
        priceInfo = q['priceInfo']
        info = q['info']
        allData = {'close_price': close_price, 'dates': dates, 'priceInfo':priceInfo, 'info': info}
    return allData

def getstockname(arr):
    allData = {}
    for symbol in arr:
        try:
            q = nse.stock_quote(symbol)
        except:
            pass

        else:
            name = q['info']['companyName']
            allData[symbol] = name
    return allData