#!/usr/bin/env python
# -*- coding: utf-8 -*-
from dotenv import load_dotenv, find_dotenv
import datetime
import os
import json

# load environment variables
load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))
# local, sandbox, or production
MODE = os.getenv('MODE')
print('RUNNING IN {} MODE'.format(MODE))
TEST = False if MODE == 'production' else True
SHOW_DOCS = True
DOCS_URL = '/docs'
FLASK_PROFILER = False
FLASK_SECRET_KEY = os.getenv('FLASK_SECRET_KEY')
FLASK_SALT = os.getenv('FLASK_SALT')
PASSWORD_RECOVER_KEY = os.getenv('PASSWORD_RECOVER_KEY')
JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
DATABASE_NAME = os.getenv('DATABASE_NAME')
DATABASE_USERNAME = os.getenv('DATABASE_USERNAME') 
DATABASE_PASSWORD = os.getenv('DATABASE_PASSWORD')
DATABASE_HOST = os.getenv('DATABASE_HOST')
if MODE != 'local':
    DATABASE_HOST = os.getenv('DATABASE_HOST').format(
        username=DATABASE_USERNAME, 
        password=DATABASE_PASSWORD, 
        database=DATABASE_NAME) 
CURRENT_DATE = datetime.datetime.now()
LOGO_WORDMARK = ''
LOGO_SYMBOL = ''
ADMIN_EMAIL = 'support@66pct.xyz'
INTERNAL_PARTNER_EMAIL = ''
SUPPORT_EMAIL = ADMIN_EMAIL
SECURITY_EMAIL = ''
PRESS_EMAIL = ''
SELF_ALERT_EMAIL = ADMIN_EMAIL
BRAND_NAME = os.getenv('BRAND_NAME')
COMPANY_NAME = os.getenv('COMPANY_NAME')
MARKETING_WEBSITE_URL = ''
LINKEDIN_URL = ''
API_VERSION = 'v1'
API_URL_PREFIX = '{}'.format(API_VERSION)
if MODE == 'sandbox':
    API_SUBDOMAIN = 'api'
    WEB_SUBDOMAIN = None
    DASHBOARD_SUBDOMAIN = None
    BASE_DOMAIN = '66pct.xyz'
    DASHBOARD_ENDPOINT = os.getenv('DASHBOARD_ENDPOINT') 
    API_ENDPOINT = os.getenv('API_ENDPOINT')
elif MODE == 'local':
    API_SUBDOMAIN = None
    DASHBOARD_SUBDOMAIN = None
    WEB_SUBDOMAIN = None
    BASE_DOMAIN = None
    API_ENDPOINT = os.getenv('API_ENDPOINT')
    DASHBOARD_ENDPOINT = os.getenv('DASHBOARD_ENDPOINT')
elif MODE == 'production':
    API_SUBDOMAIN = 'api'
    WEB_SUBDOMAIN = None
    DASHBOARD_SUBDOMAIN = None
    BASE_DOMAIN = '66pct.xyz'
    DASHBOARD_ENDPOINT = os.getenv('DASHBOARD_ENDPOINT') 
    API_ENDPOINT = os.getenv('API_ENDPOINT')
