# Stock Market Price Indicator

This is a Python application that utilizes the Financial Modeling Prep API. It notifies the user via an email and a system notification when a specified stock or cryptocurrency has crossed below a specified target. 

## Setup

1. Go to the Financial Modeling Prep [website](https://site.financialmodelingprep.com/developer) and create a free account
    - Go to 'Dashboard' to get your API key
    - **Note:** The free API allows a total of 250 request calls/day or 1 call every 6 minutes. Personally, I tune this based on what time I get on my computer and when I leave my computer to maximize the number of calls I can make.
2. Follow this [link](https://www.youtube.com/watch?v=g_j6ILT-X0k) to get your password to connect Python to your Gmail account
3. Make sure you have these modules imported: requests, ssl, smtplib, time, plyer, email.message
4. Fill all the missing information in (email sender/receiver, ticker, target, passwords) and you have yourself a fully customizable stock price indicator!

## Images
### Conditions:
![](/images/conditions.png)
### What occurs when price falls below target price:
![](/images/sys_noti.png)
![](/images/email2.png)
![](/images/email.png)

## Future Plans/Next steps

Many features such as price indication on Wealthsimple does not work on my outdated phone so I hope to create a mobile version of this project for which I can use on a daily basis.