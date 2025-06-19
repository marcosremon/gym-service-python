import re

class MailUtils:
    @staticmethod
    def is_email_valid(email):
        pattern = r'^[^@]+@[^@]+\.[^@]+$'
        return re.match(pattern, email) is not None