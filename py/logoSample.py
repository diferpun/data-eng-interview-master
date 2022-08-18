import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import validators
import sys
from logocrawler.functionslib import logo_collector

if __name__ == "__main__":
   logo_df = logo_collector(verbose=True,auth_param=True)

