from fastapi import APIRouter
import requests
from datetime import date, timedelta, datetime
from typing import Optional
from ..database.connection import *
from ..model.stock import *
import json
from bs4 import BeautifulSoup

api_router = APIRouter()
url = "https://finfo-iboard.ssi.com.vn/graphql"

quarters = [3, 6, 9, 12]

headers = {
    'authority': 'finfo-iboard.ssi.com.vn',
    'content-type': 'application/json',
    'origin': 'https://iboard.ssi.com.vn',
    'referer': 'https://iboard.ssi.com.vn/',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/113.0.0.0 Safari/537.36',
    'Cookie': '__cf_bm=Jor8F.J8wFyUmErBrq_GicTcyrdUJdqKHbWuAyCTolY-1685420001-0-AQ9ARsJogOCxtxAxkQO6a8A5JtPsM2q'
              '/UipImj7NYCa++GLGrc5olAKSZyFrN0+ZCI0YczO34rY5nlcmNuEGCl0='
}


def parseSymbol(symbol):
    payload_sub_companies = json.dumps({
        "operationName": "subCompanies",
        "variables": {
            "symbol": symbol,
            "language": "vn",
            "offset": 1,
            "size": 100
        },
        "query": "query subCompanies($symbol: String!, $size: Int, $offset: Int, $language: String) {\n  "
                 "subCompanies(symbol: $symbol, size: $size, offset: $offset, language: $language) {\n    datas {\n   "
                 "   parentsymbol\n      parentcompanyname\n      roleid\n      childsymbol\n      childcompanyname\n "
                 "     chartercapital\n      percentage\n      rolename\n      __typename\n    }\n    paging {\n      "
                 "pagesize\n      currentpage\n      totalpage\n      totalrow\n      __typename\n    }\n    "
                 "__typename\n  }\n}\n"
    })

    payload_shareholders = json.dumps({
        "operationName": "shareholders",
        "variables": {
            "symbol": symbol,
            "size": 50,
            "offset": 1
        },
        "query": "query shareholders($symbol: String!, $size: Int, $offset: Int, $order: String, $orderBy: String, "
                 "$type: String, $language: String) {\n  shareholders(\n    symbol: $symbol\n    size: $size\n    "
                 "offset: $offset\n    order: $order\n    orderBy: $orderBy\n    type: $type\n    language: "
                 "$language\n  )\n}\n"
    })

    payload_leaderships = json.dumps({
        "operationName": "leaderships",
        "variables": {
            "symbol": symbol,
            "offset": 1,
            "size": 100
        },
        "query": "query leaderships($symbol: String!, $size: Int, $offset: Int, $order: String, $orderBy: String) {\n "
                 " leaderships(\n    symbol: $symbol\n    size: $size\n    offset: $offset\n    order: $order\n    "
                 "orderBy: $orderBy\n  ) {\n    datas {\n      symbol\n      fullname\n      positionname\n      "
                 "positionlevel\n      __typename\n    }\n    __typename\n  }\n}\n"
    })

    d = date.today()
    d2 = d - timedelta(days=50)
    d = d.strftime("%d/%m/%Y")
    d2 = d2.strftime("%d/%m/%Y")

    payload_stock_price = json.dumps({
        "operationName": "stockPrice",
        "variables": {
            "symbol": symbol,
            "offset": 1,
            "size": 50,
            "fromDate": d2,
            "toDate": d
        },
        "query": "query stockPrice($symbol: String!, $size: Int, $offset: Int, $fromDate: String, $toDate: String) {"
                 "\n  stockPrice(\n    symbol: $symbol\n    size: $size\n    offset: $offset\n    fromDate: "
                 "$fromDate\n    toDate: $toDate\n  )\n}\n"
    })

    payload_company_profile = json.dumps({
        "operationName": "companyProfile",
        "variables": {
            "symbol": symbol,
            "language": "vn"
        },
        "query": "query companyProfile($symbol: String!, $language: String) {\n  companyProfile(symbol: $symbol, "
                 "language: $language) {\n    symbol\n    subsectorcode\n    industryname\n    supersector\n    "
                 "sector\n    subsector\n    foundingdate\n    chartercapital\n    numberofemployee\n    "
                 "banknumberofbranch\n    companyprofile\n    listingdate\n    exchange\n    firstprice\n    "
                 "issueshare\n    listedvalue\n    companyname\n    __typename\n  }\n  companyStatistics(symbol: "
                 "$symbol) {\n    symbol\n    ttmtype\n    marketcap\n    sharesoutstanding\n    bv\n    beta\n    "
                 "eps\n    dilutedeps\n    pe\n    pb\n    dividendyield\n    totalrevenue\n    profit\n    asset\n   "
                 " roe\n    roa\n    npl\n    financialleverage\n    __typename\n  }\n}\n"
    })

    payload_similar_industry_companies = json.dumps({
        "operationName": "similarIndustryCompanies",
        "variables": {
            "symbol": symbol,
            "language": "vn",
            "offset": 1,
            "size": 100
        },
        "query": "query similarIndustryCompanies($symbol: String!, $size: Int, $offset: Int, $language: String) {\n  "
                 "similarIndustryCompanies(\n    symbol: $symbol\n    size: $size\n    offset: $offset\n    language: "
                 "$language\n  )\n}\n"
    })

    return payload_sub_companies, payload_shareholders, payload_leaderships, payload_stock_price, \
        payload_company_profile, payload_similar_industry_companies


