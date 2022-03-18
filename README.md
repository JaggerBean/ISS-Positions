# ISS Positional Data
## What is this repo about?
This repo contains files to make your own docker image and flask server. The server takes curl requests from a user and reports back information from XML data. All of the options are as follows:

        ### ISS TRACKER ###

    Informational and management routes:

    / (GET) print this information
    /read_data (post) reset data, load from file

    Routes for querying positional and velocity data:

    /epochs (GET) list all epochs
    /epochs/<epoch> (GET) info on a specific epoch

    Routes for querying sighting data:

    /countries (GET) List of all countries
    /countries/<country> (GET) All data associated with <country>
    /countries/<country>/regions (GET) List of all regions
    /countries/<country>/regions/<region> (GET) All data associated with <region>
    /countries/<country>/regions/<region>/cities (GET) List of all cities
    /countries/<country>/regions/<region>/cities/<city> (GET) All data associated with <city>

## How to download the original data.
-   The ISS positional data set  [found here](https://data.nasa.gov/Space-Science/ISS_COORDS_2022-02-13/r6u8-bhhq), under the link ‘Public Distribution File’. Use the XML version
    
-   One of the 18 sighting data sets,  [also found here](https://data.nasa.gov/Space-Science/ISS_COORDS_2022-02-13/r6u8-bhhq)  under various names. **This repo uses the XMLsightingData_citiesINT02 file exclusively.**

## How to build your own docker container.
**If you would like to use my docker container please skip this step.**
Execute the following commands:

    docker build -t <your_name>/<program_name>:<version_num> .
**DONT FORGET THE " . "**
    
    docker run --name "<program_name>" -p 5002:5000 <your_name>/<program_name>:<version_num>
    
anything in <> is your choice but make sure that they match.
## If you would like to use my container instead.
simply run the Makefile by running this in your terminal:

    make run

if you would like to manually run the docker container, in your terminal run:

    docker pull jaggerbean/iss-data:1.0
This command will pull version 1.0 of my docker image to your current directory from docker hub. Then you will need to run the docker container by running:

    docker run --name "iss-data" -p <PORt_NUMBER>:5000 jaggerbean/iss-data:1.0
Anything in <> is your choice.

## Testing the container
After you have constructed your docker container, test it by running:

    docker run -it --rm <jaggerbean/iss-data:1.0> test_app.py
If you built your own container, replace the part in <> to match your container.

## How to interact with the server once it is running
you will interact through the server using curl requests. all of the options are listed at the top of the readme but an example would be:

    [jagger@isp02 midterm]$ curl localhost:5002/epochs/2022-057T09:52:56.869Z
    [
      {
        "EPOCH": "2022-057T09:52:56.869Z",
        "X": {
          "#text": "-4157.6226642798401",
          "@units": "km"
        },
        "X_DOT": {
          "#text": "5.8553914186678702",
          "@units": "km/s"
        },
        "Y": {
          "#text": "-2682.9438646285198",
          "@units": "km"
        },
        "Y_DOT": {
          "#text": "-3.9846935694505698",
          "@units": "km/s"
        },
        "Z": {
          "#text": "4651.3777791075099",
          "@units": "km"
        },
        "Z_DOT": {
          "#text": "2.9234153028502798",
          "@units": "km/s"
        }
      }

    ]

## What does it all mean?
Any curl request that has an endpoint of a variable that you decided will return .json data that is narrowed down to the variable that you selected. Any curl request that ends with a predetermined command will return all of the options that fit the predetermined command in a list. For example if the curl request ends with `/regions`, then the server will return a list of all of the regions it can find.
 
 User selected variable:

     curl localhost:5002/countries/Canada/regions/Quebec/cities/Mobile_Servicing_System_Operations_Complex_Saint_Hubert
        [
          {
            "city": "Mobile_Servicing_System_Operations_Complex_Saint_Hubert",
            "country": "Canada",
            "duration_minutes": "2",
            "enters": "10 above SSE",
            "exits": "10 above ESE",
            "max_elevation": "11",
            "region": "Quebec",
            "sighting_date": "Thu Feb 17/05:43 AM",
            "spacecraft": "ISS",
            "utc_date": "Feb 17, 2022",
            "utc_offset": "-5.0",
            "utc_time": "10:43"
          },
          {
            "city": "Mobile_Servicing_System_Operations_Complex_Saint_Hubert",
            "country": "Canada",
            "duration_minutes": "6",
            "enters": "10 above SSW",
            "exits": "10 above E",
            "max_elevation": "28",
            "region": "Quebec",
            "sighting_date": "Sat Feb 19/05:41 AM",
            "spacecraft": "ISS",
            "utc_date": "Feb 19, 2022",
            "utc_offset": "-5.0",
            "utc_time": "10:41"
          },

Predetermined command:

    [jagger@isp02 midterm]$ curl localhost:5002/countries/Canada/regions
    [
      "Quebec",
      "Saskatchewan",
      "Yukon_Territory"
    ]

# Citation
All data used and provided in this repo is from NASA and can be found [here](https://data.nasa.gov/Space-Science/ISS_COORDS_2022-02-13/r6u8-bhhq).