API_FILE_ENDPOINT = API_ENDPOINT
TRADING_SERVICE_BASE_URL = os.getenv('TRADING_SERVICE_BASE_URL')
WEBSOCKET_ENDPOINT = os.getenv('WEBSOCKET_ENDPOINT')
SENDGRID_KEY = os.getenv('SENDGRID_KEY')
SENDGRID_WEBHOOKS_URL = '/api/webhooks/sendgrid'
IB_USERNAME = os.getenv('IB_USERNAME')
IB_PASSWORD = os.getenv('IB_PASSWORD')
TWILIO_SID = os.getenv('TWILIO_SID')
TWILIO_TOKEN = os.getenv('TWILIO_TOKEN')
AUTHY_API_KEY = os.getenv('AUTHY_API_KEY')
TWILIO_NUMBER = os.getenv('TWILIO_NUMBER')
SUPPORT_PHONE = ''
MAILING_ADDRESS = ''
CARD_PROCESSING_FEE = .04 # pct
CARD_PROCESSING_FIXED_FEE = .30 # dollars
STRIPE_ENDPOINT = 'https://api.stripe.com'
STRIPE_SECRET_KEY = os.getenv('STRIPE_SECRET_KEY')
STRIPE_PUBLIC_KEY = os.getenv('STRIPE_PUBLIC_KEY')
LIST_ENVELOPE = 'data'
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_ACCESS_KEY_SECRET = os.getenv('AWS_ACCESS_KEY_SECRET')
AWS_S3_BUCKET = '-'.join(DATABASE_NAME.split('_')) + '-' + MODE
AWS_S3_IMAGE_BUCKET = AWS_S3_BUCKET + '-images-' + MODE
LOG_LEVEL = 'INFO'
TERMS_OF_SERVICE_URL = DASHBOARD_ENDPOINT + '/terms_of_service'
PRIVACY_URL = DASHBOARD_ENDPOINT + '/privacy'
LOGIN_URL = DASHBOARD_ENDPOINT + '/login'
SIGNUP_URL = DASHBOARD_ENDPOINT + '/signup'
CHANGE_PASSWORD_ROUTE = '/change_password'
GREATER_THAN = 'greater than'
GREATER_THAN_OR_EQUAL_TO = 'greater than or equal to'
LESS_THAN = 'less than'
LESS_THAN_OR_EQUAL_TO = 'less than or equal to'
CONDITIONS = [
    GREATER_THAN, 
    GREATER_THAN_OR_EQUAL_TO, 
    LESS_THAN, 
    LESS_THAN_OR_EQUAL_TO
]
FIELDS = [
    'price',
    'delta',
    'daily_pnl',
    'unrealized_pnl',
    'gamma',
    'theta',
    'vega',
    'underlying_price',
    'underlying_pct_change',
    'unrealized_pct_change',
    'pnl_pct_change',
    'value',
] 
ROLES = [
    {'name': 'owner', 'description': 'Full access rights'},
    {'name': 'manager', 'description': 'Same rights as owner but cannot change critical items'},
    {'name': 'read_only', 'description': 'Read-only rights'},
]
USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36'
MONTHS = [
    {'short_name': 'Jan', 'name': "January", "number": 1}, 
    {'short_name': 'Feb', 'name': "February", "number": 2}, 
    {'short_name': 'Mar', 'name': "March", "number": 3}, 
    {'short_name': 'Apr', 'name': "April", "number": 4}, 
    {'short_name': 'May', 'name': "May", "number": 5}, 
    {'short_name': 'Jun', 'name': "June", "number": 6}, 
    {'short_name': 'Jul', 'name': "July", "number": 7}, 
    {'short_name': 'Aug', 'name': "August", "number": 8}, 
    {'short_name': 'Sep', 'name': "September", "number": 9}, 
    {'short_name': 'Oct', 'name': "October", "number": 10}, 
    {'short_name': 'Nov', 'name': "November", "number": 11}, 
    {'short_name': 'Dec', 'name': "December", "number": 12}, 
]
COUNTRIES = [
{"name": "Afghanistan", "code": "AF"},
{"name": "Åland Islands", "code": "AX"},
{"name": "Albania", "code": "AL"},
{"name": "Algeria", "code": "DZ"},
{"name": "American Samoa", "code": "AS"},
{"name": "AndorrA", "code": "AD"},
{"name": "Angola", "code": "AO"},
{"name": "Anguilla", "code": "AI"},
{"name": "Antarctica", "code": "AQ"},
{"name": "Antigua and Barbuda", "code": "AG"},
{"name": "Argentina", "code": "AR"},
{"name": "Armenia", "code": "AM"},
{"name": "Aruba", "code": "AW"},
{"name": "Australia", "code": "AU"},
{"name": "Austria", "code": "AT"},
{"name": "Azerbaijan", "code": "AZ"},
{"name": "Bahamas", "code": "BS"},
{"name": "Bahrain", "code": "BH"},
{"name": "Bangladesh", "code": "BD"},
{"name": "Barbados", "code": "BB"},
{"name": "Belarus", "code": "BY"},
{"name": "Belgium", "code": "BE"},
{"name": "Belize", "code": "BZ"},
{"name": "Benin", "code": "BJ"},
{"name": "Bermuda", "code": "BM"},
{"name": "Bhutan", "code": "BT"},
{"name": "Bolivia", "code": "BO"},
{"name": "Bosnia and Herzegovina", "code": "BA"},
{"name": "Botswana", "code": "BW"},
{"name": "Bouvet Island", "code": "BV"},
{"name": "Brazil", "code": "BR"},
{"name": "British Indian Ocean Territory", "code": "IO"},
{"name": "Brunei Darussalam", "code": "BN"},
{"name": "Bulgaria", "code": "BG"},
{"name": "Burkina Faso", "code": "BF"},
{"name": "Burundi", "code": "BI"},
{"name": "Cambodia", "code": "KH"},
{"name": "Cameroon", "code": "CM"},
{"name": "Canada", "code": "CA"},
{"name": "Cape Verde", "code": "CV"},
{"name": "Cayman Islands", "code": "KY"},
{"name": "Central African Republic", "code": "CF"},
{"name": "Chad", "code": "TD"},
{"name": "Chile", "code": "CL"},
{"name": "China", "code": "CN"},
{"name": "Christmas Island", "code": "CX"},
{"name": "Cocos (Keeling) Islands", "code": "CC"},
{"name": "Colombia", "code": "CO"},
{"name": "Comoros", "code": "KM"},
{"name": "Congo", "code": "CG"},
{"name": "Congo, The Democratic Republic of the", "code": "CD"},
{"name": "Cook Islands", "code": "CK"},
{"name": "Costa Rica", "code": "CR"},
{"name": "Cote D'Ivoire", "code": "CI"},
{"name": "Croatia", "code": "HR"},
{"name": "Cuba", "code": "CU"},
{"name": "Cyprus", "code": "CY"},
{"name": "Czech Republic", "code": "CZ"},
{"name": "Denmark", "code": "DK"},
{"name": "Djibouti", "code": "DJ"},
{"name": "Dominica", "code": "DM"},
{"name": "Dominican Republic", "code": "DO"},
{"name": "Ecuador", "code": "EC"},
{"name": "Egypt", "code": "EG"},
{"name": "El Salvador", "code": "SV"},
{"name": "Equatorial Guinea", "code": "GQ"},
{"name": "Eritrea", "code": "ER"},
{"name": "Estonia", "code": "EE"},
{"name": "Ethiopia", "code": "ET"},
{"name": "Falkland Islands (Malvinas)", "code": "FK"},
{"name": "Faroe Islands", "code": "FO"},
{"name": "Fiji", "code": "FJ"},
{"name": "Finland", "code": "FI"},
{"name": "France", "code": "FR"},
{"name": "French Guiana", "code": "GF"},
{"name": "French Polynesia", "code": "PF"},
{"name": "French Southern Territories", "code": "TF"},
{"name": "Gabon", "code": "GA"},
{"name": "Gambia", "code": "GM"},
{"name": "Georgia", "code": "GE"},
{"name": "Germany", "code": "DE"},
{"name": "Ghana", "code": "GH"},
{"name": "Gibraltar", "code": "GI"},
{"name": "Greece", "code": "GR"},
{"name": "Greenland", "code": "GL"},
{"name": "Grenada", "code": "GD"},
{"name": "Guadeloupe", "code": "GP"},
{"name": "Guam", "code": "GU"},
{"name": "Guatemala", "code": "GT"},
{"name": "Guernsey", "code": "GG"},
{"name": "Guinea", "code": "GN"},
{"name": "Guinea-Bissau", "code": "GW"},
{"name": "Guyana", "code": "GY"},
{"name": "Haiti", "code": "HT"},
{"name": "Heard Island and Mcdonald Islands", "code": "HM"},
{"name": "Holy See (Vatican City State)", "code": "VA"},
{"name": "Honduras", "code": "HN"},
{"name": "Hong Kong", "code": "HK"},
{"name": "Hungary", "code": "HU"},
{"name": "Iceland", "code": "IS"},
{"name": "India", "code": "IN"},
{"name": "Indonesia", "code": "ID"},
{"name": "Iran, Islamic Republic Of", "code": "IR"},
{"name": "Iraq", "code": "IQ"},
{"name": "Ireland", "code": "IE"},
{"name": "Isle of Man", "code": "IM"},
{"name": "Israel", "code": "IL"},
{"name": "Italy", "code": "IT"},
{"name": "Jamaica", "code": "JM"},
{"name": "Japan", "code": "JP"},
{"name": "Jersey", "code": "JE"},
{"name": "Jordan", "code": "JO"},
{"name": "Kazakhstan", "code": "KZ"},
{"name": "Kenya", "code": "KE"},
{"name": "Kiribati", "code": "KI"},
{"name": "Korea, Democratic People's Republic of", "code": "KP"},
{"name": "Korea, Republic of", "code": "KR"},
{"name": "Kuwait", "code": "KW"},
{"name": "Kyrgyzstan", "code": "KG"},
{"name": "Lao People's Democratic Republic", "code": "LA"},
{"name": "Latvia", "code": "LV"},
{"name": "Lebanon", "code": "LB"},
{"name": "Lesotho", "code": "LS"},
{"name": "Liberia", "code": "LR"},
{"name": "Libyan Arab Jamahiriya", "code": "LY"},
{"name": "Liechtenstein", "code": "LI"},
{"name": "Lithuania", "code": "LT"},
{"name": "Luxembourg", "code": "LU"},
{"name": "Macao", "code": "MO"},
{"name": "Macedonia, The Former Yugoslav Republic of", "code": "MK"},
{"name": "Madagascar", "code": "MG"},
{"name": "Malawi", "code": "MW"},
{"name": "Malaysia", "code": "MY"},
{"name": "Maldives", "code": "MV"},
{"name": "Mali", "code": "ML"},
{"name": "Malta", "code": "MT"},
{"name": "Marshall Islands", "code": "MH"},
{"name": "Martinique", "code": "MQ"},
{"name": "Mauritania", "code": "MR"},
{"name": "Mauritius", "code": "MU"},
{"name": "Mayotte", "code": "YT"},
{"name": "Mexico", "code": "MX"},
{"name": "Micronesia, Federated States of", "code": "FM"},
{"name": "Moldova, Republic of", "code": "MD"},
{"name": "Monaco", "code": "MC"},
{"name": "Mongolia", "code": "MN"},
{"name": "Montserrat", "code": "MS"},
{"name": "Morocco", "code": "MA"},
{"name": "Mozambique", "code": "MZ"},
{"name": "Myanmar", "code": "MM"},
{"name": "Namibia", "code": "NA"},
{"name": "Nauru", "code": "NR"},
{"name": "Nepal", "code": "NP"},
{"name": "Netherlands", "code": "NL"},
{"name": "Netherlands Antilles", "code": "AN"},
{"name": "New Caledonia", "code": "NC"},
{"name": "New Zealand", "code": "NZ"},
{"name": "Nicaragua", "code": "NI"},
{"name": "Niger", "code": "NE"},
{"name": "Nigeria", "code": "NG"},
{"name": "Niue", "code": "NU"},
{"name": "Norfolk Island", "code": "NF"},
{"name": "Northern Mariana Islands", "code": "MP"},
{"name": "Norway", "code": "NO"},
{"name": "Oman", "code": "OM"},
{"name": "Pakistan", "code": "PK"},
{"name": "Palau", "code": "PW"},
{"name": "Palestinian Territory, Occupied", "code": "PS"},
{"name": "Panama", "code": "PA"},
{"name": "Papua New Guinea", "code": "PG"},
{"name": "Paraguay", "code": "PY"},
{"name": "Peru", "code": "PE"},
{"name": "Philippines", "code": "PH"},
{"name": "Pitcairn", "code": "PN"},
{"name": "Poland", "code": "PL"},
{"name": "Portugal", "code": "PT"},
{"name": "Puerto Rico", "code": "PR"},
{"name": "Qatar", "code": "QA"},
{"name": "Reunion", "code": "RE"},
{"name": "Romania", "code": "RO"},
{"name": "Russian Federation", "code": "RU"},
{"name": "RWANDA", "code": "RW"},
{"name": "Saint Helena", "code": "SH"},
{"name": "Saint Kitts and Nevis", "code": "KN"},
{"name": "Saint Lucia", "code": "LC"},
{"name": "Saint Pierre and Miquelon", "code": "PM"},
{"name": "Saint Vincent and the Grenadines", "code": "VC"},
{"name": "Samoa", "code": "WS"},
{"name": "San Marino", "code": "SM"},
{"name": "Sao Tome and Principe", "code": "ST"},
{"name": "Saudi Arabia", "code": "SA"},
{"name": "Senegal", "code": "SN"},
{"name": "Serbia and Montenegro", "code": "CS"},
{"name": "Seychelles", "code": "SC"},
{"name": "Sierra Leone", "code": "SL"},
{"name": "Singapore", "code": "SG"},
{"name": "Slovakia", "code": "SK"},
{"name": "Slovenia", "code": "SI"},
{"name": "Solomon Islands", "code": "SB"},
{"name": "Somalia", "code": "SO"},
{"name": "South Africa", "code": "ZA"},
{"name": "South Georgia and the South Sandwich Islands", "code": "GS"},
{"name": "Spain", "code": "ES"},
{"name": "Sri Lanka", "code": "LK"},
{"name": "Sudan", "code": "SD"},
{"name": "Suriname", "code": "SR"},
{"name": "Svalbard and Jan Mayen", "code": "SJ"},
{"name": "Swaziland", "code": "SZ"},
{"name": "Sweden", "code": "SE"},
{"name": "Switzerland", "code": "CH"},
{"name": "Syrian Arab Republic", "code": "SY"},
{"name": "Taiwan, Province of China", "code": "TW"},
{"name": "Tajikistan", "code": "TJ"},
{"name": "Tanzania, United Republic of", "code": "TZ"},
{"name": "Thailand", "code": "TH"},
{"name": "Timor-Leste", "code": "TL"},
{"name": "Togo", "code": "TG"},
{"name": "Tokelau", "code": "TK"},
{"name": "Tonga", "code": "TO"},
{"name": "Trinidad and Tobago", "code": "TT"},
{"name": "Tunisia", "code": "TN"},
{"name": "Turkey", "code": "TR"},
{"name": "Turkmenistan", "code": "TM"},
{"name": "Turks and Caicos Islands", "code": "TC"},
{"name": "Tuvalu", "code": "TV"},
{"name": "Uganda", "code": "UG"},
{"name": "Ukraine", "code": "UA"},
{"name": "United Arab Emirates", "code": "AE"},
{"name": "United Kingdom", "code": "GB"},
{"name": "United States", "code": "US"},
{"name": "United States Minor Outlying Islands", "code": "UM"},
{"name": "Uruguay", "code": "UY"},
{"name": "Uzbekistan", "code": "UZ"},
{"name": "Vanuatu", "code": "VU"},
{"name": "Venezuela", "code": "VE"},
{"name": "Viet Nam", "code": "VN"},
{"name": "Virgin Islands, British", "code": "VG"},
{"name": "Virgin Islands, U.S.", "code": "VI"},
{"name": "Wallis and Futuna", "code": "WF"},
{"name": "Western Sahara", "code": "EH"},
{"name": "Yemen", "code": "YE"},
{"name": "Zambia", "code": "ZM"},
{"name": "Zimbabwe", "code": "ZW"}
]