def save_sub_companies(payload):
    response = requests.request("POST", url, headers=headers, data=payload)
    if response.status_code == 200:
        data = response.json()
        lst = data["data"]["subCompanies"]["datas"]
        for company in lst:
            filter_query = {'childcompanyname': company['childcompanyname']}
            update_data = {'$set': SubCompany(**company).dict()}
            collection_subCompanies.update_one(filter_query, update_data, upsert=True)
    else:
        print('Request failed with status code:', response.status_code)


def save_leaderships(payload):
    response = requests.request("POST", url, headers=headers, data=payload)
    if response.status_code == 200:
        data = response.json()
        lst = data["data"]["leaderships"]["datas"]
        for leadership in lst:
            filter_query = {'fullname': leadership['fullname']}
            update_data = {'$set': Leadership(**leadership).dict()}
            collection_leadership.update_one(filter_query, update_data, upsert=True)
    else:
        print('Request failed with status code:', response.status_code)


def save_shareholders(payload, symbol):
    response = requests.request("POST", url, headers=headers, data=payload)
    if response.status_code == 200:
        data = response.json()
        lst = data["data"]["shareholders"]["dataList"]
        for shareholder in lst:
            s = Shareholder(**shareholder)
            s.company = symbol
            filter_query = {'name': shareholder['name'], 'company': symbol}
            update_data = {'$set': s.dict()}
            collection_shareholder.update_one(filter_query, update_data, upsert=True)
    else:
        print('Request failed with status code:', response.status_code)


def save_stock_price(payload):
    response = requests.request("POST", url, headers=headers, data=payload)
    if response.status_code == 200:
        data = response.json()
        lst = data["data"]["stockPrice"]["dataList"]
        for price in lst:
            filter_query = {'tradingdate': price['tradingdate'], 'symbol': price['symbol']}
            update_data = {'$set': StockPrice(**price).dict()}
            collection_stockPrice.update_one(filter_query, update_data, upsert=True)
    else:
        print('Request failed with status code:', response.status_code)


def save_company_profile(payload):
    response = requests.request("POST", url, headers=headers, data=payload)
    if response.status_code == 200:
        data = response.json()
        p = data["data"]["companyProfile"]
        s = data["data"]["companyStatistics"]
        profile = CompanyProfile(**p)
        soup = BeautifulSoup(profile.companyprofile, 'html.parser')
        div_text = soup.div.get_text()
        profile.companyprofile = div_text.strip()
        filter_query = {'symbol': p['symbol']}
        update_data = {'$set': profile.dict()}
        collection_companyProfile.update_one(filter_query, update_data, upsert=True)

        stat = CompanyStatistics(**s)
        filter_query = {'symbol': s['symbol']}
        update_data = {'$set': stat.dict()}
        collection_companyStat.update_one(filter_query, update_data, upsert=True)

    else:
        print('Request failed with status code:', response.status_code)


def save_similar_industry_companies(payload, symbol):
    response = requests.request("POST", url, headers=headers, data=payload)
    if response.status_code == 200:
        data = response.json()
        lst = data["data"]["similarIndustryCompanies"]["dataList"]
        for company in lst:
            c = SimilarIndustryCompany(**company)
            c.relatingcompany = symbol
            filter_query = {'symbol': company['symbol'], 'relatingcompany': symbol}
            update_data = {'$set': c.dict()}
            collection_similarIndustryCompanies.update_one(filter_query, update_data, upsert=True)
    else:
        print('Request failed with status code:', response.status_code)


@api_router.get("/stock")
async def save_stock_info(symbol: Optional[str] = "ACB"):
    payload_sub_companies, payload_shareholders, payload_leaderships, payload_stock_price, \
        payload_company_profile, payload_similar_industry_companies = parseSymbol(symbol)

    save_sub_companies(payload_sub_companies)
    save_leaderships(payload_leaderships)
    save_company_profile(payload_company_profile)
    save_similar_industry_companies(payload_similar_industry_companies, symbol)
    save_stock_price(payload_stock_price)
    save_shareholders(payload_shareholders, symbol)

    return f'Saved stock: {symbol}'


