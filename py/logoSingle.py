import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import validators
import sys
from logocrawler.functionslib import get_icon

if __name__ == "__main__":

      for line in sys.stdin:
       if 'q' == line.rstrip():
           break
       img_url = get_icon(line, auth_param=False, tout=5)
       sys.stdout.flush()
       sys.stdout.write(f"{img_url}\n")