CURRENCIES =  [
      "usd",
      "aed",
      "afn",
      "all",
      "amd",
      "ang",
      "aoa",
      "ars",
      "aud",
      "awg",
      "azn",
      "bam",
      "bbd",
      "bdt",
      "bgn",
      "bif",
      "bmd",
      "bnd",
      "bob",
      "brl",
      "bsd",
      "bwp",
      "bzd",
      "cad",
      "cdf",
      "chf",
      "clp",
      "cny",
      "cop",
      "crc",
      "cve",
      "czk",
      "djf",
      "dkk",
      "dop",
      "dzd",
      "egp",
      "etb",
      "eur",
      "fjd",
      "fkp",
      "gbp",
      "gel",
      "gip",
      "gmd",
      "gnf",
      "gtq",
      "gyd",
      "hkd",
      "hnl",
      "hrk",
      "htg",
      "huf",
      "idr",
      "ils",
      "inr",
      "isk",
      "jmd",
      "jpy",
      "kes",
      "kgs",
      "khr",
      "kmf",
      "krw",
      "kyd",
      "kzt",
      "lak",
      "lbp",
      "lkr",
      "lrd",
      "lsl",
      "mad",
      "mdl",
      "mga",
      "mkd",
      "mmk",
      "mnt",
      "mop",
      "mro",
      "mur",
      "mvr",
      "mwk",
      "mxn",
      "myr",
      "mzn",
      "nad",
      "ngn",
      "nio",
      "nok",
      "npr",
      "nzd",
      "pab",
      "pen",
      "pgk",
      "php",
      "pkr",
      "pln",
      "pyg",
      "qar",
      "ron",
      "rsd",
      "rub",
      "rwf",
      "sar",
      "sbd",
      "scr",
      "sek",
      "sgd",
      "shp",
      "sll",
      "sos",
      "srd",
      "std",
      "svc",
      "szl",
      "thb",
      "tjs",
      "top",
      "try",
      "ttd",
      "twd",
      "tzs",
      "uah",
      "ugx",
      "uyu",
      "uzs",
      "vnd",
      "vuv",
      "wst",
      "xaf",
      "xcd",
      "xof",
      "xpf",
      "yer",
      "zar",
      "zmw"
]

