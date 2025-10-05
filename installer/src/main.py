# installer/src/main.py
from flow.scraper_flow import LoginAutomator

if __name__ == "__main__":
    automator = LoginAutomator()
    automator.ensure_logged_in()   
    automator.ensure_logged_in()