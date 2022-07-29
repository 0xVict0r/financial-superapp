from fastapi import FastAPI
from stock_valuation.valuation_functions import get_valuation

app = FastAPI()


@app.get("/")
def home():
    return "This is the Financial SuperApp API tool. Navigate to /docs to read the documentation."


@app.get("/get-stock-valuation/{ticker}")
def get_stock_valuation(ticker: str):
    valuation = get_valuation(ticker, False)[0]
    return {"currentStockValuation": valuation}
