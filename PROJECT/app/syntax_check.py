import re

class CheckFormat():
    def is_valid_phone_number_with_cc(self, phone_number):
    
        pattern=r"^\+([0-9]{1,3})\s?-?\.?([0-9]{10})$"
        return re.match(pattern, phone_number) is not None

    def is_valid_phone_number(self, phone_number):
        pattern=r"^\s*[0-9]{10}\s*$"
        return re.match(pattern, phone_number) is not None
    
    def is_valid_email(self, email):
        pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        return re.match(pattern, email) is not None
    
    def is_valid_linkedin_url(self, url):
        pattern = r"^(https:\/\/(www\.)?)?linkedin\.com\/in\/[a-zA-Z0-9-]+\/?$"
        return re.match(pattern, url) is not None
    
    def is_valid_github_url(self, url):
        pattern = r"^(https:\/\/(www\.)?)?github\.com\/[a-zA-Z0-9-]+(\/[a-zA-Z0-9-_]+)?\/?$"
        return re.match(pattern, url) is not None