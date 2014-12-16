#!/usr/bin/env python
from __future__ import print_function, division
from datetime import datetime
from os import popen, listdir
from os.path import join, isfile, expanduser
import pytz
import yaml
from collections import OrderedDict

RAW_UKPD_DATA_PATH = "/data/mine/vadeec/merged"
OUTPUT_PATH = "."

TIMEZONE = "Europe/London"
TZ = pytz.timezone(TIMEZONE)
N_BULDINGS = 5

dataset = {
    "name": "UK-DALE",
    "long_name": "UK Domestic Appliance-Level Electricity",
    "subject": "Disaggregated domestic electricity demand",
    "geospatial_coverage": "Southern England",
    "publisher": "UK Energy Research Centre Energy Data Centre (UKERC EDC)",
    "related_documents": [
    (
        "Dataset is available for download from http://www.doc.ic.ac.uk/~dk3810/data/"
    ), 
    (
        "Dataset is also available from the UK Energy Research Council's"
        " Energy Data Centre: The 1-second data is available from"
        " http://data.ukedc.rl.ac.uk/cgi-bin/dataset_catalogue/view.cgi.py?id=19"
        " and the 6-second data is available from"
        " http://data.ukedc.rl.ac.uk/cgi-bin/dataset_catalogue/view.cgi.py?id=18"
        " but please note that this archive is updated less frequently than the"
        " data on www.doc.ic.ac.uk/~dk3810/data/"
    ),
    (
        "This research paper describes the data collection:"
        " http://arxiv.org/abs/1404.0284"
    ),
    (
        "The following poster describes the metering setup and provides some analyses:"
        " Jack Kelly and William Knottenbelt." 
        " Smart Meter Disaggregation: Data Collection & Analysis."
        " UK Energy Research Council Summer School Ph.D. poster session."
        " June 2013. PDF: http://www.doc.ic.ac.uk/~dk3810/writing/UKERC_poster2013_v2.pdf"
    ), 
    ], 
    "creators": ["Kelly, Jack"],
    "contact": "jack.kelly@imperial.ac.uk",
    "institution": "Imperial College London", 
    "description": (
        "Appliance-by-appliance and whole-home power demand for 5 UK homes."
        " Appliance power demand was recorded once every 6 seconds."
        " Whole-home power demand was recorded once every 6 seconds for all"
        " homes and additionally at 16kHz for homes 1, 2 and 5."
        " Detailed metadata is included."
    ),
    "number_of_buildings": N_BULDINGS,
    "geo_location": {
        "country": "GB", 
        "locality": "London",
        "latitude": 51.464462, 
        "longitude": -0.076544
    }, 
    "timezone": TIMEZONE,
    "schema": "https://github.com/nilmtk/nilm_metadata/tree/v0.2",
    "funding": [
        "Jack Kelly's PhD is funded by an EPSRC DTA", 
        "Hardware necessary for this project was funded from"
        " Jack Kelly's Intel EU PhD Fellowship"],
    "rights_list": [{
        "name": "Creative Commons Attribution 4.0 International (CC BY 4.0)",
        "uri": "http://creativecommons.org/licenses/by/4.0/"
    }],
    "description_of_subjects": "4 MSc students and 1 PhD student."
}

building_metadata = {
    1: {
        "rooms": [
            {"name": "lounge", "floor": 0},
            {"name": "hall", "instance": 1,  "floor": 0},
            {"name": "hall", "instance": 2,  "floor": 1},
            {"name": "kitchen", "floor": 0},
            {"name": "utility", "floor": 0},
            {"name": "dining room", "floor": 0},
            {"name": "bedroom", "instance": 1, "floor": 1, 
             "description": "master bedroom"},
            {"name": "bedroom", "instance": 2, "floor": 1, 
             "description": "kid's bedroom"},
            {"name": "study", "instance": 1, "floor": 1, 
             "description": "occasionally used as a spare bedroom "},
            {"name": "bathroom", "instance": 1, "floor": 1, 
             "description": "shower + bath + toilet + sink + cupboards "
             "+ hot water tank + boiler + solar thermal pumping station"}
        ],
        "description": "Some individual appliance meters are switched off from the socket for significant portions of time.  These include (using original names): laptop, kettle, toaster, lcd_office, hifi_office, livingroom_s_lamp, soldering_iron, gigE_&_USBhub, hoover, iPad_charger, utilityrm_lamp, hair_dryer, straighteners, iron, childs_ds_lamp, office_lamp3, office_pc, gigE_switch",
        "n_occupants": 4,
        "description_of_occupants": "2 adults and 1 dog started living in the house in 2006 (i.e. before the dataset started recording).  One child born 2011-08-27 and a second child born 2014-04-27.",
        "construction_year": 1905,
        "energy_improvements": ["solar thermal", "loft insulation", "solid wall insulation", "double glazing"],
        "heating": ["natural gas"],
        "building_type": "end of terrace",
        "ownership": "bought"
    },
    2: {
        "n_occupants": 2,
        "description_of_occupants": "2 adults, 1 at work all day, other sometimes home",
        "heating": ["natural gas"],
        "construction_year": 1900,
        "energy_improvements": ["cavity wall insulation", "double glazing"],
        "building_type": "end of terrace",
        "ownership": "bought"
    },
    3: {},
    4: {},
    5: {
        "n_occupants": 2,
        "description_of_occupants": "2 adults",
        "heating": ["natural gas"],
        "communal_boiler": True,
        "construction_year": 2009,
        "building_type": "flat",
        "ownership": "bought"
    }
}

