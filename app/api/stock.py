from fastapi import APIRouter
import requests
from datetime import date, timedelta
from typing import Optional
from ..database.connection import *
from ..model.stock import *
import json

api_router = APIRouter()
url = "https://finfo-iboard.ssi.com.vn/graphql"

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
async def get_stock_info(symbol: Optional[str] = "ACB"):
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
