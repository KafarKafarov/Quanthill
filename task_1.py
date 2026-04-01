def find_best_days(prices) -> tuple[int, int]:
    if len(prices) < 2:
        return 0, 0

    min_price = prices[0]
    min_price_day = 1

    best_profit = 0
    best_buy_day = 0
    best_sell_day = 0

    for day_index in range(1, len(prices)):
        current_price = prices[day_index]
        current_day = day_index + 1

        current_profit = current_price - min_price
        if current_profit > best_profit:
            best_profit = current_profit
            best_buy_day = min_price_day
            best_sell_day = current_day

        if current_price < min_price:
            min_price = current_price
            min_price_day = current_day

    return best_buy_day, best_sell_day


def parse_prices(line: str) -> list[int]:
   return [
       int(part.strip())
       for part in line.split(",")
   ]


def main() -> None:
    days_count = int(input().strip())
    prices = parse_prices(input().strip())

    if len(prices) != days_count:
        raise ValueError(
            f"Ожидалось {days_count} цен, получено {len(prices)}"
        )

    buy_day, sell_day = find_best_days(prices)
    print(f"{buy_day},{sell_day}")


if __name__ == "__main__":
    main()