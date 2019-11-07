Stocker-Application
A simple Django website to keep track of the stock market.

Getting Started
One needs to install django and all the files in requirements.txt to get the project up and running. Highly recommended to use a virtual enviornment.

Prerequisites/Installing
Start a virtual enviornment to start. Install all the files in requirements.txt in the virtual enviornment. Get your own IEX & Alphavantage api keys and substitute them in quotes/views.py. If you want to get the reset password working, simply substitute your Gmail id and password (you have to allow "less secure apps" in your account settings) in seetings.py. If you want to use Sendgrid, uncomment the codeblock in settings.py and substitute you apikey from sendgrid and install the following pakages:
sendgrid-django


