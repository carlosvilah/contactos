import xmlrpc.client
from decouple import config

class OdooClient:
    def __init__(self):
        self.url = config('ODOO_URL')
        self.db = config('ODOO_DB')
        self.username = config('ODOO_USERNAME')
        self.password = config('ODOO_PASSWORD')
        self.uid = None
        self.models = None
        self._authenticate()

    def _authenticate(self):
        common = xmlrpc.client.ServerProxy(f'{self.url}/xmlrpc/2/common')
        self.uid = common.authenticate(self.db, self.username, self.password, {})
        if not self.uid:
            raise ValueError("Authentication with Odoo failed!")

        self.models = xmlrpc.client.ServerProxy(f'{self.url}/xmlrpc/2/object')
