import logging
import re
import os.path

MAX_WAIT = 10

home = os.path.expanduser("~")
dir_path = os.path.join(home, '.logs')

if not os.path.exists(dir_path):
    os.makedirs(dir_path)

logging.basicConfig(filename=dir_path + "/apparate.log",
                    format='%(asctime)s %(message)s',
                    filemode='a')

logger = logging.getLogger()

# Setting the threshold of logger to DEBUG
logger.setLevel(logging.DEBUG)

# configuration for spider
login_page_url = "https://www.hackerrank.com/login"
all_submissions_page_url = "https://www.hackerrank.com/submissions/all"
submissions_page_i_url = "https://www.hackerrank.com/submissions/all/page/"

cpp_formatter_url = "http://format.krzaq.cc/"

p = re.compile("[0-9]+$")
