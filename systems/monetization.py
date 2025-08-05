from datetime import datetime

class FaithPass:
    def __init__(self, active=False, expiry_date=None):
        self.active = active
        self.expiry_date = expiry_date

    def is_active(self):
        return self.active and (self.expiry_date is None or self.expiry_date > datetime.now())
