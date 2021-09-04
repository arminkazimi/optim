import json
import geocoder
import pandas as pd
from optimizer.power_grid_oprimizer import PowerGridOptimizer
from optimizer.wind_solar_optimizer import WindSolarOptimizer
from data_generator.solar_generator import SolarGenerator
from data_generator.wind_generator import WindGenerator


class Investigator:

    def __init__(self, config_file):
        with open(config_file) as json_config_file:
            self.params = json.load(json_config_file)
        self._base_path = self.params['base_path']
        self.location = self.params['location']
        self.from_date = self.params['from_date']
        self.to_date = self.params['to_date']
        self.lat = self.params['lat']
        self.long = self.params['long']
        self.from_date = self.params['from_date']
        self.to_date = self.params['to_date']
        self.resolution = self.params['resolution']
        self.problems = self.params['problems']

    def start(self):
        for problem in self.problems:
            if problem['name'] == 'power_grid_optimization':
                df = pd.read_csv(problem['data_path'])
                df = df.rename(columns={'consumption': 'demand'})
                power_grid_problem = PowerGridOptimizer(df, problem)
                result = power_grid_problem.optimizer()
                df.x = result['x']
                df.battery_usage = result['battery']
                file_name = 'power_grid_result.csv'
                df.to_csv(self.params['base_path'] + file_name)

            if problem['name'] == 'solar_wind_sizing':
                if problem['lat'] is None or problem['long'] is None:
                    g = geocoder.arcgis(problem['location']).json
                    problem['lat'] = g['lat']
                    problem['long'] = g['lng']
                # print(problem['lat'], problem['long'])

                solar = SolarGenerator(problem['from_date'], problem['to_date'], problem['lat'],
                                       problem['long'], problem['resolution'])
                wind = WindGenerator(problem['from_date'], problem['to_date'], problem['lat'],
                                     problem['long'], problem['resolution'])
                solar_data = solar.generator()
                wind_data = wind.generator()
                df = pd.read_csv(problem['data_path'], usecols=['demand'])
                df = df.iloc[:len(solar_data)]
                df['solar_power'] = solar_data.solar_index.values
                df['wind_power'] = wind_data.wspd.values
                df['battery'] = [f'b{i}' for i in df.iterrows()]
                df['s'] = [f's{i}' for i in df.iterrows()]
                df['w'] = [f'w{i}' for i in df.iterrows()]

                solar_wind_sizing = WindSolarOptimizer(df, problem['battery_max_capacity'], problem['battery_0'],
                                                       problem['eps'], problem['solar_cost'],
                                                       problem['wind_cost'])
                solar_wind_sizing.optimizer()
                # print('solar_data: ', solar_data.solar_index.values)
                # print('wind_data: ', wind_data['wspd'].iloc[48:72])
