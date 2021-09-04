import pytz
import pandas as pd
from astral.sun import sun
from timezonefinder import TimezoneFinder
from astral import LocationInfo
from datetime import datetime, timedelta, time, date


class SolarGenerator:

    def __init__(self, from_date, to_date, lat, long, resolution):
        self.from_date = datetime.strptime(from_date, '%Y-%m-%d %H:%M:%S')
        self.to_date = datetime.strptime(to_date, '%Y-%m-%d %H:%M:%S')
        self.lat = lat
        self.long = long
        self.resolution = resolution
        tf = TimezoneFinder()
        self.timezone = pytz.timezone(tf.timezone_at(lng=self.long, lat=self.lat))


    def generator(self):
        print('time zone is: ', self.timezone)
        self.from_date = self.timezone.localize(self.from_date)
        self.to_date = self.timezone.localize(self.to_date)
        city = LocationInfo(latitude=self.lat, longitude=self.long)
        if self.resolution == '1hour':
            delta = timedelta(hours=1)

        if self.resolution == '1day':
            delta = timedelta(days=1)

        df = pd.DataFrame(columns=['datetime', 'sunrise', 'noon', 'sunset', 'solar_index'])
        datetime_list = list()
        sunrise_list = list()
        noon_list = list()
        sunset_list = list()
        solar_index_list = list()
        solar_index = 0
        while self.from_date <= self.to_date:
            s = sun(city.observer,
                    date=date(self.from_date.year, self.from_date.month, self.from_date.day))
            datetime_list.append(self.from_date.strftime('%Y-%m-%d %H:%M:%S'))
            sunrise_list.append(s['sunrise'])
            noon_list.append(s['noon'])
            sunset_list.append(s['sunset'])
            if self.resolution == '1hour':
                if s['sunrise'] <= self.from_date <= s['noon']:
                    solar_index += 0.05
                elif s['noon'] <= self.from_date <= s['sunset']:
                    solar_index -= 0.05
                    if solar_index <= 0.001:
                        solar_index = 0.05
                else:
                    solar_index = 0

                solar_index_list.append(solar_index)
            self.from_date += delta

        df.solar_index = [item*5.5*60*16.67/1000 for item in solar_index_list]

        df.datetime = datetime_list
        df.sunrise = sunrise_list
        df.noon = noon_list
        df.sunset = sunset_list
        return df
