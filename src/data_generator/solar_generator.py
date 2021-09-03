import pandas as pd
from astral.sun import sun
from astral import LocationInfo
from datetime import datetime, timedelta, time, date


class SolarGenerator:
    def __init__(self, from_date, to_date, lat, long, resolution):
        self.from_date = datetime.strptime(from_date, '%Y-%m-%d %H:%M:%S')
        self.to_date = datetime.strptime(to_date, '%Y-%m-%d %H:%M:%S')
        self.lat = lat
        self.long = long
        self.resolution = resolution

    def generator(self):
        city = LocationInfo(latitude=self.lat, longitude=self.long)
        if self.resolution == '1hour':
            delta = timedelta(hours=1)

        if self.resolution == '1day':
            delta = timedelta(days=1)

        df = pd.DataFrame(columns=['datetime', 'sunrise', 'noon', 'sunset'])
        datetime_list = list()
        sunrise_list = list()
        noon_list = list()
        sunset_list = list()
        while self.from_date <= self.to_date:
            s = sun(city.observer,
                    date=date(self.from_date.year, self.from_date.month, self.from_date.day))
            datetime_list.append(self.from_date.strftime('%Y-%m-%d %H:%M:%S'))
            sunrise_list.append(s['sunrise'])
            noon_list.append(s['noon'])
            sunset_list.append(s['sunset'])
            self.from_date += delta

        df.datetime = datetime_list
        df.sunrise = sunrise_list
        df.noon = noon_list
        df.sunset = sunset_list
        return df
