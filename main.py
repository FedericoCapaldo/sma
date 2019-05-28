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
        self.daily_values = []

    def get_current_price(self):
        return float(self.daily_values[-1][1])

    def add_daily_quote(self, today_val):
        self.daily_values.append(today_val)

    def sma_50(self):
        if len(self.daily_values) == 0:
            print("no values to calculate sma")
            return 0
        elif len(self.daily_values) < 50:
            print("no enough values to calculate sma")
            return 0

        return reduce((lambda x, y: x + y), map((lambda x: float(x[1])),self.daily_values[-50:])) / 50

    def sma_20(self):
        if len(self.daily_values) == 0:
            print("no values to calculate sma")
            return 0
        elif len(self.daily_values) < 20:
            print("no enough values to calculate sma")
            return 0

        return reduce((lambda x, y: x + y), map((lambda x: float(x[1])),self.daily_values[-20:])) / 20


def is_moving_average_below(currency):
    return currency.sma_20() < currency.sma_50()


def sell(position, money, eur, gbp):
    if position == eur.name:
        return money * gbp.get_current_price()
    elif position == gbp.name:
        return money * eur.get_current_price()


if __name__ == "__main__":
    eur_vals = get_forex_data(EUR_FILE)
    gbp_vals = get_forex_data(GBP_FILE)

    MONEY = 1000
    DAY = 0
    eur = SMA_val("eur")
    gbp = SMA_val("gbp")

    position = "gbp"

    while True:
        eur.add_daily_quote(eur_vals[DAY])
        gbp.add_daily_quote(gbp_vals[DAY])
        DAY += 1
        if DAY < 50:
            continue

        if position == "gbp":
            if is_moving_average_below(gbp):
                MONEY = sell(position, MONEY, eur, gbp)
                position = "eur"
            # else:
                # nothing for now
        elif position == "eur":
            if is_moving_average_below(eur):
                MONEY = sell(position, MONEY, eur, gbp)
                position = "gbp"
            # else:
                # nothing for now

        if DAY > 3000 and position == "gbp":
            print(MONEY)
            print(DAY)
            break