STRIPE_COUNTRIES = [
    'Australia',
    'Austria',
    'Belgium',
    'Canada',
    'Denmark',
    'Finland',
    'France',
    'Germany',
    'Hong Kong',
    'Ireland',
    'Italy',
    'Japan',
    'Luxembourg',
    'Netherlands',
    'New Zealand',
    'Norway',
    'Portugal',
    'Singapore',
    'Spain',
    'Sweden',
    'Switzerland',
    'United Kingdom',
    'United States',
]
STRIPE_CURRENCIES = [
    'usd', 
    'gbp',
    'eur', 
    'aud', 
    'cad',
    'jpy',
    'nok',
    'chf', 
    'sek', 
    'nzd',
    'dkk',
    'sgd', 
    'hkd', 
] 

ALLOWED_COUNTRIES = [x for x in COUNTRIES if x['name'] in STRIPE_COUNTRIES]
ALLOWED_CURRENCIES = STRIPE_CURRENCIES 
PAYMENT_METHODS = ['bank_account', 'card']
DAY_NAMES = {
    'monday': 0,
    'tuesday': 1,
    'wednesday': 2,
    'thursday': 3,
    'friday': 4,
    'saturday': 5,
    'sunday': 6,
}


STATES = [
    {
        "name": "Alabama",
        "abbreviation": "AL"
    },
    {
        "name": "Alaska",
        "abbreviation": "AK"
    },
    {
        "name": "American Samoa",
        "abbreviation": "AS"
    },
    {
        "name": "Arizona",
        "abbreviation": "AZ"
    },
    {
        "name": "Arkansas",
        "abbreviation": "AR"
    },
    {
        "name": "California",
        "abbreviation": "CA"
    },
    {
        "name": "Colorado",
        "abbreviation": "CO"
    },
    {
        "name": "Connecticut",
        "abbreviation": "CT"
    },
    {
        "name": "Delaware",
        "abbreviation": "DE"
    },
    {
        "name": "District Of Columbia",
        "abbreviation": "DC"
    },
    {
        "name": "Federated States Of Micronesia",
        "abbreviation": "FM"
    },
    {
        "name": "Florida",
        "abbreviation": "FL"
    },
    {
        "name": "Georgia",
        "abbreviation": "GA"
    },
    {
        "name": "Guam",
        "abbreviation": "GU"
    },
    {
        "name": "Hawaii",
        "abbreviation": "HI"
    },
    {
        "name": "Idaho",
        "abbreviation": "ID"
    },
    {
        "name": "Illinois",
        "abbreviation": "IL"
    },
    {
        "name": "Indiana",
        "abbreviation": "IN"
    },
    {
        "name": "Iowa",
        "abbreviation": "IA"
    },
    {
        "name": "Kansas",
        "abbreviation": "KS"
    },
    {
        "name": "Kentucky",
        "abbreviation": "KY"
    },
    {
        "name": "Louisiana",
        "abbreviation": "LA"
    },
    {
        "name": "Maine",
        "abbreviation": "ME"
    },
    {
        "name": "Marshall Islands",
        "abbreviation": "MH"
    },
    {
        "name": "Maryland",
        "abbreviation": "MD"
    },
    {
        "name": "Massachusetts",
        "abbreviation": "MA"
    },
    {
        "name": "Michigan",
        "abbreviation": "MI"
    },
    {
        "name": "Minnesota",
        "abbreviation": "MN"
    },
    {
        "name": "Mississippi",
        "abbreviation": "MS"
    },
    {
        "name": "Missouri",
        "abbreviation": "MO"
    },
    {
        "name": "Montana",
        "abbreviation": "MT"
    },
    {
        "name": "Nebraska",
        "abbreviation": "NE"
    },
    {
        "name": "Nevada",
        "abbreviation": "NV"
    },
    {
        "name": "New Hampshire",
        "abbreviation": "NH"
    },
    {
        "name": "New Jersey",
        "abbreviation": "NJ"
    },
    {
        "name": "New Mexico",
        "abbreviation": "NM"
    },
    {
        "name": "New York",
        "abbreviation": "NY"
    },
    {
        "name": "North Carolina",
        "abbreviation": "NC"
    },
    {
        "name": "North Dakota",
        "abbreviation": "ND"
    },
    {
        "name": "Northern Mariana Islands",
        "abbreviation": "MP"
    },
    {
        "name": "Ohio",
        "abbreviation": "OH"
    },
    {
        "name": "Oklahoma",
        "abbreviation": "OK"
    },
    {
        "name": "Oregon",
        "abbreviation": "OR"
    },
    {
        "name": "Palau",
        "abbreviation": "PW"
    },
    {
        "name": "Pennsylvania",
        "abbreviation": "PA"
    },
    {
        "name": "Puerto Rico",
        "abbreviation": "PR"
    },
    {
        "name": "Rhode Island",
        "abbreviation": "RI"
    },
    {
        "name": "South Carolina",
        "abbreviation": "SC"
    },
    {
        "name": "South Dakota",
        "abbreviation": "SD"
    },
    {
        "name": "Tennessee",
        "abbreviation": "TN"
    },
    {
        "name": "Texas",
        "abbreviation": "TX"
    },
    {
        "name": "Utah",
        "abbreviation": "UT"
    },
    {
        "name": "Vermont",
        "abbreviation": "VT"
    },
    {
        "name": "Virgin Islands",
        "abbreviation": "VI"
    },
    {
        "name": "Virginia",
        "abbreviation": "VA"
    },
    {
        "name": "Washington",
        "abbreviation": "WA"
    },
    {
        "name": "West Virginia",
        "abbreviation": "WV"
    },
    {
        "name": "Wisconsin",
        "abbreviation": "WI"
    },
    {
        "name": "Wyoming",
        "abbreviation": "WY"
    }
]
