"""
=========================================
CHITT - Weather Plugin
=========================================
Author  : AVISHKAR
Project : CHITT AI Assistant
Version : 1.0.0
=========================================
"""

import requests

from plugins.plugin_base import PluginBase


class WeatherPlugin(PluginBase):

    def __init__(self):

        super().__init__()

        self.name = "WeatherPlugin"

        self.version = "1.0.0"

        self.description = "Weather Information Plugin"

        self.base_url = "https://api.openweathermap.org/data/2.5/weather"

        self.api_key = None

    # ---------------------------------
    # Startup
    # ---------------------------------

    def start(self):

        print(f"{self.name} Started")

    # ---------------------------------
    # Shutdown
    # ---------------------------------

    def stop(self):

        print(f"{self.name} Stopped")

    # ---------------------------------
    # API Key
    # ---------------------------------

    def set_api_key(self, key):

        self.api_key = key

    # ---------------------------------
    # Weather
    # ---------------------------------

    def weather(self, city):

        if not self.api_key:

            return {

                "success": False,

                "message": "API Key not configured."

            }

        try:

            response = requests.get(

                self.base_url,

                params={

                    "q": city,

                    "appid": self.api_key,

                    "units": "metric"

                },

                timeout=10

            )

            data = response.json()

            if response.status_code != 200:

                return {

                    "success": False,

                    "message": data.get(

                        "message",

                        "Unknown Error"

                    )

                }

            return {

                "success": True,

                "city": data["name"],

                "country": data["sys"]["country"],

                "temperature": data["main"]["temp"],

                "feels_like": data["main"]["feels_like"],

                "humidity": data["main"]["humidity"],

                "pressure": data["main"]["pressure"],

                "weather": data["weather"][0]["main"],

                "description": data["weather"][0]["description"],

                "wind_speed": data["wind"]["speed"]

            }

        except Exception as error:

            return {

                "success": False,

                "message": str(error)

            }

    # ---------------------------------
    # Execute
    # ---------------------------------

    def execute(self, city="Delhi"):

        return self.weather(city)

    # ---------------------------------
    # Settings
    # ---------------------------------

    def settings(self):

        return {

            "api_key": self.api_key,

            "default_city": "Delhi"

        }

    # ---------------------------------
    # Health
    # ---------------------------------

    def health(self):

        return {

            "plugin": self.name,

            "enabled": self.enabled,

            "api": self.api_key is not None,

            "status": "OK"

        }


if __name__ == "__main__":

    plugin = WeatherPlugin()

    plugin.start()

    print(plugin.execute("Mumbai"))

    plugin.stop()
    