appliances_for_each_building = {
    1: [
        {
            'type': 'boiler',
            'manufacturer': 'Worcester~Greenstar',
            'model': '30CDi Conventional natural gas',
            'fuel': 'natural gas',
            'subtype': 'system',
            'part_number': '41-311-71',
            'efficiency_rating': {'certification_name': 'SEDBUK', 'rating': 'A'},
            'nominal_consumption': {'on_power': 70},
            'distributions': 
            {
                'on_power': 
                [
                    {'model': {'distribution_name': 'normal', 'mu': 73, 'sigma': 12}}
                ]
            },
            'room': 'bathroom',
            'original_name': 'boiler',
            'year_of_purchase': 2011,
            'description': 'includes all electronics associated with the boiler including the central heating pump, the hot water pump, the bathroom underfloor heating pump, the boiler controller, the boiler itself. Over winter the central heating is on 24 hrs and is controlled by our portable wireless thermostat which is usually set at 18-20 degrees C and is put in the room we want to be the most comfortable. Prior to 3rd May 2013, the hot water was set to come on from 0630-0700 and 1630-1700.  After 3rd May the HW comes on 0650-0700 and 1650-1700.'
        },
        {
            'type': 'solar thermal pumping station',
            'manufacturer': 'Navitron',
            'model': 'Solar Thermal Pumping Station',
            'nominal_consumption': {'on_power': 43},
            'room': 'bathroom',
            'original_name': 'solar_thermal_pump',
            'year_of_purchase': 2011,
            'description': 'includes all electronics associated with the evacuated-tube solar hot water system including the water pump and control electronics.  The temperature difference controller is model STDC manufactured by Navitron'
        },
        {
            'type': 'laptop computer',
            'manufacturer': 'HP',
            'model': '6450b',
            'cpu': 'Intel(R) Core(TM) i5 CPU M450 2.40GHz',
            'nominal_consumption': {'on_power': 70},
            'components':
            [
            {
                'type': 'flat screen',
                'diagonal_size': 14.0,
                'display_technology': 'LCD',
                'max_resolution': {'horizontal': 1600, 'vertical': 900}
            }],
            'original_name': 'laptop',
            'year_of_purchase': 2010,
            'room': 'study'
        },
        {
            'type': 'laptop computer', 
            'instance': 3,
            'manufacturer': 'Lenovo',
            'original_name': 'laptop',
            'description': 'On loan from company for 3 months whilst doing a project with them.',
            'dates_active': [{'start': '2014-07-14T00:00:00+01:00', 
                              'end': '2014-10-24T23:59:59+01:00'}],
        },
        {
            'type': 'washer dryer',
            'original_name': 'washing_machine',
            'year_of_purchase': 2007,
            'manufacturer': 'Hotpoint',
            'brand': 'Aquarius',
            'model': 'WD420 1200 spin',
            'room': 'utility'
        },
        {
            'type': 'dish washer',
            'original_name': 'dishwasher',
            'year_of_purchase': 2007,
            'manufacturer': 'Whirlpool / Ikea',
            'model': 'DWH B10',
            'room': 'kitchen'
        },
        {
            'type': 'television',
            'original_name': 'tv',
            'on_power_threshold': 10,
            'year_of_manufacture': 2001,
            'manufacturer': 'Panasonic',
            'components': [
                {
                    'type': 'CRT screen',
                    'display_format': 'PAL',
                    'diagonal_size': 34
                }
            ],
            'integrated_av_sources': ['analogue TV tuner'],
            'room': 'lounge'
        },
        {
            'type': 'light',
            'instance': 1,
            'original_name': 'kitchen_lights',
            'description': '10 LED downlights in the kitchen ceiling',
            'subtype': 'ceiling downlight',
            'main_room_light': True,
            'components': [
                {
                    'type': 'LED lamp',
                    'count': 10,
                    'manufacturer': 'Philips',
                    'model': 'Dimmable MASTER LED 10W MR16 GU5.3 24degrees 2700K 12v',
                    'nominal_consumption': { 'on_power': 10 }
                },
                {
                    'type': 'dimmer', 
                    'subtype': 'TRIAC'
                }
            ],
            'nominal_consumption': { 'on_power': 100 },
            'dates_active': [{'start': '2013-04-25T08:00:00+01:00'}],
            "description": "the new, efficient kitchen ceiling lights.  Prior to 2013-04-25 we used incandescent lamps.  The kitchen receives very little natural light hence the kitchen lights are used a lot."
        },
        {
            'type': 'light',
            'instance': 2,
            'original_name': 'kitchen_lights',
            'description': '10 50W downlights in the kitchen ceiling',
            'subtype': 'ceiling downlight',
            'room': 'kitchen',
            'main_room_light': True,
            'components': [
                {
                    'type': 'incandescent lamp',
                    'subtype': 'halogen',
                    'count': 10,
                    'nominal_consumption': { 'on_power': 50 }
                },
                {
                    'type': 'dimmer', 'subtype': 'TRIAC'
                }
            ],
            'nominal_consumption': { 'on_power': 500 },
            'dates_active': [{'end': '2013-04-25T07:59:00+01:00'}],
            "description": "the old, inefficient kitchen ceiling lights.  After 2013-04-25 we used LED lamps. The kitchen receives very little natural light hence the kitchen lights are used a lot.   5th April 2013 1450 BST: replaced 1x50W halogen with 10W 12V Philips dimmable LED. 10th April 2013: replaced 1x50W halogen with 8W 12V MegaMan Dimmable LED. 25th April 2013 0800 BST: all 10 light fittings are now 10W 12V Philips dimmable LEDs."
        },
        {
            'type': 'HTPC',
            'original_name': 'htpc',
            'on_power_threshold': 20,
            'year_of_purchase': 2008,
            'room': 'lounge',
            'description': 'home theatre PC. The only AV source for the TV. Also turns itself on to record FreeView programs. Also used for playing music occasionally.'
        },
        {
            'type': 'kettle',
            'original_name': 'kettle',
            'year_of_purchase': 2007,
            'room': 'kitchen',
            'on_power_threshold': 2000,
            'dominant_appliance': True
        },
        {
            'type': 'food processor',
            'manufacturer': 'Breville',
            'original_name': 'kettle',
            'year_of_purchase': 2007,
            'room': 'kitchen'
        },
        {
            'type': 'toasted sandwich maker',
            'original_name': 'kettle',
            'year_of_purchase': 2007,
            'room': 'kitchen'
        },
        {
            'type': 'toaster',
            'original_name': 'toaster',
            'year_of_purchase': 2009,
            'room': 'kitchen',
            'on_power_threshold': 1000,
            'dominant_appliance': True
        },
        {
            'type': 'kitchen aid',
            'manufacturer': 'Artisan',
            'original_name': 'toaster',
            'year_of_purchase': 2009,
            'room': 'kitchen'
        },
        {
            'type': 'food processor',
            'instance': 2,
            'original_name': 'toaster',
            'manufacturer': 'Kenwood',
            'year_of_purchase': 2009,
            'room': 'kitchen'
        },
        {
            'type': 'fridge freezer',
            'subtype': 'fridge on top',
            'original_name': 'fridge',
            'on_power_threshold': 50,
            'year_of_purchase': 2010,
            'room': 'kitchen'
        },
        {
            'type': 'microwave',
            'original_name': 'microwave',
            'room': 'kitchen',
            'on_power_threshold': 5,
            'year_of_purchase': 2006
        },
        {
            'type': 'computer monitor',
            'original_name': 'lcd_office',
            'room': 'study',
            'components': [
                {
                    'type': 'flat screen',
                    'display_technology': 'LCD',
                    'diagonal_size': 24,
                    'manufacturer': 'Dell'
                }
            ],
            'year_of_purchase': 2010
        },
        {
            'type': 'audio system',
            'original_name': 'hifi_office',
            'room': 'study',
            'components': [
                {
                    'type': 'audio amplifier',
                    'year_of_purchase': 2012,
                    'components': [ {'type': 'DAC'} ]
                },
                {
                    'type': 'radio',
                    'subtype': 'analogue',
                    'year_of_purchase': 1995
                },
                {
                    'type': 'CD player',
                    'year_of_purchase': 1995
                }
            ]
        },
        {
            'type': 'breadmaker',
            'original_name': 'breadmaker',
            'room': 'kitchen',
            'year_of_purchase': 2010
        },
        {
            'type': 'audio amplifier',
            'original_name': 'amp_livingroom',
            'room': 'lounge',
            'year_of_purchase': 2004
        },
        {
            'type': 'broadband router',
            'original_name': 'adsl_router',
            'room': 'hall',
            'year_of_purchase': 2006
        },
        {
            'type': 'light',
            'instance': 3,
            'original_name': 'livingroom_s_lamp',
            'room': 'lounge',
            'subtype': 'floor standing',
            'year_of_purchase': 2006,
            'components': [{'type': 'compact fluorescent lamp'}]
        },
        {
            'type': 'soldering iron',
            'original_name': 'soldering_iron',
            'room': 'study',
            'description': 'temperature controlled',
            'manufacturer': 'Xytronic',
            'model': '168-3CD',
            'year_of_purchase': 2011
        },
        {
            'type': 'ethernet switch',
            'original_name': 'gigE_&_USBhub',
            'subtype': '1gigabit',
            'room': 'study',
            'year_of_purchase': 2008
        },
        {
            'type': 'USB hub',
            'original_name': 'gigE_&_USBhub',
            'room': 'study',
            'year_of_purchase': 2008
        },
        {
            'type': 'vacuum cleaner',
            'original_name': 'hoover',
            'year_of_purchase': 2008
        },
        {
            'type': 'light',
            'instance': 4,
            'subtype': 'table',
            'original_name': 'kitchen_dt_lamp',
            'room': 'kitchen',
            'components': [
                {'type': 'incandescent lamp'},
                {'type': 'dimmer', 'number_of_dimmer_levels': 3 }
            ],
            'year_of_purchase': 2006
        },
        {
            'type': 'light',
            'instance': 5,
            'subtype': 'floor standing',
            'original_name': 'bedroom_ds_lamp',
            'room': 'bedroom,1',
            'components': [
                {'type': 'incandescent lamp'},
                {'type': 'dimmer', 'subtype': 'TRIAC'}
            ],
            'year_of_purchase': 2006
        },
        {
            'type': 'light',
            'instance': 6,
            'subtype': 'floor standing',
            'original_name': 'livingroom_s_lamp2',
            'room': 'lounge',
            'year_of_purchase': 2006,
            'components': [{'type': 'compact fluorescent lamp'}]
        },
        {
            'type': 'tablet computer charger',
            'original_name': 'iPad_charger',
            'room': 'lounge',
            'year_of_purchase': 2012,
            'manufacturer': 'Apple'
        },
        {
            'type': 'active subwoofer',
            'original_name': 'subwoofer_livingroom',
            'room': 'lounge',
            'year_of_purchase': 2003
        },
        {
            'type': 'light',
            'instance': 7,
            'original_name': 'livingroom_lamp_tv',
            'room': 'lounge',
            'year_of_purchase': 2006,
            'components': [{'type': 'compact fluorescent lamp'}],
            'subtype': 'mood',
            'description': 'throws light onto the wall behind the television'
        },
        {
            'type': 'radio',
            'subtype': 'DAB',
            'original_name': 'DAB_radio_livingroom',
            'room': 'lounge',
            'year_of_purchase': 2012,
            'description': 'this DAB radio was only in the lounge when we first had it.  Then it was moved to bedroom 1 and was put on an IAM with a bunch of other low-power appliances.'
        },
        {
            'type': 'light',
            'instance': 8,
            'subtype': 'floor standing',
            'original_name': 'kitchen_lamp2',
            'components': [{'type': 'compact fluorescent lamp'}],
            'room': 'kitchen',
            'year_of_purchase': 2006
        },
        {
            'type': 'wireless phone charger',
            'original_name': 'kitchen_phone&stereo',
            'room': 'kitchen',
            'year_of_purchase': 2009
        },
        {
            'type': 'audio system',
            'instance': 2,
            'original_name': 'kitchen_phone&stereo',
            'room': 'kitchen',
            'description': 'mostly used as an amp for iPods',
            'year_of_purchase': 2009
        },
        {
            'type': 'light',
            'instance': 9,
            'original_name': 'utilityrm_lamp',
            'room': 'utility',
            'components': [{'type': 'linear fluorescent lamp'}],
            'year_of_purchase': 2006
        },
        {
            'type': 'mobile phone charger',
            'original_name': 'samsung_charger',
            'room': 'bedroom,1',
            'year_of_purchase': 2012,
            'manufacturer': 'Samsung'
        },
        {
            'type': 'light',
            'instance': 10,
            'subtype': 'table',
            'components': [
                {'type': 'incandescent lamp'},
                {'type': 'dimmer', 'number_of_dimmer_levels': 3 }
            ],
            'original_name': 'bedroom_d_lamp',
            'room': 'bedroom,1',
            'year_of_purchase': 2006,
            'description': 'This light was not plugged into its submeter for a few months.  Instead the little DAB radio in the bedroom was plugged into this submeter.  This was fixed (and the light was reconnected with its submeter) on 2014-11-30 around 18:30.'
        },
        {
            'type': 'coffee maker',
            'original_name': 'coffee_machine',
            'room': 'kitchen',
            'year_of_purchase': 2010
        },
        {
            'type': 'radio',
            'instance': 2,
            'subtype': 'analogue',
            'original_name': 'kitchen_radio',
            'on_power_threshold': 2,
            'room': 'kitchen',
            'year_of_purchase': 2004
        },
        {
            'type': 'mobile phone charger',
            'instance': 2,
            'original_name': 'bedroom_chargers',
            'on_power_threshold': 1,
            'room': 'bedroom,1',
            'year_of_purchase': 2012,
            'manufacturer': 'Apple'
        },
        {
            'type': 'baby monitor',
            'subtype': 'parent unit',
            'instance': 2,
            'original_name': 'bedroom_chargers',
            'on_power_threshold': 1,
            'room': 'bedroom,1',
            'year_of_purchase': 2011
        },
        {
            'type': 'radio',
            'instance': 3,
            'subtype': 'DAB',
            'on_power_threshold': 1,
            'original_name': 'bedroom_chargers',
            'room': 'bedroom,1',
            'year_of_purchase': 2012
        },
        {
            'type': 'hair dryer',
            'original_name': 'hair_dryer',
            'room': 'bedroom,1',
            'year_of_purchase': 2013
        },
        {
            'type': 'hair straighteners',
            'original_name': 'straighteners',
            'room': 'bedroom,1',
            'year_of_purchase': 2006
        },
        {
            'type': 'clothes iron',
            'original_name': 'iron',
            'room': 'bedroom,1',
            'year_of_purchase': 2006
        },
        {
            'type': 'oven',
            'original_name': 'gas_oven',
            'on_power_threshold': 10,
            'room': 'kitchen',
            'fuel': 'natural gas',
            'year_of_purchase': 2000
        },
        {
            'type': 'computer',
            'original_name': 'data_logger_pc',
            'do_not_inherit': ['control'],
            'control': ['always on'],
            'description': 'data logging PC',
            'cpu': 'Intel Atom',
            'room': 'hall',
            'year_of_purchase': 2012,
            'dominant_appliance': True
        },
        {
            'type': 'external hard disk',
            'original_name': 'data_logger_pc',
            'description': 'external disk used every few months to transfer data from data logging PC',
            'room': 'hall',
            'year_of_purchase': 2012
        },
        {
            'type': 'light',
            'instance': 11,
            'subtype': 'table',
            'components': [{'type': 'incandescent lamp'}],
            'year_of_purchase': 2006,
            'original_name': 'childs_table_lamp',
            'room': 'bedroom,2'
        },
        {
            'type': 'light',
            'instance': 12,
            'subtype': 'floor standing',
            'description': 'reading lamp',
            'original_name': 'childs_ds_lamp',
            'components': [{'type': 'LED lamp'}, {'type': 'dimmer'}],
            'room': 'bedroom,2',
            'year_of_purchase': 2012,
            'description': 'Prior to around 1st April 2013 it was a dimmable CFL.  But that blew so we changed to a 75W incandesent for a little while.  Then on 10th April 2013 we changed it to a Philips MASTER LEDBULB 8W dimmable.  This information has not been modelled in this schema, but it could be.'
        },
        {
            'type': 'baby monitor',
            'original_name': 'baby_monitor_tx',
            'subtype': 'baby unit',
            'room': 'bedroom,2',
            'year_of_purchase': 2011
        },
        {
            'type': 'charger',
            'original_name': 'battery_charger',
            'room': 'study',
            'description': 'for charging misc batteries (e.g. AA and AAA batteries)',
            'year_of_purchase': 2008
        },
        {
            'type': 'light',
            'instance': 13,
            'components': [{'type': 'compact fluorescent lamp'}],
            'original_name': 'office_lamp1',
            'subtype': 'mood',
            'room': 'study',
            'year_of_purchase': 2006
        },
        {
            'type': 'light',
            'instance': 14,
            'components': [{'type': 'compact fluorescent lamp'}],
            'original_name': 'office_lamp2',
            'subtype': 'mood',
            'room': 'study',
            'year_of_purchase': 2006

        },
        {
            'type': 'light',
            'instance': 15,
            'components': [{'type': 'compact fluorescent lamp'}],
            'original_name': 'office_lamp3',
            'subtype': 'table',
            'room': 'study',
            'year_of_purchase': 2006
        },
        {
            'type': 'desktop computer',
            'original_name': 'office_pc',
            'room': 'study',
            'year_of_purchase': 2007
        },
        {
            'type': 'fan',
            'subtype': 'desk',
            'original_name': 'office_fan',
            'room': 'study',
            'year_of_purchase': 2006
        },
        {
            'type': 'printer',
            'subtype': 'LED',
            'original_name': 'LED_printer',
            'room': 'study',
            'year_of_purchase': 2012
        },
        #### -- APPLIANCES NOT SUBMETERED: ---- ###
        {
            'type': 'immersion heater',
            'description': 'It has never been used and would only ever be used if the boiler broke.',
            'meters': [0],
            'room': 'bathroom',
            'year_of_purchase': 2012
        },
        {
            'type': 'water pump',
            'description': 'Very efficient under-floor heating water pump.  Uses about 5 watts when running.',
            'meters': [0],
            'room': 'lounge',
            'year_of_purchase': 2010
        },
        {
            'type': 'security alarm',
            'description': 'Always on.  Appears to use about 10 watts.  Was turned off Sunday 11th August 2013',
            'meters': [0],
            'room': 'hall',
            'year_of_purchase': 2008,
            'dates_active': [{'end': '2013-08-11'}]
        },
        {
            'type': 'fan',
            'instance': 2,
            'subtype': 'single-room MVHR',
            'description': 'Bathroom extractor fan (MVHR). On for most of the time during winter months (in summer we turn the fan off and open the window). Has 2 modes: trickle and boost.  Boost is triggered using a manual pull-cord when necessary. Only uses about 2 watts in trickle mode and about 10 watts in boost mode.',
            'meters': [0],
            'room': 'bathroom',
            'year_of_purchase': 2012          
        },
        {
            'type': 'drill', 
            'description': 'Used: Sat 13/04/2013 17:43 BST for one short burst.  And other times, not logged.',
            'meters': [0],
            'year_of_purchase': 2009
        },
        {
            'type': 'laptop computer', 
            'instance': 2,
            'manufacturer': 'Dell',
            'meters': [0],
            'year_of_purchase': 2012,
            'description': 'Charged 09:21 BST Sat 4th May 2013 and lots of other times subsequently.'
        },
        {
            'type': 'light',
            'count': 9,
            'original_name': 'lighting_circuit',
            'instance': 16,
            'description': 'all the lights on the lighting circuit.  Mostly undimmable CFLs.  One dimmable LED.  One dimmable incandescent.',
            'categories': {
                'electrical': ["incandescent", "fluorescent", "compact", "LED"]
            }
        }
    ],
    2: [
        {
            'type': 'laptop computer',
            'original_name': 'laptop'
        },
        {
            'type': 'computer monitor',
            'original_name': 'monitor'
        },
        {
            'type': 'active speaker',
            'original_name': 'speakers'
        },
        {
            'type': 'computer',
            'description': 'server',
            'original_name': 'server'
        },
        {
            'type': 'broadband router',
            'original_name': 'router'
        },
        {
            'type': 'external hard disk',
            'description': 'server_hdd',
            'original_name': 'server_hdd'
        },
        {
            'type': 'kettle',
            'original_name': 'kettle'
        },
        {
            'type': 'rice cooker',
            'original_name': 'rice_cooker'
        },
        {
            'type': 'running machine',
            'original_name': 'running_machine'
        },
        {
            'type': 'laptop computer',
            'instance': 2,
            'original_name': 'laptop2'
        },
        {
            'type': 'washing machine',
            'original_name': 'washing_machine'
        },
        {
            'type': 'dish washer',
            'original_name': 'dish_washer'
        },
        {
            'type': 'fridge',
            'original_name': 'fridge'
        },
        {
            'type': 'microwave',
            'original_name': 'microwave'
        },
        {
            'type': 'toaster',
            'original_name': 'toaster'
        },
        {
            'type': 'games console',
            'model': 'Playstation',
            'original_name': 'playstation'
        },
        {
            'type': 'modem',
            'original_name': 'modem'
        },
        {
            'type': 'cooker',
            'original_name': 'cooker'
        }
    ],
    3: [
        {
            'type': 'kettle',
            'original_name': 'kettle'
        },
        {
            'type': 'electric space heater',
            'original_name': 'electric_heater'
        },
        {
            'type': 'laptop computer',
            'original_name': 'laptop'
        },
        {
            'type': 'projector',
            'original_name': 'projector'
        }
    ],
    4: [
        {
            'type': 'television',
            'original_name': 'tv_dvd_digibox_lamp'
        },
        {
            'type': 'DVD player',
            'original_name': 'tv_dvd_digibox_lamp'
        },
        {
            'type': 'set top box',
            'description': 'digibox',
            'original_name': 'tv_dvd_digibox_lamp'
        },
        {
            'type': 'light',
            'description': 'probably near the television',
            'original_name': 'tv_dvd_digibox_lamp'
        },
        {
            'type': 'kettle',
            'original_name': 'kettle_radio'
        },
        {
            'type': 'radio',
            'description': 'probably near the kettle',
            'original_name': 'kettle_radio'
        },
        {
            'type': 'boiler',
            'fuel': 'natural gas',
            'original_name': 'gas_boiler'
        },
        {
            'type': 'freezer',
            'original_name': 'freezer'
        },
        {
            'type': 'washing machine',
            'original_name': 'washing_machine_microwave_breadmaker'
        },
        {
            'type': 'microwave',
            'original_name': 'washing_machine_microwave_breadmaker'
        },
        {
            'type': 'breadmaker',
            'original_name': 'washing_machine_microwave_breadmaker'
        }
    ],
    5: [
        {
            'type': 'active speaker',
            'original_name': 'stereo_speakers_bedroom'
        },
        {
            'type': 'desktop computer',
            'cpu': 'Intel i7',
            'original_name': 'i7_desktop'
        },
        {
            'type': 'hair dryer',
            'original_name': 'hairdryer'
        },
        {
            'type': 'television',
            'description': 'primary TV',
            'original_name': 'primary_tv'
        },
        {
            'type': 'computer monitor',
            'components': [
                {
                    'type': 'flat screen',
                    'display_technology': 'LCD',
                    'diagonal_size': 24
                }
            ],
            'room': 'bedroom',
            'original_name': '24_inch_lcd_bedroom'
        },
        {
            'type': 'running machine',
            'original_name': 'treadmill'
        },
        {
            'type': 'network attached storage',
            'original_name': 'network_attached_storage'
        },
        {
            'type': 'server computer',
            'cpu': 'Intel Core2',
            'original_name': 'core2_server'
        },
        {
            'type': 'computer monitor',
            'components': [
                {
                    'type': 'flat screen',
                    'display_technology': 'LCD',
                    'diagonal_size': 24
                }
            ],
            'original_name': '24_inch_lcd'
        },
        {
            'type': 'games console',
            'model': 'Playstation 4',
            'manufacturer': 'Sony',
            'original_name': 'PS4'
        },
        {
            'type': 'clothes iron',
            'original_name': 'steam_iron'
        },
        {
            'type': 'coffee maker',
            'model': 'Pixie',
            'manufacturer': 'Nespresso',
            'original_name': 'nespresso_pixie'
        },
        {
            'type': 'desktop computer',
            'cpu': 'Intel Atom',
            'original_name': 'atom_pc'
        },
        {
            'type': 'toaster',
            'original_name': 'toaster'
        },
        {
            'type': 'audio amplifier',
            'subtype': 'home theatre',
            'original_name': 'home_theatre_amp'
        },
        {
            'type': 'set top box',
            'model': 'Sky HD',
            'original_name': 'sky_hd_box'
        },
        {
            'type': 'kettle',
            'original_name': 'kettle'
        },
        {
            'type': 'fridge freezer',
            'original_name': 'fridge_freezer'
        },
        {
            'type': 'electric oven',
            'original_name': 'oven'
        },
        {
            'type': 'electric stove',
            'original_name': 'electric_hob'
        },
        {
            'type': 'dish washer',
            'original_name': 'dishwasher'
        },
        {
            'type': 'microwave',
            'original_name': 'microwave'
        },
        {
            'type': 'washer dryer',
            'original_name': 'washer_dryer'
        },
        {
            'type': 'vacuum cleaner',
            'original_name': 'vacuum_cleaner'
        }
    ]
}

