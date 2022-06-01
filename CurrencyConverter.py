
#this program utilizes the following python libraries
#pandas to read and interperet excel files
#requests to retrieve data from an url
#os to configure costum pathing
import pandas as pd
import requests as rq
import os

#the program imports the latest currency rates (USD)
#stores the rates under the name 'newrates' as a json file
#the json format allows us to easily use the data 
api = "https://api.exchangerate-api.com/v4/latest/USD"
response = rq.get(api)
newrates = response.json()

#using pandas to read the excel file
#using os to secure proper pathfinding independent of location
ccodes = pd.read_excel ((os.path.dirname(__file__)+"\CURRENCY_CODES.xlsx"),index_col=0)


#the program uses functions to limit the amount of lines of codes

#this function gives the exchange rate between to currencies using USD as the base
def exchangerate(x,y):
    #adds the upper() so the input does not need to be uppercase
    #this is used througout the program
    currencyfrom = (newrates["rates"][x.upper()])
    currencyto   = (newrates["rates"][y.upper()])           
    exchangerate.finalrate = (1/currencyfrom)*currencyto

#uses the previous function to convert a selected amount
def convert(x,y,z):
    exchangerate(x,z)
    convert.converted= y*exchangerate.finalrate

#returns the currency code of input country 
def check():
    #uses 'try except' to counter any invalid inputs
    try:
        cur=input("What country's currency code do you want to know?")
        #pandas converted the data into an array so it can be simply looked up
        ccode= (ccodes.loc[cur.upper(),'Code'])
        print("The curreny code of the currency usid in %s is %s"%(cur, ccode))
    except KeyError:
        print("You input does not match any country in our database.")


#the 'while True' loop is used troughout the program
#to loop back if input is invalid
#or to loop back to start the program over again   
while True:
    #Currency Converter's introduction interface
    #presents the available functions
    print("Welcome to this currency information programm!")
    print("These are the currently supported functions:")
    print(" [1] Find Currency Code")
    print(" [2] Find Exchange Rate")
    print(" [3] Convert Currency")
    print(" [4] Compare Exchange Rate Against Historical Rates")
    
    while True:
        selection=int(input("Please enter the number of the function you want to use:"))
        if selection == 1:
            print("you have selected: Find Currency Code")
            check()
            break

        if selection == 2:
            print("You have selected: Find Exchange Rate")
            while True:
                cur1=input("What is the currency you want to find the exchange rate for?") 
                cur2=input("Against what currency?")
                #since the function booth looks up values from an array
                #and uses a mathimatical equation
                #it is possible to get two different errors
                #hence try except looks for both key and attribute errors
                try:
                    exchangerate(cur1,cur2)
                    print("The current exchange rate from %s and %s is"%(cur1, cur2), exchangerate.finalrate) 
                    break
                except (KeyError, AttributeError) as error:
                    print("Your input is not a valid currency code, please try again.")
                    #allows the usage of check() since any mistake would root from invalid currency code 
                    ifcheck=input("You can check for currency codes by typing [?]")
                    if ifcheck == "?":
                        check()
            break  

        elif selection == 3:
            print("You have selected: Convert Currency")
            while True:
                cur1=input("Which currency would you like to convert?")
                while True:
                    #checks if the amount is compatible with the function before running it
                    #to distinguish errors from currency codes and amounts
                    try:
                        amt=float(input("What amount?"))
                        break
                    except ValueError:
                        print("please input a valid amount")
                cur2=input("To what currency?")
                try:
                    convert(cur1,amt,cur2)
                    print("For %d %s you get %d %s"%(amt, cur1, convert.converted, cur2))
                    break
                except (KeyError, AttributeError) as error:
                    print("Your input is not a valid currency code, please try again.")
                    ifcheck=input("You can check for currency codes by typing [?]")
                    if ifcheck == "?":
                        check()
            break 

        elif selection == 4:
            print("You have selected: Compare Exchange Rates Against Historical Rates")
            cur1=input("What currency do you want to check historical rates for?")
            cur2=input("What currency do you want to compare it to?")
            date=input("what date do you want to compare the current exchange rate to? [YYYY-MM-DD]")
            print("This process may take some time")
            
            #this section retrieves historical exchange rate data
            #has to be placed after the 'date' input
            oldurl = "https://api.apilayer.com/exchangerates_data/"+date+"&base=USD"
            payload = {}   
            headers= {"apikey": "npyPeVq9GUNvyU5gkGjBE0dK6VazKsvE"}
            oldresponse = rq.request("GET", oldurl, headers=headers, data = payload)
            oldrates=oldresponse.json()
            
            try:
                #finds the new exchange rates and the old ones
                #then calculates the change in percent
                exchangerate(cur1,cur2)
                oldcurrencyfrom = (oldrates["rates"][cur1.upper()])
                oldcurrencyto   = (oldrates["rates"][cur2.upper()])            
                oldrate = (1/oldcurrencyfrom)*oldcurrencyto
                change = float((exchangerate.finalrate-oldrate)/oldrate)
                change = change*100
                #checks if the change is positive or negative
                #in order to respond correctly 
                if change <= 0: 
                    change=change*-1
                    print("%s has depriciated %.4f percent to %s since %s"%(cur1.upper(),change,cur2.upper(),date))   
                elif change >= 0:
                    print("The %s has appreciated %.4f percent to %s since %s"%(cur1,change,cur2,date))    
                elif change == 0:
                    print("The rate is more or less the same")    

            except (KeyError, AttributeError) as error:
                print("Your input is invalid. Make sure your currency codes are correct, and the date has the format [YYYY-MM-DD].")
                ifcheck=input("You can check for currency codes by typing [?]")
                if ifcheck == "?":
                    check()
            break        
        else:
            print("please enter a valid input")
    #allows the user to go back to the start of the program
    while True:
        quit=input("Would you like to return to the main menu? (Yes/No)")
        if quit.upper() in ("YES", "NO"):
            break
    if quit.upper() == "NO":
        break
print("Thank you for using our program!")
