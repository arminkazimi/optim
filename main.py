import logging
from argparse import ArgumentParser
from data_generator.solar_generator import SolarGenerator
from data_generator.wind_generator import WindGenerator
import geocoder
import json

def main():
    f = open('config/config.json', )
    config = json.load(f)
    f.close()
    parser = ArgumentParser()
    parser.add_argument("-c", "--config", dest="config_file",
                        help="Config file", metavar="FILE")
    args = parser.parse_args()
    print(args.config_file)
    if config['location'] and not config['lat'] and not config['long']:
        print('search Lat and Long with "location"')
        location = config['location']
        g = geocoder.arcgis(location).json
        latitude = g['lat']
        longitude = g['lng']
    elif config['lat'] and config['long']:
        latitude = float(config['lat'])
        longitude = float(config['long'])
    from_date = config['from_date']
    to_date = config['to_date']
    resolution = config['resolution']
    solar = SolarGenerator(from_date, to_date, latitude, longitude, resolution)
    wind = WindGenerator(from_date, to_date, latitude, longitude, resolution)
    solar_data = solar.generator()
    wind_data = wind.generator()
    print('solar_data: ', solar_data)
    print('wind_data: ', wind_data['wspd'])

if __name__ == '__main__':
    main()