@api_router.post("/stock")
async def get_stock_info(symbols: SymbolList):
    for s in symbols.symbols:
        payload_sub_companies, payload_shareholders, payload_leaderships, payload_stock_price, \
            payload_company_profile, payload_similar_industry_companies = parseSymbol(s)

        save_sub_companies(payload_sub_companies)
        save_leaderships(payload_leaderships)
        save_company_profile(payload_company_profile)
        save_similar_industry_companies(payload_similar_industry_companies, s)
        save_stock_price(payload_stock_price)
        save_shareholders(payload_shareholders, s)

    return f'Saved + {str(symbols.symbols)}'


@api_router.get("/stock_info/{symbol}")
async def get_stock_info(symbol):
    shareholders = []
    sm_companies = []
    leaderships = []
    company_profile_data = collection_companyProfile.find_one({'symbol': symbol}, {'_id': 0})
    company_stat_data = collection_companyStat.find_one({'symbol': symbol}, {'_id': 0})

    for s in collection_shareholder.find({'company': symbol}, {'_id': 0}):
        shareholders.append(s)
    for c in collection_similarIndustryCompanies.find({'relatingcompany': symbol}, {'_id': 0}):
        sm_companies.append(c)
    for l in collection_leadership.find({'symbol': symbol}, {'_id': 0}):
        leaderships.append(l)

    resp = {
        'symbol': symbol,
        'profile': company_profile_data,
        'stat': company_stat_data,
        'similar_industry_companies': sm_companies,
        'leaderships': leaderships,
        'shareholders': shareholders
    }
    return {'data': resp}


@api_router.get("/trading_history/{symbol}")
async def get_trading_history(symbol):
    stock_price = []
    for s in collection_stockPrice.find({'symbol': symbol}, {'_id': 0}):
        stock_price.append(s)
    resp = {
        'symbol': symbol,
        'stock_price': stock_price
    }
    return {'data': resp}


def get_third_thursday(year, month):
    first_day = date(year, month, 1)
    weekday = first_day.weekday()
    days_to_thursday = (3 - weekday + 7) % 7
    third_thursday = first_day + timedelta(days=days_to_thursday + 7 * 2)
    return third_thursday


def get_quarter(month):
    if month in range(1, 4):
        return 0
    elif month in range(4, 7):
        return 1
    elif month in range(7, 10):
        return 2
    elif month in range(10, 13):
        return 3


def is_valid_date(year, month, day):
    try:
        date(year, month, day)
        return True
    except ValueError:
        return False


@api_router.post("/derivative_code")
async def get_trading_history(date_req: Date):
    year = int(date_req.year)
    month = int(date_req.month)
    day = int(date_req.day)
    valid = is_valid_date(year, month, day)
    if not valid:
        return {"error": "Invalid date"}

    date_input = date(year, month, day)
    last_thursday_in_year = get_third_thursday(date_req.year, 12)

    if date_input > last_thursday_in_year:
        day = 1
        month = 1
        year += 1

    str_month_year = date_input.strftime("%y%m")
    symbol = f'VN30F{str_month_year}'

    this_month_dl = get_third_thursday(year, month)
    if date_input >= this_month_dl:
        month += 1
        this_month_dl = get_third_thursday(year, month)
    this_quarter = get_quarter(month)
    this_quarter_dl = get_third_thursday(year, quarters[this_quarter])

    next_month_dl = None
    next_quarter_dl = None
    if month == 12 or (month == 12 and this_quarter == 3):
        next_month_dl = get_third_thursday(year, 1)
        next_quarter_dl = get_third_thursday(year + 1, quarters[0])
    elif 10 <= month <= 12:
        next_month_dl = get_third_thursday(year, int(month) + 1)
        next_quarter_dl = get_third_thursday(year + 1, quarters[0])
    else:
        next_month_dl = get_third_thursday(year, int(month) + 1)
        next_quarter_dl = get_third_thursday(year, quarters[this_quarter + 1])

    resp = {"data": [
        {
            "symbol": symbol,
            "code": "VN30F1M",
            "expired_date": this_month_dl.strftime("%d/%m/%Y")
        },
        {
            "symbol": symbol,
            "code": "VN30F2M",
            "expired_date": next_month_dl.strftime("%d/%m/%Y")
        },
        {
            "symbol": symbol,
            "code": "VN30F1Q",
            "expired_date": this_quarter_dl.strftime("%d/%m/%Y")
        },
        {
            "symbol": symbol,
            "code": "VN30F2Q",
            "expired_date": next_quarter_dl.strftime("%d/%m/%Y")
        },
    ]}

    return resp




