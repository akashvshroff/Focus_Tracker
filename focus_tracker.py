import time
import schedule
import win32gui
from datetime import date, datetime
from collections import defaultdict
import smtplib
import sys
from smtp_details import *


class AutoTracker:
    def __init__(self, app_2_track, chrome_sites, send_mail):
        print("Starting now")
        self.app_2_track = app_2_track
        self.chrome_sites = chrome_sites
        # initialise email requirements
        self.todays_date = date.today()
        self.my_email = my_email
        self.send_mail = send_mail
        self.app_password = app_password
        self.conn = smtplib.SMTP('smtp.gmail.com', 587)
        self.conn.ehlo()
        self.conn.starttls()
        # Get your app password from https://support.google.com/accounts/answer/185833?hl=en
        self.conn.login(my_email, app_password)

        # initialise file updating
        self.fhand = open("Usage_Log.txt", 'a+')
        self.time_tracker()

    def get_window_name(self):
        for name in self.app_2_track:
            if name.lower() in self.wname.lower():
                if not name.lower() == 'chrome':  # checks what app
                    return name
                else:
                    if self.chrome_sites:  # if you've opted for multiple sites on chrome
                        for site in self.chrome_sites:
                            if site.lower() in self.wname.lower():
                                return site
                        return 'Chrome-Misc'
                    else:
                        return 'Chrome'
        return ''

    def time_tracker(self):
        self.usage = defaultdict(int)
        self.start = time.time()  # initialise timer
        self.prev = ''  # window that is being tracked i.e in focus
        self.prev_not_tracked = False  # if not tracked before
        self.time_now = datetime.now()
        self.end = datetime.combine(self.time_now, datetime.time.max)
        while self.end > self.time_now:  # stops at midnight
            self.time_now = datetime.now()
            window = win32gui.GetForegroundWindow()  # gets focus window
            self.wname = win32gui.GetWindowText(window)
            self.wn = self.get_window_name()
            if self.wn:  # False if the window was not meant to be tracked
                if self.prev_not_tracked:  # if you now use an app while last app wasn't tracked
                    self.start = time.time()
                    self.prev_not_tracked = False
                if self.prev:  # if not first time
                    if not self.prev == self.wn:  # change in focus window
                        self.usage[self.prev] += time.time() - self.start
                        self.prev, self.wn = self.wn, ''  # resetting the check
                        self.start = time.time()  # reset the timer
                else:  # first time or after a window that wasn't meant to be tracked
                    self.prev, self.wn = self.wn, ''  # initialising
            else:
                if self.prev:  # if you were tracking something
                    self.usage[self.prev] += time.time() - self.start
                    self.prev = ''
                self.prev_not_tracked = True  # because it's calculated the time for prev, tracking nothing now
            time.sleep(1)
        # for the last item that was being tracked
        self.usage[self.prev] += time.time() - self.start
        self.send_report()

    def print_report(self):  # mainly for debugging, isn't being called
        us = dict(self.usage)
        for i, (k, v) in enumerate(us.items()):
            i += 1
            s = int(v)
            t = '{:02}:{:02}:{:02}'.format(int(s / 3600), int(s / 60 % 60), s % 60)
            print('{}.{}:{}'.format(i, k.strip(), t))
        time.sleep(5)
        quit()

    def send_report(self):
        sub = 'Daily Report - {}'.format(self.todays_date)
        us = {k: v for k, v in sorted(dict(self.usage).items(),
                                      key=lambda item: item[1], reverse=True)}
        # sorts the usage in descending order
        body = 'Usage Amount:'
        body += '\n'
        for i, (k, v) in enumerate(us.items()):
            i += 1
            s = int(v)
            t = '{:02}:{:02}:{:02}'.format(int(s / 3600), int(s / 60 % 60), s % 60)
            body += '{}. {} - {}'.format(i, k.strip(), t)
            body += '\n'
        self.msg = '{}\n\n{}'.format(sub, body)
        mail = 'Subject:{}\n\n{}'.format(sub, body)
        self.conn.sendmail(self.my_email, self.send_mail, mail)
        self.conn.quit()
        self.update_file()

    def update_file(self):
        self.fhand.write("-"*15)
        self.fhand.write('\n')
        self.fhand.write(self.msg)
        self.fhand.write('\n')
        self.fhand.close()
        # self.print_report()


def main():
    global apps_list
    global chrome_list
    global send_email
    # gets all the necessary inputs from the user
    print("Welcome to the focus tracker! This is the primary set up")
    print("-"*20)
    print("Enter apps to track (only Chrome in browsers :\), separated by commas if more than 1")
    apps = input()
    apps_list = apps.split(',')
    chr_yes_or_no = False if not 'Chrome' in apps_list else True
    if chr_yes_or_no:
        print("If Chrome, do you want to track websites separately? Yes or No")
        ans = input()
        resp = False if ans.lower() == 'no' else True
        if resp:
            print("Enter sites on Chrome to track, again separated by commas")
            print("Apart from your sites, other Chrome usage will show as Chrome-Misc")
            cs = input()
            chrome_list = cs.split(',')
        else:
            chrome_list = []
    else:
        chrome_list = []
    print("Enter email to notify")
    send_email = input()


def driver():
    global apps_list
    global chrome_list
    global send_email
    try:
        AutoTracker(apps_list, chrome_list, send_email)
    except KeyboardInterrupt:
        print("Shutting down.")
        time.sleep(2)
        sys.exit()


if __name__ == '__main__':
    main()
    schedule.every().day.at("08:00").do(driver)  # starts at 8am
    while True:
        schedule.run_pending()
