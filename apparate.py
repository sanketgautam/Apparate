from spider import Spider
import pickle
from github import Github
import base64
from datetime import datetime
from credentials import * #contains all the passwords & tokens

file_path = "submissions.txt"

def stringToBase64(s):
    return base64.b64encode(s.encode('utf-8'))

def base64ToString(b):
    return base64.b64decode(b).decode('utf-8')

class Apparate:

    def __init__(self):
        self.submissions = []
        self.repo = None

        # Verifying that Submissions GitHub Repo exists
        g = Github(github_token)
        user = g.get_user()

        try:
            self.repo = user.get_repo(submissions_repo)
            print("Submissions Repo already exists")
        except Exception as e:
            if e._GithubException__status == 404:
                print("Submissions Repo not Found")
                self.repo = user.create_repo(name=submissions_repo, private=True, description="Collection of Solutions to various HackerRank Problems")
                self.repo.create_file("/README.md", "initial commit", "# " + submissions_repo)
                print("Repo & README.md created successfully")
            else:
                print("exception : ", e)

        #verifying that GitHub Repo contains submissions.txt
        try:
            c = self.repo.get_contents("submissions.txt")
            self.submissions = pickle.loads(c.decoded_content)
        except Exception as e:
            if e._GithubException__status == 404:
                print("submissions.txt doesn't exists")
                c = self.repo.create_file("/submissions.txt", "created submissions.txt", pickle.dumps(self.submissions))
                print("file created successfully")
            else:
                print("exception : ", e)

        print("submissions", self.submissions)
        print("submissions size", len(self.submissions))

    def check_updates(self):

        spider = Spider(hackerrank_username, hackerrank_password)
        if len(self.submissions) > 0:
            last_saved = self.submissions[0][4] #get all submissions after last_saved
        else:
            last_saved = -1 #get all the submissions
        spider.fetch_new_submissions(last_saved)

        new_submissions = spider.submissions

        if len(new_submissions) is 0:
            #no new submissions found
            return None, None

        print("{} new submission(s) found.".format(len(new_submissions)))
        print("Fetching code for new submissions...")
        codes = spider.fetch_code_for_submissions(new_submissions)

        return new_submissions, codes

    def create_submission_files(self, submissions, codes):
        # Deprecated: This method will not be used further
        #it'll iterate through and create individual files for each submission containing metadata and code
        #metadata parameters
        # -------------------------------------------------------
        #problem title: submission[0] > title
        #problem link: submission[2] > problem
        #author: hackerrank_username
        #language: submission[1] > language
        #code:
        # --------------------------------------------------------
        files = []
        print("Generating files for {} submission(s)...".format(len(submissions)))
        i = 1
        for submission in submissions:
            print(" - generating file for submission {} ".format(i))
            content = "-----------------------------------------------------------------------\n"
            content += "\nProblem Title: " + submission[0]
            content += "\nProblem Link: " + submission[2]
            content += "\nAuthor: " + hackerrank_username
            content += "\nLanguage : " + submission[1]
            content += "\n\n---------------------------------------------------------------------\n\n"
            content += "\n"+codes[submission]
            language = submission[1]
            file_directory = "submissions/"
            file_name = submission[0]
            file_extension = ""

            if "c++" in language.lower():
                file_extension = ".cpp"
            elif "java" in language.lower():
                file_extension = ".java"
            elif "python" in language.lower():
                file_extension = ".py"

            file = file_name + file_extension
            f = open(file_directory + file, 'w')
            f.write(content)
            f.close()
            files.append(file)
            i += 1

    def create_commit(self, submission, code):
        #it'll create a commit for newly added files
        title = submission[0]
        language = submission[1]
        link = submission[2]

        content = "-----------------------------------------------------------------------\n"
        content += "\nProblem Title: " + title
        content += "\nProblem Link: " + link
        content += "\nAuthor: " + hackerrank_username
        content += "\nLanguage : " + language
        content += "\n\n---------------------------------------------------------------------\n\n"
        content += "\n" + code

        file_directory = "/submissions/"
        file_name = title
        file_extension = ""

        if "c++" in language.lower():
            file_extension = ".cpp"
        elif "java" in language.lower():
            file_extension = ".java"
        elif "python" in language.lower():
            file_extension = ".py"

        file = file_name + file_extension
        file_path = file_directory + file

        # verifying that GitHub Repo contains file at filepath
        try:
            message = "updated " + file_name
            c = self.repo.get_file_contents(file_path)
            if c.decoded_content != content:
                print("  -- updating existing file")
                self.repo.update_file(file_path, message, content, c.sha)
        except Exception as e:
            if e._GithubException__status == 404:
                message = "added " + file_name
                print("  -- creating new file")
                self.repo.create_file(file_path, message, content)
                print("  -- file created successfully")
            else:
                print("exception : ", e)
        return file

    def update_repo(self, submissions, codes):
        files = []
        print("Updating repo for {} new submission(s)...".format(len(submissions)))
        i = 1
        for submission in submissions:
            print(" - updating repo with submission {}".format(i))
            file = self.create_commit(submission, codes[submission])
            files.append(file)
            i += 1

    def update_submissions(self, submissions):
        try:
            c = self.repo.get_file_contents("/submissions.txt")
            self.repo.update_file("/submissions.txt", "updated submissions.txt", pickle.dumps(submissions +
                                                                                              self.submissions), c.sha)
            print("submissions.txt updated successfully")
        except Exception as e:
            print("exception : ", e.with_traceback())

if __name__ == "__main__":
    # if check_updates == None
    #   return
    # create_submission_files
    # create_commit for changes
    # push changes to github
    #starting timer
    startTime = datetime.now()
    print(startTime.strftime("Executing Apparate on %a, %d %b %Y, %H:%M:%S"))

    apparate = Apparate()
    new_submissions, codes = apparate.check_updates()
    if new_submissions is not None:
        apparate.update_repo(new_submissions, codes)
        apparate.update_submissions(new_submissions)
    else:
        print("No new submissions found!")
        print("Nothing to update")

    #end timer
    diff = (datetime.now() - startTime).seconds
    minutes = diff//60
    seconds = diff - minutes*60

    print("Time taken to Apparate is {} min(s), {} sec(s)".format(minutes, seconds ))

    '''print(new_submissions, codes)
    if new_submissions is None:
        print("No new updates")
        exit(0)

    #creating new submissions files with metadata
    new_files = apparate.create_submission_files(new_submissions, codes)

    print("new_files", new_files)
    #updating the submissions record
    apparate.update_submissions(new_submissions)

    #commit these files in the local repo
    #loop through the new_files

    #for each file, if it doesn't exists
        #put/ create file in the repo with message "added submission ****"
    #if it exists, already
        #get the base64, remove new lines and decode it
        #compare with the new base64 encoded code
        #if there is a match
            #pass
        #else
            #update the existing file with message "updated submission ****"

    commit_message = "added "
    for file in new_files:
        commit_message +=file+", "
    commit_message = commit_message[:-2]
    '''
    # push these files in GitHUb repo
