import json
import pandas as pd
from optimizer.power_grid_oprimizer import PowerGridOptimizer
from optimizer.wind_solar_optimizer import WindSolarOptimizer


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
            if problem['name'] == 'power_grid_problem':
                df = pd.read_csv(problem['data_path'])
                df = df.rename(columns={'consumption': 'demand'})
                power_grid_problem = PowerGridOptimizer(df, problem)
                result = power_grid_problem.optimizer()
                df.x = result['x']
                df.battery_usage = result['battery']
                file_name = 'power_grid_result.csv'
                df.to_csv(self.params['base_path']+file_name)
