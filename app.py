import json
import datetime
import yfinance as ticker_data

# Nifty 100 టాప్ స్టాక్స్ లిస్ట్
STOCKS = [
    "RELIANCE.NS", "TCS.NS", "HDFCBANK.NS", "BHARTIARTL.NS", "ICICIBANK.NS",
    "INFY.NS", "SBIN.NS", "TATAMOTORS.NS", "LTIM.NS", "AXISBANK.NS",
    "TATASTEEL.NS", "JIOFIN.NS", "ITC.NS", "HINDUNILVR.NS", "LT.NS"
]

def scan_markets():
    matched_stocks = []
    print("Scanning started...")

    for symbol in STOCKS:
        try:
            stock = ticker_data.Ticker(symbol)
            # గత 100 రోజుల డేటా డౌన్లోడ్ చేస్తున్నాం
            df = stock.history(period="100d")
            
            if len(df) < 50:
                continue
                
            close_prices = df['Close']
            volumes = df['Volume']
            
            # EMA లెక్కింపు
            ema21 = close_prices.ewm(span=21, adjust=False).mean()
            ema50 = close_prices.ewm(span=50, adjust=False).mean()
            
            current_price = close_prices.iloc[-1]
            last_ema21 = ema21.iloc[-1]
            last_ema50 = ema50.iloc[-1]
            
            # వాల్యూమ్ కండిషన్
            avg_volume = volumes.iloc[-6:-1].mean()
            current_volume = volumes.iloc[-1]
            
            # --- నీ 5 కండిషన్స్ చెకింగ్ ---
            if current_price > last_ema21 and current_price > last_ema50 and last_ema21 > last_ema50 and current_volume > avg_volume:
                
                stock_clean_name = symbol.replace(".NS", "")
                
                matched_stocks.append({
                    "name": stock_clean_name,
                    "price": round(current_price, 2),
                    "news": f"{stock_clean_name} లో బలమైన బుల్లిష్ రివర్సల్ మరియు బ్రేక్ అవుట్ సంకేతాలు కనిపిస్తున్నాయి.",
                    "ema_status": f"Price ({round(current_price,2)}) is above 21 EMA ({round(last_ema21,2)}) & 50 EMA ({round(last_ema50,2)})",
                    "volume_status": f"High Volume Detected! Today: {int(current_volume)} | Avg: {int(avg_volume)}"
                })
                print(f"✓ Found Match: {stock_clean_name}")
                
        except Exception as e:
            print(f"Error scanning {symbol}: {e}")

    # ఫలితాలను JSON ఫైల్ రూపంలో సేవ్ చేస్తాము
    output_data = {
        "last_updated": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "stocks": matched_stocks
    }
    
    with open('data.json', 'w') as f:
        json.dump(output_data, f, indent=4)
    print("Scan completed. data.json updated.")

if __name__ == "__main__":
    scan_markets()
