import json

EUR_FILE = 'eur-gbp-2001.json'
GBP_FILE = 'gbp-eur-2001.json'

def get_forex_data(file_name):
    with open(file_name, 'r') as file:
        eur_data = json.load(file)["Time Series FX (Daily)"]

    euro_daily = []

    for day in sorted(eur_data):
        euro_daily.append((day, eur_data[day]["4. close"]))

    return euro_daily


class SMA_val:
    def __init__(self, name):
        self.name = name
        self.days = 0
        self.daily_values = []

    def add_daily_quote(self, today_val):
        self.daily_values.append(today_val)
        self.days = self.days + 1

    def current_sma(self):
        if len(self.daily_values) == 0:
            print("no values to calculate sma")
            return 0
        return reduce((lambda x, y: x + y), self.daily_values) / self.days


if __name__ == "__main__":
    tuple_date_eurval = get_forex_data(EUR_FILE)
    tuple_date_gbpval = get_forex_data(GBP_FILE)

    DAY = 1
    euro = SMA_val("eur")
    gbp = SMA_val("gbp")

    while True:
        # something
    
