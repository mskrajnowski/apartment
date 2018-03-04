from urllib.parse import urlencode


base_search = 'https://www.otodom.pl/sprzedaz/mieszkanie/'

def search(
    page=1,
    results_per_page=24,
    min_price=None,
    max_price=None,
    min_meter_price=None,
    max_meter_price=None,
    min_area=None,
    max_area=None,
    min_year=None,
    max_year=None,
    rooms=None,
    markets=None,
    created_since_days=None,
):
    params = {
        'search[filter_float_price:from]': min_price,
        'search[filter_float_price:to]': max_price,
        'search[filter_float_price_per_m:from]': min_meter_price,
        'search[filter_float_price_per_m:to]': max_meter_price,
        'search[filter_float_m:from]': min_area,
        'search[filter_float_m:to]': max_area,
        'search[filter_float_build_year:from]': min_year,
        'search[filter_float_build_year:to]': max_year,
        'search[created_since]': created_since_days,
    }

    params = {
        key: value
        for key, value in params.items()
        if value is not None
    }

    if rooms:
        params.update({
            f'search[filter_enum_rooms_num][{i}]': value
            for i, value in enumerate(rooms)
        })

    if markets:
        params.update({
            f'search[filter_enum_market][{i}]': value
            for i, value in enumerate(markets)
        })

    return base_search + '?' + urlencode(params)
