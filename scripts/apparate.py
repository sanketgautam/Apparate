from scripts.spider import Spider
import pickle
from github import Github
from datetime import datetime
from scripts.config import logger
import click


class Apparate:

    def __init__(self):
        self.submissions = []
        self.repo = None

        # verifying GitHub authentication token
        try:
            g = Github(github_token)
            user = g.get_user()
            repos = user.get_key(1)  # dummy request to test authorization
            print(type(repos))
            print(dir(repos))
        except Exception as e:
            if e._GithubException__status == 401:  # unauthorized
                print("Unable to authenticate to GitHub, please verify token")
                logger.info("Unable to authenticate to GitHub, please verify token or try again later")
                exit(1)
        print("GitHub Authentication Successful")
        logger.info("GitHub Authentication Successful")

        # verifying that Submissions GitHub Repo exists
        try:
            self.repo = user.get_repo(submissions_repo)
            logger.info("Submissions Repo already exists")
            print("Submissions Repo already exists")
        except Exception as e:
            if e._GithubException__status == 404:
                logger.info("Submissions Repo not Found")
                print("Submissions Repo not Found")
                self.repo = user.create_repo(name=submissions_repo, private=False,
                                             description="Collection of Solutions to various HackerRank Problems")
                self.repo.create_file("/README.md", "initial commit", "# " + submissions_repo)
                logger.info("Repo & README.md created successfully")
                print("Repo & README.md created successfully")
            else:
                logger.exception(e)
                print("Exception : ", e)

        # verifying that GitHub Repo contains submissions.txt
        try:
            c = self.repo.get_contents("submissions.txt")
            self.submissions = pickle.loads(c.decoded_content)
        except Exception as e:
            if e._GithubException__status == 404:
                logger.info("submissions.txt doesn't exists")
                print("submissions.txt doesn't exists")
                c = self.repo.create_file("/submissions.txt", "created submissions.txt", pickle.dumps(self.submissions))
                logger.info("file created successfully")
                print("file created successfully")
            else:
                logger.exception(e)
                print("Exception : ", e)

        logger.info("submissions size {}".format(len(self.submissions)))
        print("submissions size", len(self.submissions))

    def check_updates(self):

        spider = Spider(hackerrank_username, hackerrank_password)
        if len(self.submissions) > 0:
            last_saved = self.submissions[0][4]  # get all submissions after last_saved
        else:
            last_saved = -1  # get all the submissions
        spider.fetch_new_submissions(last_saved)

        new_submissions = spider.submissions

        if len(new_submissions) is 0:
            # quit browser
            spider.quit_driver()
            # no new submissions found
            return None, None

        logger.info("{} new submission(s) found.".format(len(new_submissions)))
        logger.debug("Fetching code for new submissions...")

        print("{} new submission(s) found.".format(len(new_submissions)))
        print("Fetching code for new submissions...")
        codes = spider.fetch_code_for_submissions(new_submissions)

        # quit browser
        spider.quit_driver()

        return new_submissions, codes

    def create_commit(self, submission, code):
        # it'll create a commit for added or updated file
        title = submission[0]
        language = submission[1]
        link = submission[2]

        file_directory = "/submissions/"
        file_name = title
        file_extension = ""

        if "c++" in language.lower():
            file_extension = ".cpp"
        elif "java" in language.lower():
            file_extension = ".java"
        elif "python" in language.lower():
            file_extension = ".py"

        if file_extension != ".py":
            content = "/*-----------------------------------------------------------------------\n"
        else:
            content = "'''-----------------------------------------------------------------------\n"
        content += "\nProblem Title: " + title
        content += "\nProblem Link: " + link
        content += "\nAuthor: " + hackerrank_username
        content += "\nLanguage : " + language
        if file_extension != ".py":
            content += "\n\n-----------------------------------------------------------------------*/\n\n"
        else:
            content += "\n\n-----------------------------------------------------------------------'''\n\n"
        content += "\n" + code

        file = file_name + file_extension
        file_path = file_directory + file

        # verifying that GitHub Repo contains file at file_path
        try:
            message = "updated " + file_name
            c = self.repo.get_file_contents(file_path)
            if c.decoded_content != content:
                self.repo.update_file(file_path, message, content, c.sha)
                logger.info("  -- updated existing file")
                print("  -- updated existing file")
        except Exception as e:
            if e._GithubException__status == 404:
                message = "added " + file_name
                self.repo.create_file(file_path, message, content)
                logger.info("  -- created new file")
                print("  -- created new file")
            else:
                logger.exception(e)
                print("Exception : ", e)
        return file

    def update_repo(self, submissions, codes):
        files = []
        logger.debug("Updating repo for {} new submission(s)...".format(len(submissions)))
        print("Updating repo for {} new submission(s)...".format(len(submissions)))
        i = 1
        for submission in submissions:
            logger.info(" - updating repo with submission {}".format(i))
            print(" - updating repo with submission {}. {}".format(i, submission[0]))
            file = self.create_commit(submission, codes[submission])
            files.append(file)
            i += 1

    def update_submissions(self, submissions):
        try:
            c = self.repo.get_file_contents("/submissions.txt")
            self.repo.update_file("/submissions.txt", "updated submissions.txt", pickle.dumps(submissions +
                                                                                              self.submissions), c.sha)
            logger.info("submissions.txt updated successfully")
            print("submissions.txt updated successfully")
        except Exception as e:
            logger.exception(e)
            print("Exception : ", e)


@click.command()
@click.option("--repo", prompt=True, help="Name of GitHub repository to store submissions")
@click.option("--user", prompt=True, help="Username of your HackerRank account")
@click.option("--passwd", prompt=True, hide_input=True, help="Login Password of your HackerRank account")
@click.option("--token", prompt=True, help="GitHub Access Token with all repository privileges")
def apparate(repo, user, passwd, token):
    """ Tool to Synchronize HackerRank Submissions with GitHub """
    global submissions_repo, hackerrank_username, hackerrank_password, github_token
    submissions_repo = repo
    hackerrank_username = user
    hackerrank_password = passwd
    github_token = token

    startTime = datetime.now()
    logger.debug(startTime.strftime("Executing Apparate on %a, %d %b %Y, %H:%M:%S"))
    print(startTime.strftime("Executing Apparate on %a, %d %b %Y, %H:%M:%S"))

    try:
        apparate = Apparate()

        new_submissions, codes = apparate.check_updates()

        if new_submissions is not None:
            apparate.update_repo(new_submissions, codes)
            apparate.update_submissions(new_submissions)
        else:
            logger.info("No new submissions found!")
            logger.info("Nothing to update")

            print("No new submissions found!")
            print("Nothing to update")

    except Exception as e:

        logger.error("[FATAL Error] Unable to Apparate")
        logger.exception(e)
        print("[FATAL Error] Unable to Apparate", e)
        exit(1)  # exit indicating some issue/error/problem

    finally:

        # end timer
        diff = (datetime.now() - startTime).seconds
        minutes = diff // 60
        seconds = diff - minutes * 60

        logger.debug("Time taken to Apparate is {} min(s), {} sec(s)".format(minutes, seconds))
        print("Time taken to Apparate is {} min(s), {} sec(s)".format(minutes, seconds))


if __name__ == "__main__":
    apparate()
