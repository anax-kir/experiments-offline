from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty


class AgreementScreen(Screen):
    """
    Ask participant to agree to experiment rules and ask for email (optional field)
    """
    agreement = False
    email = ObjectProperty(None)

    def record_agreement(self, state):
        if state == "down":
            self.agreement = True
        else:
            self.agreement = False

    def record_email(self, value):
        if value and "@" in value and "." in value:
            self.email = value
            print(self.email)
        else:
            if self.email:
                self.email = None
                print(self.email)

    def check_agreement(self):
        if self.agreement:
            self.manager.current = "SocioLingScreen"
