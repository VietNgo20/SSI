import typing

from pydantic import BaseModel


class SymbolList(BaseModel):
    symbols: list[str]


class CompanyProfile(BaseModel):
    symbol: str
    subsectorcode: str
    industryname: str
    supersector: str
    sector: str
    subsector: str
    foundingdate: str
    chartercapital: str
    numberofemployee: str
    banknumberofbranch: str
    companyprofile: str
    listingdate: str
    exchange: str
    firstprice: str
    issueshare: str
    listedvalue: str
    companyname: str


class CompanyStatistics(BaseModel):
    symbol: str
    ttmtype: str
    marketcap: str
    sharesoutstanding: str
    bv: str
    beta: str
    eps: str
    dilutedeps: str
    pe: str
    pb: str
    dividendyield: str
    totalrevenue: str
    profit: str
    asset: str
    roe: str
    roa: str
    npl: str
    financialleverage: str


class SubCompany(BaseModel):
    parentsymbol: str
    parentcompanyname: str
    roleid: str
    childsymbol: str
    childcompanyname: str
    chartercapital: str
    percentage: str
    rolename: str


class SimilarIndustryCompany(BaseModel):
    relatingcompany: typing.Any
    symbol: str
    companyname: str
    currentprice: int
    pricechange: str
    perpricechange: str
    floorprice: str
    ceilingprice: str
    referenceprice: int
    exchange: str
    icblevel: str
    matchvolume: str


class Leadership(BaseModel):
    symbol: str
    fullname: str
    positionname: str
    positionlevel: str


class Shareholder(BaseModel):
    company: typing.Any
    symbol: str
    name: str
    quantity: str
    percentage: str
    publicdate: str
    ownershiptypecode: str
    type: str


class StockPrice(BaseModel):
    tradingdate: str
    pricechange: str
    perpricechange: str
    ceilingprice: str
    floorprice: str
    refprice: str
    openprice: str
    highestprice: str
    lowestprice: str
    closeprice: str
    averageprice: str
    closepriceadjusted: str
    totalmatchvol: str
    totalmatchval: str
    totaldealval: str
    totaldealvol: str
    foreignbuyvoltotal: str
    foreigncurrentroom: str
    foreignsellvoltotal: str
    foreignbuyvaltotal: str
    foreignsellvaltotal: str
    totalbuytrade: str
    totalbuytradevol: str
    totalselltrade: str
    totalselltradevol: str
    netbuysellvol: str
    netbuysellval: str
    exchange: str
    symbol: str
    foreignbuyvolmatched: str
    foreignbuyvoldeal: str

# class About(BaseModel):
#     symbol: str
#     company_profile: CompanyProfile
#     company_stats: CompanyStatistics
#     subcompanies: list[SubCompany]
#     similar_industry_companies: list[SimilarIndustryCompany]
#     leaderships: list[Leadership]
#     shareholder: list[Shareholder]
#     stock_price: list[StockPrice]
