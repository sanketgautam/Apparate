import re
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains

login_page_url = "https://www.hackerrank.com/login"
all_submissions_page_url = "https://www.hackerrank.com/submissions/all"
submissions_page_i_url = "https://www.hackerrank.com/submissions/all/page/"

cpp_formatter_url = "http://format.krzaq.cc/"

p = re.compile("[0-9]+$")

class Spider:

    def __init__(self, username, password):

        #initializing variables
        self.submissions = []
        self.start, self.end = 0, 0

        self.driver = webdriver.Firefox()
        self.driver.maximize_window()

        #logging into hackerrank account
        self.driver.get(login_page_url)
        login = self.driver.find_element_by_id("login")

        uname = login.find_element_by_name("login")
        uname.send_keys(username)

        passw = login.find_element_by_name("password")
        passw.send_keys(password)

        # Find the submit button using class name and click on it.
        login.find_element_by_name("commit").click()


    def fetch_pagination_params(self):

        # visit subimssions page
        self.driver.get(all_submissions_page_url)

        try:
            # getting the start and end for pagination
            pagination = self.driver.find_element_by_class_name("pagination").find_element_by_tag_name("ul")

            # skipping first two elements as they are previous and first buttton, which are disabled on first/current page
            self.start = int(str(
                pagination.find_element_by_css_selector("li:nth-child(3)").find_element_by_tag_name("a").get_attribute(
                    "href"))[-1])
            self.end = int(str(
                pagination.find_element_by_css_selector("li:last-child").find_element_by_tag_name("a").get_attribute(
                    "href"))[-1])

        except Exception as e:
            print(e)
            self.start, self.end = 0, 0

        print(self.start, self.end)


    def fetch_latest_submission(self):
        # Deprecated: no to be used without making changes
        # TODO: consider only accepted submissions
        self.driver.get(submissions_page_i_url + str(1))
        self.submissions = []

        try:
            list = self.driver.find_element_by_class_name("submissions-list-wrapper").find_elements_by_class_name("submissions_item")

            row = list[0]

            title = row.find_element_by_class_name("submissions-title").find_element_by_tag_name("a").get_attribute("text")
            language = row.find_element_by_class_name("submissions-language").find_element_by_tag_name("p").text
            problem = row.find_element_by_class_name("submissions-title").find_element_by_tag_name("a").get_attribute("href")
            result = row.find_element_by_class_name("span3").find_element_by_tag_name("p").text
            link = row.find_element_by_class_name("view-results").get_attribute("href")

            self.submissions.append((title, language, problem, result, link))

        except Exception as e:
            print(e)
            return -1
        return self.submissions[0]


    def fetch_new_submissions(self, last_saved):
        self.fetch_pagination_params()
        self.submissions = []

        if self.start is 0 or self.end is 0:
            return

        for i in range(self.start, self.end+1):
            self.driver.get(submissions_page_i_url + str(i))
            list = self.driver.find_element_by_class_name("submissions-list-wrapper").find_elements_by_class_name("submissions_item")

            for row in list:
                title = row.find_element_by_class_name("submissions-title").find_element_by_tag_name("a").get_attribute("text")
                language = row.find_element_by_class_name("submissions-language").find_element_by_tag_name("p").text
                problem = row.find_element_by_class_name("submissions-title").find_element_by_tag_name("a").get_attribute("href")
                result = row.find_element_by_class_name("span3").find_element_by_tag_name("p").text
                link = row.find_element_by_class_name("view-results").get_attribute("href")

                #current = int(p.findall(link)[0])
                if link == last_saved:
                    return
                #consider only accepted submissions
                if result != "Accepted":
                    continue
                self.submissions.append((title, language, problem, result, link))


    def fetch_code_for_submissions(self, submissions):

        codes = {}
        i = 1
        for submission in submissions:
            print(" - fetching code for submission {}".format(i))
            code = ""
            link = submission[4]
            self.driver.get(link)
            lines = self.driver.find_elements_by_css_selector("span[role=presentation]")
            for line in lines:
                    code += (line.text+"\n")
            codes[submission] = self.prettify_code(submission[1], code)
            i += 1
        return codes

    def prettify_code(self, language, code):

        pretty_code = code

        if "c++" in language.lower():
            self.driver.get(cpp_formatter_url)

            self.driver.find_element_by_name("code").send_keys(code)
            select = Select(self.driver.find_element_by_id('styleSelect'))
            select.select_by_visible_text('WebKit')
            self.driver.find_element_by_id("submitButton").click()
            time.sleep(2)
            pretty_code = self.driver.find_element_by_name("code").text

        return pretty_code

if __name__ == "__main__":
    spider = Spider()
    #latest_submission = spider.fetch_latest_submission()
    #print("latest_submission : ", latest_submission)
    #print("submissions length", len(spider.submissions))
    #print("submissions : ", spider.submissions)
    #print("-------------------------------------------------------------")
    spider.fetch_new_submissions(0)
    print("submissions length", len(spider.submissions))
    print("submissions : ", spider.submissions)
    print("--------------------------------------------------------------")
    codes = spider.fetch_code_for_submissions(spider.submissions)
    print(codes)
    #print(pretty_code)

if __name__ == "__maan__":

    driver.get(login_page_url)
    login  = driver.find_element_by_id("login")

    uname = login.find_element_by_name("login")
    uname.send_keys(username)

    passw = login.find_element_by_name("password")
    passw.send_keys(password)

    # Find the submit button using class name and click on it.
    login.find_element_by_name("commit").click()

    #visit subimssions page
    driver.get(all_submissions_page_url)

    #getting the start and end for pagination
    pagination = driver.find_element_by_class_name("pagination").find_element_by_tag_name("ul")

    #skipping first two elements as they are previous and first buttton, which are disabled on first/current page
    start = int(str(pagination.find_element_by_css_selector("li:nth-child(3)").find_element_by_tag_name("a").get_attribute("href"))[-1])
    end = int(str(pagination.find_element_by_css_selector("li:last-child").find_element_by_tag_name("a").get_attribute("href"))[-1])

    print(start, end)


    for i in range(start, end+1):
        driver.get(submissions_page_i_url+str(i))
        list = driver.find_element_by_class_name("submissions-list-wrapper").find_elements_by_class_name("submissions_item")

        for row in list:
            title = row.find_element_by_class_name("submissions-title").find_element_by_tag_name("a").get_attribute("text")
            language = row.find_element_by_class_name("submissions-language").find_element_by_tag_name("p").text
            problem = row.find_element_by_class_name("submissions-title").find_element_by_tag_name("a").get_attribute("href")
            result = row.find_element_by_class_name("span3").find_element_by_tag_name("p").text
            link = row.find_element_by_class_name("view-results").get_attribute("href")
            print(title, language, problem, result, link)

            submissions.append((title, language, problem, result, link))

    print(submissions)

    #wait for 5 secs
    #time.sleep(5)
    #driver.quit()

    '''
        Spider Class:
            - fetchLatestSubmission()
            - fetchNewSubmissions(last_saved) #pass -1 to fetch all submissions
            - fetchCodeForSubmissions(submissions)
             
        Decisions: 
         - The submissions[] array is stored in a text file named submissions.txt 
        
        Algorithm:
        - The initial value of last_saved is "-1".
        - Every time we run the script, do:
             - we find new submissions which are submitted after last_saved (top of submissions.txt)
             - if len(submissions) = 0
                    do nothing & exit
             - iterate over all new submissions and fetch the code for all new_submissions[] 
             - create files with code & metadata for each new submission
             - create new commit and push to GitHub
             - update the value of submissions[] array & last_saved with the top of submissions[]
    '''