def load_labels(data_dir):
    """Loads data from labels.dat file.

    Parameters
    ----------
    data_dir : str

    Returns
    -------
    labels : dict
         mapping channel numbers (ints) to appliance names (str)
    """
    filename = join(data_dir, 'labels.dat')
    with open(filename) as labels_file:
        lines = labels_file.readlines()

    labels = {}
    for line in lines:
        line = line.split(' ')
        # TODO add error handling if line[0] not an int
        labels[int(line[0])] = line[1].strip()

    return labels

def chan_for_label(target, labels):
    for chan, label in labels.iteritems():
        if label == target:
            return chan
    raise KeyError()

def _line_to_datetime(line):
    timestamp = line.partition(" ")[0]
    return datetime.fromtimestamp(float(timestamp), tz=TZ)

def end_time(filename):
    last_line = popen("tail -n 1 %s" % filename).read()
    return _line_to_datetime(last_line)

def start_time(filename):
    first_line = popen("head -n 1 %s" % filename).read()
    return _line_to_datetime(first_line)

def timeframe(start, end):
    return {'start': start.isoformat(), 'end': end.isoformat()}

dataset_start = None
dataset_end = None
buildings = {}
for building_i in range(1, N_BULDINGS+1):
    building = building_metadata[building_i]
    building['instance'] = building_i
    original_building_name = 'house_{:d}'.format(building_i)
    building['original_name'] = original_building_name
    building_path = join(RAW_UKPD_DATA_PATH, original_building_name)

    #--------- METERS -------------------------------
    mains = join(building_path, 'mains.dat')
    mains_exists =  isfile(mains)
    labels = load_labels(building_path)
    building_start = None
    building_end = None
    building['elec_meters'] = {}
    chans = labels.keys() 
    chans.sort() # we want to process meters in order
    for chan in chans:
        label = labels[chan]
        fname = join(building_path, 'channel_{:d}.dat'.format(chan))
        start = start_time(fname)
        end = end_time(fname)
        if building_start is None or start < building_start:
            building_start = start
        if building_end is None or end > building_end:
            building_end = end

        meter = {
            'data_location': 
                 'house_{:d}/channel_{:d}.dat'.format(building_i, chan),
            'timeframe': timeframe(start, end)
        }

        if label == 'aggregate':
            meter.update({"site_meter": True,
                          'device_model': 'EcoManagerWholeHouseTx',
                          'preprocessing_applied': 
                              {'clip': {'upper_limit': 20000}}})
        else:
            meter.update({"submeter_of": 0 if mains_exists else 1,
                          'device_model': 'EcoManagerTxPlug',
                          'preprocessing_applied': 
                              {'clip': {'upper_limit': 4000}}})
            if building_i == 1:
                if label in ['boiler', 'solar_thermal_pump', 'lighting_circuit',
                             'kitchen_lights']:
                    meter.update({'device_model': 'CurrentCostTx'})

                if label == 'kitchen_lights':
                    meter.update({"submeter_of": 
                                  chan_for_label('lighting_circuit', labels)})

                if label == 'toaster':
                    meter.update({'warning': 'For the five days from Mon 24th June 2013 to Fri 28th June we had someone staying at the house who occassionally swapped the toaster and kettle around (i.e. the toaster was plugged into the kettle sensor and visa-versa!) and also appeared to plug the hoover sensor into the kettle sensor (i.e. both the hoover and kettle sensor would have recorded the same appliance for a few hours).'})

        building['elec_meters'][chan] = meter
        
    if mains_exists:
        meters = building['elec_meters'].keys()
        meters.sort()
        building['elec_meters'][meters[-1]+1] = {
            'device_model': 'SoundCardPowerMeter',
            'timeframe': timeframe(start_time(mains), end_time(mains)),
            'site_meter': True,
            'submeter_of': 1,
            'data_location': 'house_{:d}/mains.dat'.format(building_i)
        }

    building['timeframe'] = timeframe(building_start, building_end)
    if dataset_start is None or building_start < dataset_start:
        dataset_start = building_start
    if dataset_end is None or building_end > dataset_end:
        dataset_end = building_end

    #------------ APPLIANCES --------------------
    appliances = appliances_for_each_building[building_i]

    # infer meter IDs from original_name and labels.dat
    instances = {}
    for i in range(len(appliances)):
        appliance = appliances[i]
        if not appliance.get('meters'):
            appliance['meters'] = [chan_for_label(appliance['original_name'], labels)]
        if not appliance.get('instance'):
            appliance_type = appliance.get('type')
            instance = instances.setdefault(appliance_type, 1)
            appliance['instance'] = instance
            instances[appliance_type] += 1
    
    building['appliances'] = appliances
    buildings[building_i] = building
    
dataset['timeframe'] = timeframe(dataset_start, dataset_end)
dataset['date'] = dataset_end.date().isoformat()
    
with open(join(OUTPUT_PATH, 'dataset.yaml'), 'w') as fh:
    yaml.dump(dataset, fh)

for building_i, building in buildings.iteritems():
    with open(join(OUTPUT_PATH, 'building{:d}.yaml'.format(building_i)), 'w') as fh:
        yaml.dump(building, fh)

print("done")
