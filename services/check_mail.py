import requests


class CheckMail:
    def __init__(self, email):
        self.base_url = "https://api.mailcheck.ai"
        self.headers = {"Content-Type": "application/json"}
        self.email = email
        self.check = self.check_mail()

    def check_mail(self):
        mail = self.base_url + f"/email/{self.email}"
        response = requests.get(mail, headers=self.headers)
        temp_mail = response.json()["disposable"]
        if temp_mail == True:
            return True
        elif temp_mail == False:
            return False
