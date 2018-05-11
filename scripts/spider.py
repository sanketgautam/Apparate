import time
from scripts.config import *
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.firefox.options import Options


class Spider:

    def __init__(self, username, password):

        # initializing variables
        self.submissions = []
        self.start, self.end = 0, 0

        options = Options()
        options.headless = True

        self.driver = webdriver.Firefox(firefox_options=options)
        logger.info("Headless Firefox Initialized")
        print("Headless Firefox Initialized")
        self.driver.maximize_window()

        # logging into HackerRank account
        self.driver.get(login_page_url)
        login = self.driver.find_element_by_id("login")

        uname = login.find_element_by_name("login")
        uname.send_keys(username)

        passw = login.find_element_by_name("password")
        passw.send_keys(password)

        # Find the submit button using class name and click on it.
        login.find_element_by_name("commit").click()

        # verifying that login was successful
        time.sleep(5)

        try:
            error = login.find_element_by_class_name("alert")
            if error.text == "Invalid login or password. Please try again.":
                logger.info("Unable to login to HackerRank, please verify username or password")
                print("Unable to login to HackerRank, please verify username / password or try again later")
                exit(1)
        except Exception:
            logger.info("HackerRank Login Successful")
            print("HackerRank Login Successful")

    def fetch_pagination_params(self):

        # visit submissions page
        self.driver.get(all_submissions_page_url)

        try:
            # getting the start and end for pagination
            pagination = self.driver.find_element_by_class_name("pagination").find_element_by_tag_name("ul")

            # skipping first two elements as they are previous(<) and first(<<) buttton,
            # which are disabled on current (all submissions) page
            self.start = int(str(
                pagination.find_element_by_css_selector("li:nth-child(3)").find_element_by_tag_name("a").get_attribute(
                    "href"))[-1])
            self.end = int(str(
                pagination.find_element_by_css_selector("li:last-child").find_element_by_tag_name("a").get_attribute(
                    "href"))[-1])

        except Exception as e:
            logger.error(e)
            print(e)
            self.start, self.end = 0, 0

        logger.info("pagination params, {} - {}".format(self.start, self.end))
        print("pagination params, {} - {}".format(self.start, self.end))

    def fetch_new_submissions(self, last_saved):
        self.fetch_pagination_params()
        self.submissions = []

        if self.start is 0 or self.end is 0:
            return

        for i in range(self.start, self.end + 1):
            self.driver.get(submissions_page_i_url + str(i))
            rows = self.driver.find_element_by_class_name("submissions-list-wrapper").find_elements_by_class_name(
                "submissions_item")

            for row in rows:
                title = row.find_element_by_class_name("submissions-title").find_element_by_tag_name(
                    "a").get_attribute("text")
                language = row.find_element_by_class_name("submissions-language").find_element_by_tag_name("p").text
                problem = row.find_element_by_class_name("submissions-title").find_element_by_tag_name(
                    "a").get_attribute("href")
                result = row.find_element_by_class_name("span3").find_element_by_tag_name("p").text
                link = row.find_element_by_class_name("view-results").get_attribute("href")

                # current = int(p.findall(link)[0])
                if link == last_saved:
                    return

                # consider only accepted submissions
                if result != "Accepted":
                    continue
                self.submissions.append((title, language, problem, result, link))

    def fetch_code_for_submissions(self, submissions):

        codes = {}
        i = 1
        for submission in submissions:
            logger.info(" - fetching code for submission {}".format(i))
            print(" - fetching code for submission {}".format(i))
            code = ""
            link = submission[4]
            self.driver.get(link)
            lines = self.driver.find_elements_by_css_selector("span[role=presentation]")
            for line in lines:
                code += (line.text + "\n")
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

    def quit_driver(self):
        self.driver.quit()


if __name__ == "__main__":
    spider = Spider()
    spider.fetch_new_submissions(0)  # 0 to fetch all accepted submissions
    print("new submissions : ", spider.submissions)
    print("new submissions length", len(spider.submissions))
    print("--------------------------------------------------------------")
    print("Fetching source codes for new submissions")
    codes = spider.fetch_code_for_submissions(spider.submissions)
    print(codes)
