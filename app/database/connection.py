from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["calendar"]
collection_holidays = db["holiday"]
ssi_db = client["SSI"]
collection_companyProfile = ssi_db["companyProfile"]
collection_companyStat = ssi_db["companyStat"]
collection_shareholder = ssi_db["shareholder"]
collection_leadership = ssi_db["leadership"]
collection_similarIndustryCompanies = ssi_db["similarIndustryCompanies"]
collection_subCompanies = ssi_db["subCompanies"]
collection_stockPrice = ssi_db["stockPrice"]
