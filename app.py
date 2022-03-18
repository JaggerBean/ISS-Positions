from flask import Flask, request, jsonify
import xmltodict
import sys
import logging
import socket

format_str=f'[%(asctime)s {socket.gethostname()}] %(filename)s:%(funcName)s:%(lineno)s - %(levelname)s: %(message)s'
logging.basicConfig(level=logging.DEBUG, format=format_str)

app = Flask(__name__)

iss_epoch_data = {}
iss_sighting_data = {}




@app.route('/', methods=['GET'])
def how_to():

    """
    Shows how to use the app to get the results you want.

    Returns: 
        string: all of the possible inputs that the server is looking for.
    """


    logging.debug('used GET to access "how_to"')

    return '\n\n	### ISS TRACKER ###\n\n    Informational and management routes:\n\n    / (GET) print this information\n    /read_data (post) reset data, load from file\n\n    Routes for querying positional and velocity data:\n\n    /epochs (GET) list all epochs\n    /epochs/<epoch> (GET) info on a specific epoch\n\n    Routes for querying sighting data:\n\n    /countries (GET) List of all countries\n    /countries/<country> (GET) All data associated with <country>\n    /countries/<country>/regions (GET) List of all regions\n    /countries/<country>/regions/<region> (GET) All data associated with <region>\n    /countries/<country>/regions/<region>/cities (GET) List of all cities\n    /countries/<country>/regions/<region>/cities/<city> (GET) All data associated with <city>\n\n'

@app.route('/read_data', methods=['POST'])
def read_data_from_file_into_dict():
    
    """
    Used to read in the data for later use with other functions. (Updates the list of data dictionaries)

    Returns:
        string: informing the user that the data is now available for use.
    """

    logging.debug('used POST to read in data')

    global iss_epoch_data
    global iss_sighting_data

    with open( 'ISS.OEM_J2K_EPH.xml' , 'r') as f:
        iss_epoch_data = xmltodict.parse(f.read())

    with open( 'XMLsightingData_citiesINT02.xml' , 'r') as f:
        iss_sighting_data = xmltodict.parse(f.read())

    return f'Data has been read from file\n'

# now iss_epoch_data and iss_sighting_data will be accessible to other functions


@app.route('/epochs', methods=['GET'])
def all_epochs():

    """
    All ISS epoch data.

    uses GET to request all possible epoch data.

    Returns:
        List: all epochs in the data set.
    """

    logging.debug('used GET to access all epoch data')

    epoch = []
    for row in iss_epoch_data['ndm']['oem']['body']['segment']['data']['stateVector']:
        epoch.append(row['EPOCH'])
    
    return jsonify(epoch)

@app.route('/epochs/<string:epoch>', methods=['GET'])
def one_epoch(epoch: str):
    

    """
    Single ISS epoch data.

    uses GET to request one epoch data set.

    INPUT:
        epoch <string>: the specific epoch that you would like data for.

    RETURNS:
        json data for the specific epoch queried.
    """

    logging.debug('used GET to access one epoch data')

    number = (f'{epoch}')
    epochs = []
    for row in iss_epoch_data['ndm']['oem']['body']['segment']['data']['stateVector']:
        if number == row['EPOCH']:
            epochs.append(row)
    return jsonify(epochs)


@app.route('/countries', methods=['GET'])
def countries():


    """
    All ISS Country data.

    uses GET to access all possible country data.

    Returns:
        list: all countries within the data set.
    """

    logging.debug('used GET to access all country data')

    country = []
 
    [country.append(row['country']) for row in iss_sighting_data['visible_passes']['visible_pass'] if row['country'] not in country]

    return jsonify(country)



@app.route('/countries/<string:country>', methods=['GET'])
def country(country:str):
    
    """
    Single ISS country data.

    uses GET to request one country data set.

    INPUT:
        country <string>: the specific country that you would like data for.
    
    RETURNS:
        json sighting data with matching queried country
    """

    logging.debug('used GET to access data from one country')

    country = f'{country}'
    countries = []
    for row in iss_sighting_data['visible_passes']['visible_pass']:
        if row['country'] == country:
            countries.append(row) 
    return jsonify(countries)



@app.route('/countries/<string:country>/regions', methods=['GET'])
def country_region(country:str):
    
    
    """
    All ISS region data.

    uses GET to request all regions within a country.

    INPUT:
        country <string>: the specific country that you would like data for.
    
    RETURNS:
        json data of all regions with matching queried country
    """

    logging.debug('used GET to access all region data within a specific country')

    country = f'{country}'
    countries = []
    regions = []
    for row in iss_sighting_data['visible_passes']['visible_pass']:
        if row['country'] == country:
            countries.append(row)
            
    for row in countries:
        if row['region'] not in regions:
            regions.append(row['region'])  
    return jsonify(regions)



@app.route('/countries/<string:country>/regions/<string:region>', methods=['GET'])
def region(country:str, region:str):
    

    """
    Single ISS region data.

    uses GET to request all data for a specific region within a country.

    INPUT:
        country <string>: the specific country that you would like data for.
        region <string>: the specific region that you would like data for.    

    RETURNS:
        json sighting data with matching queried country and region
    """

    logging.debug('used GET to access a specific region within a country')

    country = f'{country}'
    region = f'{region}'
    countries = []
    regions = []
    for row in iss_sighting_data['visible_passes']['visible_pass']:
        if row['country'] == country:
            countries.append(row)
            
    for row in countries:
        if row['region'] == region:
            regions.append(row)  
    

    return jsonify(regions)


@app.route('/countries/<string:country>/regions/<string:region>/cities', methods=['GET'])
def country_region_city(country:str, region:str):
    
    """
    All ISS city data.

    uses GET to request all of the cities withing a specific region of a country.

    INPUT:
        country <string>: the specific country that you would like data for.  
        region <string>: the specific region that you would like data for.  
  
    RETURNS:
        json data with all cities of a certain region of a country
    """

    logging.debug('used GET to access all city data within a specific region of a country')

    country = f'{country}'
    region = f'{region}'
    countries = []
    regions = []
    cities = []

    for row in iss_sighting_data['visible_passes']['visible_pass']:
        if row['country'] == country:
            countries.append(row)
            
    for row in countries:
        if row['region'] == region:
            regions.append(row)  
    
    for row in regions:
        if row['city'] not in cities:
            cities.append(row['city'])

    return jsonify(cities)



@app.route('/countries/<string:country>/regions/<string:region>/cities/<string:city>', methods=['GET'])
def city(country:str, region:str, city:str):


    """
    Single ISS city data.

    uses GET to request all data for a specific city of a region within a country.

    INPUT:
        country <string>: the specific country that you would like data for.
        region <string>: the specific region that you would like data for.    
        city <string>: the specific city that you would like data for.

    RETURNS:
        json sighting data with matching queried country, region, and city
    """
    

    logging.debug('used GET to access a specific city within a specific region of a country')

    country = f'{country}'
    region = f'{region}'
    city = f'{city}'
    countries = []
    regions = []
    cities = []

    for row in iss_sighting_data['visible_passes']['visible_pass']:
        if row['country'] == country:
            countries.append(row)
            
    for row in countries:
        if row['region'] == region:
            regions.append(row)  
    
    for row in regions:
        if row['city'] == city:
            cities.append(row)

    return jsonify(cities)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
