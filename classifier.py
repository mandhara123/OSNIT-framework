def classify_financial_attack(text):

    text = text.lower()

    # ---- FOREX SCAMS ----
    if "forex" in text and ("scam" in text or "fraud" in text or "fake" in text):
        return "Forex Scam"

    # ---- BROKER ACCOUNT TAKEOVER ----
    if "broker" in text and ("hack" in text or "breach" in text or "compromise" in text):
        return "Broker Account Takeover"

    # ---- MARKET MANIPULATION ----
    if "manipulation" in text or "pump" in text or "spoof" in text:
        return "Market Manipulation"

    # ---- TRADING PLATFORM EXPLOIT ----
    if ("trading" in text or "exchange" in text or "platform" in text) and \
       ("exploit" in text or "vulnerability" in text or "zero-day" in text):
        return "Trading Platform Exploit"

    # ---- FINANCIAL MALWARE ----
    if "bank" in text or "wallet" in text or "financial" in text:
        if "malware" in text or "trojan" in text or "stealer" in text:
            return "Financial Malware"

    # ---- DEFAULT ----
    return None
