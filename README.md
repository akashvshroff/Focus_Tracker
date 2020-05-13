# Outline
 * A customizable, automatic Windows-OS based time tracker that determines the primary application being used, i.e the window in focus and logs the usage time for user-determined applications and websites. It mails a daily report to an email chosen by the user,  and runs automatically the next day. It also logs the records to a txt file allowing for analysis at a later date. Detailed description below.

# Purpose
 * This project came about as I wanted to find a way to determine how much quality time, i.e focus time, I was spending on programming as I am currently a self taught programmer and I found that most available applications were not as customizable as I hoped and therefore I built my own. Through this undertaking, I could better understand the finer nuances of Python and fully appreciate libraries such as datetime, smtp, schedule and re.

# Description
 * The working principle of the program lies in its use of win32gui to check which window is in focus each second. It maintains note of the last window it was tracking and if the current window differs from the last window, it updates the logs of the last window using a defaultdict of the int category to ease storage and avoid key error validation. It then changes the previous window to then start tracking the current window.
 * The program must accomplish much more however. It's feature of tracking only certain user determined applications and websites which allows for optimization and only necessary info being given to the user means that it must effectively stop tracking and start again. This is accomplished by using the bool prev_not_tracked. If the window being used is not meant to be tracked, wn is set to '' by the get_window_name function, this leads to the prev_not_tracked being set to True and prev set to '' after the usage time for the prev window is updated.
 * In the time_tracker function, if the previous has not been tracked, start is reset and prev_not_tracked is set to the False. Then prev is checked. Prev essentially kicks in when the timer is running for the first time, or running after a site that wasn't meant to be tracked. If prev is True (i.e isn't '') and isn't the same as the current window, then the time is logged for the prev window and prev is set to the current window as explained in point 1. If prev is the same as the current window, that means the same window is being used and it continues automatically.
 * What is important to note is the while loop which runs until midnight for the current day, calculated using the datetime.combine function with datetime.time.max. The end (time) is compared to time_now which is calculated each iteration.
 * Once the code exits the while loop, the time for the prev window is updated once again as the last window has not had a chance to be updated yet.
 * Following which the send_report and update_file which send the report using the smtplib and log the data to a file respectively.
 * The tracking is housed in a class AutoTracker, the constructor for which sets the instance variables, the apps to track, chrome sites if any, mail to notify etc while also initialising the various connections.
 * The driver function creates an object of the class and is called upon every day at 8:30 AM using the schedule function housed in the if __main__ function.
 * Upon start-up of the program, the main() function is also called which gets user input for apps to track, chrome sites if any and email to notify. The email to notify is validated using regex.
 * These variables are global (not the cleanest I know, would love an alternative) and are called upon by the driver function when creating the instance.

 # P.S - Important
 - Currently this program only works on Windows as I do not have a linux or mac os device to test it on and I would love if anyone could help me with that. Moreover, I do not Firefox and have not included a separate section for it as I have for Chrome, however the code shouldn't vary too much.
 - Moreover, to install the dependancy win32gui, use the command 'pip install pywin32' as there will be a wheel error while instaling win32gui and it comes packaged with pywin32.
 - The smtp_details imported in the script is simply another python script that contains my email and app password.
