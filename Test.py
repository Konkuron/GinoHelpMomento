import pandas as pd
import numpy as np

#Creating all pandas Dataframes needed
Row_location = {}
DateRelation = pd.DataFrame()
Timeframe = pd.DataFrame({"Date": []})
Communication_errors = pd.DataFrame({"Communication error #": [], "Error log:": []})
Test1 = pd.read_csv("Test1.csv")
Test2 = pd.read_csv("Test2.csv")
Test3 = pd.read_csv("Test3.csv")
Test4 = pd.read_csv("Test4.csv")

#Creating the variables needed
Error_counter = 0
Number_of_inverters = 0
Oldest_Date = 10    #Given a bigger value than 0 for a fair comparison
Latest_Date = 0
Current_date = 0

#Asking for the number of inverters
Number_of_inverters = int(input("Ingresa el número de inversores:"))

#Filling the date relation dataframe with all dates
DateRelation["Date1"] = Test1["Date"]
DateRelation["Date2"] = Test2["Date"]
DateRelation["Date3"] = Test3["Date"]
DateRelation["Date4"] = Test4["Date"]

#Filling the date relation dataframe with all generation

#Verifying the outcome of DateRelation
print(DateRelation)

#Determining the oldest and latest date from all Dataframes
for n in range(Number_of_inverters):
    if Oldest_Date > DateRelation[f"Date{n+1}"].min():
        Oldest_Date = DateRelation[f"Date{n+1}"].min()
    if Latest_Date < DateRelation[f"Date{n+1}"].max():
        Latest_Date = DateRelation[f"Date{n+1}"].max()

#Verifying the output for the oldest and latest date
print(f"The oldest date found is {Oldest_Date}")
print(f"The latest date found is {Latest_Date}")

#Setting current date as the oldest as a starting point
Current_date = int(Oldest_Date)

#Calculating the range of dates taking into account the index starting point
Date_Range = Latest_Date - Oldest_Date + 1

#Filling in the time frame dataframe with dates from oldest to latest
for n in range(Date_Range):
    #Keeping current date up to date
    Current_date = Current_date
    Timeframe.loc[n, "Date"] = Current_date
    Current_date += 1

#Verifying the output for the time frame dataframe
print(Timeframe)

#Comparing all raw dataframes dates against the timeframe date
for n in range(Date_Range):

    #Copying the generation values in order by date from the raw dataframes to the time frame dataframe

    for y in range(len(Test1["Date"])):
        #First we verify that the dates match
        if (Timeframe["Date"][n] in Test1["Date"]) and (Timeframe["Date"][n] == Test1["Date"][y]):
            #Identifying the row location of the raw data in the raw dataframe 
            Row_location[n] = np.where(Test1["Date"] == Timeframe["Date"][n])
            print(Row_location)

            #Copying the raw data of generation to the time frame dataframe
            Timeframe.loc[n, "Generation 1"] = Test1.loc[Row_location[n][0][0], "Generation 1"]

        if (Timeframe["Date"][n] in Test2["Date"]) and (Timeframe["Date"][n] == Test2["Date"][y]):
            Row_location[n] = np.where(Test2["Date"] == Timeframe["Date"][n])
            print(Row_location)
            Timeframe.loc[n, "Generation 2"] = Test2.loc[Row_location[n][0][0], "Generation 2"]

        if (Timeframe["Date"][n] in Test3["Date"]) and (Timeframe["Date"][n] == Test3["Date"][y]):
            Row_location[n] = np.where(Test3["Date"] == Timeframe["Date"][n])
            print(Row_location)
            Timeframe.loc[n, "Generation 3"] = Test3.loc[Row_location[n][0][0], "Generation 3"]

        if (Timeframe["Date"][n] in Test4["Date"]) & (Timeframe["Date"][n] == Test4["Date"][y]):
            Row_location[n] = np.where(Test4["Date"] == Timeframe["Date"][n])
            Timeframe.loc[n, "Generation 4"] = Test4.loc[Row_location[n][0][0], "Generation 4"]

#Verifying the output of the time frame with all values in order
print(Timeframe)