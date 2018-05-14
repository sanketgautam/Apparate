# Apparate
Apparate is a command line tool to synchronize your HackerRank Accepted Submissions to your GitHub Repository.
Just write `apparate` on terminal, give it your credentials, sit-back and relax, it'll take care of the rest. 

You can also schedule a cron job to run apparate regularly & keep your submissions up to date.
```
Usage: apparate [OPTIONS]

Options:
  --repo TEXT    Name of GitHub repository to store submissions
  --user TEXT    Username of your HackerRank account
  --passwd TEXT  Login Password of you HackerRank account
  --token TEXT   GitHub Access Token with all repository privileges
  --help         Show this message and exit.

```

# Setup Instructions

It's built with Python Selenium and uses Firefox binary for fetching data from HackerRank. It used GitHub REST API v3 to manage submissions repository. 
Here are the instructions to install apparate on Ubuntu 16.04 LTS. Other platforms may have similar requirements. Feel free to skip any steps which your system already satisfies accordingly.

Steps: 
 - Environment Setup  
    - [Install python-dev and OpenSSL](#install-python-dev-and-openssl)
    - [Install Firefox Geckodriver](#install-firefox-geckodriver)
    - [Install Firefox Browser](#install-firefox-browser)
    - [Install Python3 and Pip3](#install-python3-and-pip3)
 
 - Apparate Setup
    - [Download and Install Apparate](#download-and-install-apparate)
    - [Validate and Test Installation](#validate-and-test-installation)

[Optional] : You may also want to schedule a cron job to run Apparate regularly. For that, follow these instructions,

 - Scheduling cron Job to update regularly
    
    - [Change to your Local Timezone](#change-to-your-local-timezone) (required for remote deployment, ex- AWS EC2 Instance)
    - [Schedule Cron Job](#schedule-cron-job)

# Contributions

Contributions are welcome to apparate to add support for more platforms (ex- Codefchef, Codeforces etc.), improve existing code, 
update documentation or add new features. To start contributing fork this repository, make changes and send a pull request with your changes. 
 
## Install python-dev and OpenSSL

First of all update & upgrade your system,

```sudo apt update && sudo apt upgrade```

Then install python-dev. It includes header files, a static library and development tools for building Python modules, extending the Python interpreter or embedding Python in applications.

```sudo apt-get install python-dev```

Install OpenSSL development package, It's implementation of the SSL and TLS cryptographic protocols for secure  communication over the Internet. It contains development libraries, header files, and manpages for libssl and libcrypto. 
    
 ```sudo apt-get install libssl-dev```
 
Also, install fake monitor in ubuntu for required for proper working of firefox & selenium,
 ```apt-get install xvfb```

## Install Firefox Geckodriver 
 
Firefox geckodriver required for selenium, 
1. Go to the [geckodriver releases page](https://github.com/mozilla/geckodriver/releases). 
Find the latest version of the driver for your platform (32 bit/ 64 bit) and download it. For example:

        wget https://github.com/mozilla/geckodriver/releases/download/v0.20.1/geckodriver-v0.20.1-linux64.tar.gz

2. Extract the file with:

        tar -xvzf geckodriver*

3. Make it executable:

        chmod +x geckodriver

4. Add the driver to your PATH so selenium can find it:
     add `export PATH=$PATH:/path-to-extracted-file/geckodriver` to your `~/.profile` and then execute `source ~/.profile` 

Test it by re-opening terminal & executing `geckodriver` from another directory. If that doesn't works, perform step 4 again with `~/.bashrc` file instead of `~/.profile`.

## Install Firefox Browser

Follow these instructions to install firefox [install Firefox 59 to avoid any compatibility issues]

1. Download The Latest Version of Firefox 59 from their FTP using wget

    - For 32 bit systems

        wget https://ftp.mozilla.org/pub/firefox/releases/59.0/linux-i686/en-US/firefox-59.0.tar.bz2

    - For 64 bit systems

        wget https://ftp.mozilla.org/pub/firefox/releases/59.0/linux-x86_64/en-US/firefox-59.0.tar.bz2

2. Extract the tar package

        tar -xjf firefox-59.0.tar.bz2

3. Move the Firefox folder to opt & remove the Older version of Firefox if it's there

        sudo rm -rf /opt/firefox58 (only if firefox58 is already installed)

        sudo mv firefox /opt/firefox59

4. Create the symbolic link for new Firefox

        sudo mv /usr/bin/firefox /usr/bin/firefoxold (only if any other version of firefox is already installed)

        sudo ln -s /opt/firefox59/firefox-bin /usr/bin/firefox
    
Verify installation by running `firefox --version`, if it throws any errors, then also install these required dependencies,

    sudo apt-get install libgtk-3.0
    sudo apt-get install xvfb 

## Install Python3 and Pip3

**Python3**: It is already installed on new versions of Ubuntu, if not it's easy to install using `apt-get`

**pip3**: Install it using apt as `sudo apt-get install python3-pip`

## Download and Install Apparate 

1. Clone or Download Apparate Repository
    
        git clone https://github.com/sanketgautam/Apparate.git

2. Now install `Apparate`  by executing following command inside Apparate/ directory 

         pip3 install --editable . (installing setup.py)
 

## Validate and Test Installation

To verify the installation, execute
    
        apparate --help

it should give the following output,
```
Usage: apparate [OPTIONS]

Options:
  --repo TEXT    Name of GitHub repository to store submissions
  --user TEXT    Username of your HackerRank account
  --passwd TEXT  Login Password of you HackerRank account
  --token TEXT   GitHub Access Token with all repository privileges
  --help         Show this message and exit.
  
```

Run and Test Apparate as follows.

    apparate --repo <Submissions_Repo_Name> --user <HackerRank_Username> --passwd <HackerRank_Password> --token <GitHub_Token> 

## Change to your Local Timezone
Most of the cloud virtual machine instances (ex- AWS EC2) use `UTC` by default. Before scheduling apparate with crontab, verify if your machine is using correct timezone, if not,
then change timezone of your machine to your local timezone.

For that, may use `timedatectl` as,

1. To list all available timezones use `timedatectl list-timezones`

2. To set timezone use `sudo timedatectl set-timezone Asia/Kolkata`

For example, to set machine timezone to `Asia/Kolkata`, you may run,
            
            sudo timedatectl set-timezone Asia/Kolkata
**Note:** To get cron to launch programs according to local time, I had to change `/etc/localtime` to be a symbolic link to the appropriate `tzfile` for my timezone, and then restart the cron service:

    mv /etc/localtime /etc/localtime.bak
    ln -s /usr/share/zoneinfo/Asia/Kolkata /etc/localtime
    service cron restart


## Schedule Cron Job

To schedule a cron job, you can write cron expressions.To learn more about cron jobs & scheduling follow this nice article by DigitalOcean - [How To Use Cron To Automate Tasks On a VPS](https://www.digitalocean.com/community/tutorials/how-to-use-cron-to-automate-tasks-on-a-vps)

To add a contjob `crontab -e` and write down your schedule expression & and the file. Also make sure to add PATH variable to your crontab file, so that apparate & geckodriver can be found. You can list all the scheduled crontabs of a user by `crontab -l`

Example cron file for apparate (to execute it daily at 4 AM):

```
# setting shell and path for execution 
SHELL=/bin/sh
PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin:/opt/

# apparte cron expression
0 4 * * * apparte --repo "Submissions_Repository_Name" --user "Your_HackerRank_Username" --passwd "Your_HackerRank_Password" --token "GitHub_Token" >> ~/cron_apparate.log 2>&1

```
Above given example cron jobs saves command logs to `cron_apparate.log` in users home directory.
