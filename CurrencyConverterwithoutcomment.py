import pandas as pd
import requests as rq
import os

api = "https://api.exchangerate-api.com/v4/latest/USD"
response = rq.get(api)
newrates = response.json()
ccodes = pd.read_excel ((os.path.dirname(__file__)+"\CURRENCY_CODES.xlsx"),index_col=0)

def exchangerate(x,y):
    currencyfrom = (newrates["rates"][x.upper()])
    currencyto   = (newrates["rates"][y.upper()])           
    exchangerate.finalrate = (1/currencyfrom)*currencyto
def convert(x,y,z):
    exchangerate(x,z)
    convert.converted= y*exchangerate.finalrate
def check():
    try:
        cur=input("What country's currency code do you want to know?")
        ccode= (ccodes.loc[cur.upper(),'Code'])
        print("The curreny code of %s is %s"%(cur, ccode))
    except KeyError:
        print("You input does not match any country in our database. Please try again")


print("Welcome to this currency information programm!")
print("These are the currently supported functions:")
print(" [1] Find currency ticker ")
print(" [2] Find exchange rate")
print(" [3] Convert currency")
print(" [4] compare exchange rate to previous years")

while True:
    while True:
        selection=int(input("Please enter the number of the function you want to use:"))
        
        if selection == 1:
            print("you have selected: 'find currency code'")
            check()
            break

        if selection == 2:
            print("you have selected 'Find exchange rate'")
            while True:
                cur1=input("What is the currency you want to convert?") 
                cur2=input("To what currency?")
                try:
                    exchangerate(cur1,cur2)
                    print("The current exchangerate from %s to %s is"%(cur1, cur2), exchangerate.finalrate) 
                    break
                except (KeyError, AttributeError) as error:
                    print("Your input is not a valid currency code, please try again.")
                    ifcheck=input("You can check for currency codes by typing [?]")
                    if ifcheck == "?":
                        check()
            break  

        elif selection == 3:
            while True:
                cur1=input("What is the currency you want to convert?")
                while True:
                    try:
                        amt=float(input("How much?"))
                        break
                    except ValueError:
                        print("please input a valid amount")
                cur2=input("To what currency?")
                try:
                    convert(cur1,amt,cur2)
                    print("For %d %s you get %d %s"%(amt, cur1, convert.converted, cur2))
                    break
                except (KeyError, AttributeError) as error:
                    print("Your input is not a valid currency code, please try again. You can check for currency codes by typing [?]")
                    ifcheck=input("You can check for currency codes by typing [?]")
                    if ifcheck == "?":
                        check()
            break 

        elif selection == 4:
            
            cur1=input("What currency do you want to look at?")
            cur2=input("What currency do you want to compare it to?")
            date=input("what date do you want to compare it to? [YYYY-MM-DD]")
            print("this process may take some time")
            oldurl = "https://api.apilayer.com/exchangerates_data/"+date+"&base=USD"
            payload = {}   
            headers= {"apikey": "npyPeVq9GUNvyU5gkGjBE0dK6VazKsvE"}
            oldresponse = rq.request("GET", oldurl, headers=headers, data = payload)
            oldrates=oldresponse.json()
            
            try:
                exchangerate(cur1,cur2)
                oldcurrencyfrom = (oldrates["rates"][cur1.upper()])
                oldcurrencyto   = (oldrates["rates"][cur2.upper()])            
                oldrate = (1/oldcurrencyfrom)*oldcurrencyto
                change = float((exchangerate.finalrate-oldrate)/oldrate)
                if change <= 0: 
                    change=change*-1
                    print("The %s has depriciated %.4f to the %s since %s"%(cur1.upper(),change,cur2.upper(),date))   
                elif change >= 0:
                    print("The %s has appreciated %.4f percent to the %s since %s"%(cur1,change,cur2,date))    
                elif change == 0:
                    print("the rate is more or less the same")    

            except (KeyError, AttributeError) as error:
                print("Your input is invalid. Make sure your currency codes are correct, and the date has the format [YYYY-MM-DD].")
                ifcheck=input("You can check for currency codes by typing [?]")
                if ifcheck == "?":
                    check()
            break        
        else:
            print("please enter a valid input")

    while True:
        quit=input("Do you want to start again? (Yes/No)")
        if quit.upper() in ("YES", "NO"):
            break
    if quit.upper() == "NO":
        break
print("Thank you for using our program!")
