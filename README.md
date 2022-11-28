# Stock Market Price Indicator

This is a Python application that utilizes the Financial Modeling Prep API. It notifies the user via an email and a system notification when a specified stock or cryptocurrency has crossed below a specified target. The GUI is created using PySimpleGUI.

## Setup

1. Go to the Financial Modeling Prep [website](https://site.financialmodelingprep.com/developer) and create a free account
    - Go to 'Dashboard' to get your API key
    - **Note:** The free API allows a total of 250 request calls/day or 1 call every 6 minutes. Personally, I tune this based on what time I get on my computer and when I leave my computer to maximize the number of calls I can make.
2. Follow this [link](https://www.youtube.com/watch?v=g_j6ILT-X0k) to get your password to connect Python to your Gmail account
3. Make sure you have all the modules imported from the requirements.txt file

## Images
### GUI:
![](/images/GUI.png)
### What occurs when price goes below/above target price:
![](/images/GUIbuyLow.png)
![](/images/systemNotification)
![](/images/emailNotification.png)
![](/images/emailDetails.png)
![](/images/SMSNotification.jpg)

## Future Plans/Next steps

**UPDATE:** I have made a GUI using PySimpleGUI to display the information in a more aesthetically pleasing manner rather sticking to a terminal-based app.

Many features such as price indication on Wealthsimple does not work on my outdated phone so I hope to create a mobile version of this project for which I can use on a daily basis.