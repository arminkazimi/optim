import json
import geocoder
from argparse import ArgumentParser
from investigator import Investigator


def main():
    f = open('config/config.json', )
    config = json.load(f)
    f.close()
    parser = ArgumentParser()
    parser.add_argument("-c", "--config", dest="config_file",
                        help="Config file", metavar="FILE")
    args = parser.parse_args()
    investigator = Investigator(args.config_file)
    investigator.start()
    # if config['location'] and not config['lat'] and not config['long']:
    #     print('search Lat and Long with "location"')
    #     location = config['location']
    #     g = geocoder.arcgis(location).json
    #     latitude = g['lat']
    #     longitude = g['lng']
    # elif config['lat'] and config['long']:
    #     latitude = float(config['lat'])
    #     longitude = float(config['long'])
    from_date = config['from_date']
    to_date = config['to_date']
    resolution = config['resolution']



if __name__ == '__main__':
    main()
