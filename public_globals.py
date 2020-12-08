from config import *

class PublicGlobals(object):

    def __init__(self):
        self.stripe_public_key = STRIPE_PUBLIC_KEY
        self.marketing_website_url = MARKETING_WEBSITE_URL
        self.linkedin_url = LINKEDIN_URL
        self.api_endpoint = API_ENDPOINT
        self.api_file_endpoint = API_FILE_ENDPOINT
        self.dashboard_endpoint = DASHBOARD_ENDPOINT 
        self.base_domain = BASE_DOMAIN
        self.logo_symbol = LOGO_SYMBOL
        self.logo_wordmark = LOGO_WORDMARK
        self.login_url = LOGIN_URL
        self.signup_url = SIGNUP_URL
        self.countries = COUNTRIES
        self.currencies = CURRENCIES 
        self.allowed_countries = ALLOWED_COUNTRIES
        self.allowed_currencies = ALLOWED_CURRENCIES
        self.months = MONTHS
        self.card_processing_fee = CARD_PROCESSING_FEE
        self.card_processing_fixed_fee = CARD_PROCESSING_FIXED_FEE
        self.support_email = SUPPORT_EMAIL
        self.press_email = PRESS_EMAIL
        self.security_email = SECURITY_EMAIL
        self.support_phone = SUPPORT_PHONE
        self.brand_name = BRAND_NAME 
        self.conditions = CONDITIONS
        self.fields = FIELDS
        self.company_name = COMPANY_NAME
        self.mailing_address = MAILING_ADDRESS
        self.mode = MODE
        self.api_url_prefix = API_URL_PREFIX
        self.payment_methods = PAYMENT_METHODS
        self.terms_of_service_url = TERMS_OF_SERVICE_URL
        self.privacy_url = PRIVACY_URL
        self.current_date = CURRENT_DATE
        self.states = STATES

    def data(self):
        return self.__dict__
