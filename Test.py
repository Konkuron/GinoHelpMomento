import pandas as pd
import numpy as np

#Creating all pandas Dataframes needed
Row_location = {}
DateRelation = pd.DataFrame()
Timeframe = pd.DataFrame({"Date": []})
Errors = pd.DataFrame({"Location of the error": [],"Error type": [], "Error log": []})
Test1 = pd.read_csv("Test1.csv")
Test2 = pd.read_csv("Test2.csv")
Test3 = pd.read_csv("Test3.csv")
Test4 = pd.read_csv("Test4.csv")

#Creating the variables needed
Error_counter = 0
Number_of_inverters = 0
Oldest_Date = 100    #Given a bigger value than 0 for a fair comparison
Latest_Date = 0
Current_date = 0
Date_Range = 0
Error_counter = 0

#Asking for the number of inverters
Number_of_inverters = int(input("Ingresa el número de inversores:"))

#Filling the date relation dataframe with all dates
DateRelation["Date1"] = Test1["Date"]
DateRelation["Date2"] = Test2["Date"]
DateRelation["Date3"] = Test3["Date"]
DateRelation["Date4"] = Test4["Date"]

#Verifying the outcome of DateRelation
print(DateRelation)

#Determining the oldest and latest date within all Dataframes
for n in range(Number_of_inverters):
    for x in range(len(DateRelation[f"Date{n+1}"])):
        if (Oldest_Date > DateRelation[f"Date{n+1}"].min()):
            Oldest_Date = DateRelation[f"Date{n+1}"].min()
        if (Latest_Date < DateRelation[f"Date{n+1}"].max()):
            Latest_Date = DateRelation[f"Date{n+1}"].max()

#Verifying the output for the oldest and latest date
print(f"La fecha más vieja registrada entre todos los inversores fue {Oldest_Date}")
print(f"La fecha más nueva registrada entre todos los inversores fue {Latest_Date}")

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
    
#Stamping the generation raw data into the time frame dataframe and error detection data into the errors dataframe
#Comparing all raw dataframes dates against the timeframe date
for y in range(len(Test1["Date"])):

    #Copying the generation values in order by date from the raw dataframes to the time frame dataframe

    for n in range(Date_Range):

        #First we verify that the dates match
        if (Timeframe["Date"][n] in Test1["Date"]) and (Timeframe["Date"][n] == Test1["Date"][y]):
            #Identifying the row location of the raw data in the raw dataframe 
            Row_location[n] = np.where(Test1["Date"] == Timeframe["Date"][n])

            #Data has good quality condition met
            if Test1.loc[Row_location[n][0][0], "Quality"] == 0:
                Timeframe.loc[n, "Generation 1"] = Test1.loc[Row_location[n][0][0], "Generation"]
            
            #Data was lost due to telemetry failure
            if Test1.loc[Row_location[n][0][0], "Quality"] == 2:
                Errors.loc[Error_counter, "Location of the error"] = Row_location[n][0][0] + 1
                Errors.loc[Error_counter, "Error type"] = 2
                Errors.loc[Error_counter, "Error log"] = "The data was lost due to telemetry failure."
                Error_counter += 1

            #Setting a negative value as a code for error 2
                Timeframe.loc[n, "Generation 1"] = -2

            #Data was manually set (not relyable)
            if Test1.loc[Row_location[n][0][0], "Quality"] == 4:
                Errors.loc[Error_counter, "Location of the error"] = Row_location[n][0][0] + 1
                Errors.loc[Error_counter, "Error type"] = 4
                Errors.loc[Error_counter, "Error log"] = "The data was manually set."
                Error_counter += 1

            #Setting a negative value as a code for error 4
                Timeframe.loc[n, "Generation 1"] = -4

            #Data was externally modified
            if Test1.loc[Row_location[n][0][0], "Quality"] == 6:
                Errors.loc[Error_counter, "Location of the error"] = Row_location[n][0][0] + 1
                Errors.loc[Error_counter, "Error type"] = 6
                Errors.loc[Error_counter, "Error log"] = "The sample value was externally modified."
                Error_counter += 1

            #Setting a negative value as a code for error 6
                Timeframe.loc[n, "Generation 1"] = -6
            
            #Data was taken more than 15 seconds late
            if Test1.loc[Row_location[n][0][0], "Quality"] == 7:
                Errors.loc[Error_counter, "Location of the error"] = Row_location[n][0][0] + 1
                Errors.loc[Error_counter, "Error type"] = 7
                Errors.loc[Error_counter, "Error log"] = "The sample was taken more than 15 seconds late."
                Error_counter += 1

            #Setting a negative value as a code for error 7
                Timeframe.loc[n, "Generation 1"] = -7

        if (Timeframe["Date"][n] in Test2["Date"]) and (Timeframe["Date"][n] == Test2["Date"][y]):
            Row_location[n] = np.where(Test2["Date"] == Timeframe["Date"][n])
            
            if Test2.loc[Row_location[n][0][0], "Quality"] == 0:
                Timeframe.loc[n, "Generation 2"] = Test2.loc[Row_location[n][0][0], "Generation"]

            if Test2.loc[Row_location[n][0][0], "Quality"] == 2:
                Errors.loc[Error_counter, "Location of the error"] = Row_location[n][0][0] + 1
                Errors.loc[Error_counter, "Error type"] = 2
                Errors.loc[Error_counter, "Error log"] = "The data was lost due to telemetry failure."
                Error_counter += 1

            #Setting a negative value as a code for error 2
                Timeframe.loc[n, "Generation 2"] = -2

            if Test2.loc[Row_location[n][0][0], "Quality"] == 4:
                Errors.loc[Error_counter, "Location of the error"] = Row_location[n][0][0] + 1
                Errors.loc[Error_counter, "Error type"] = 4
                Errors.loc[Error_counter, "Error log"] = "The data was manually set."
                Error_counter += 1

            #Setting a negative value as a code for error 4
                Timeframe.loc[n, "Generation 2"] = -4

            if Test2.loc[Row_location[n][0][0], "Quality"] == 6:
                Errors.loc[Error_counter, "Location of the error"] = Row_location[n][0][0] + 1
                Errors.loc[Error_counter, "Error type"] = 6
                Errors.loc[Error_counter, "Error log"] = "The sample value was externally modified."
                Error_counter += 1

            #Setting a negative value as a code for error 6
                Timeframe.loc[n, "Generation 2"] = -6
            
            if Test2.loc[Row_location[n][0][0], "Quality"] == 7:
                Errors.loc[Error_counter, "Location of the error"] = Row_location[n][0][0] + 1
                Errors.loc[Error_counter, "Error type"] = 7
                Errors.loc[Error_counter, "Error log"] = "The sample was taken more than 15 seconds late."
                Error_counter += 1

            #Setting a negative value as a code for error 7
                Timeframe.loc[n, "Generation 2"] = -7

        if (Timeframe["Date"][n] in Test3["Date"]) and (Timeframe["Date"][n] == Test3["Date"][y]):
            Row_location[n] = np.where(Test3["Date"] == Timeframe["Date"][n])

            if Test3.loc[Row_location[n][0][0], "Quality"] == 0:
                Timeframe.loc[n, "Generation 3"] = Test3.loc[Row_location[n][0][0], "Generation"]

            if Test3.loc[Row_location[n][0][0], "Quality"] == 2:
                Errors.loc[Error_counter, "Location of the error"] = Row_location[n][0][0] + 1
                Errors.loc[Error_counter, "Error type"] = 2
                Errors.loc[Error_counter, "Error log"] = "The data was lost due to telemetry failure."
                Error_counter += 1

            #Setting a negative value as a code for error 2
                Timeframe.loc[n, "Generation 3"] = -2
            
            if Test3.loc[Row_location[n][0][0], "Quality"] == 4:
                Errors.loc[Error_counter, "Location of the error"] = Row_location[n][0][0] + 1
                Errors.loc[Error_counter, "Error type"] = 4
                Errors.loc[Error_counter, "Error log"] = "The data was manually set."
                Error_counter += 1

            #Setting a negative value as a code for error 4
                Timeframe.loc[n, "Generation 3"] = -4
            
            if Test3.loc[Row_location[n][0][0], "Quality"] == 6:
                Errors.loc[Error_counter, "Location of the error"] = Row_location[n][0][0] + 1
                Errors.loc[Error_counter, "Error type"] = 6
                Errors.loc[Error_counter, "Error log"] = "The sample value was externally modified."
                Error_counter += 1

            #Setting a negative value as a code for error 6
                Timeframe.loc[n, "Generation 3"] = -6
            
            if Test3.loc[Row_location[n][0][0], "Quality"] == 7:
                Errors.loc[Error_counter, "Location of the error"] = Row_location[n][0][0] + 1
                Errors.loc[Error_counter, "Error type"] = 7
                Errors.loc[Error_counter, "Error log"] = "The sample was taken more than 15 seconds late."
                Error_counter += 1

            #Setting a negative value as a code for error 7
                Timeframe.loc[n, "Generation 3"] = -7

        if (Timeframe["Date"][n] in Test4["Date"]) and (Timeframe["Date"][n] == Test4["Date"][y]):
            Row_location[n] = np.where(Test4["Date"] == Timeframe["Date"][n])

            if Test4.loc[Row_location[n][0][0], "Quality"] == 0:
                Timeframe.loc[n, "Generation 4"] = Test4.loc[Row_location[n][0][0], "Generation"]

            if Test4.loc[Row_location[n][0][0], "Quality"] == 2:
                Errors.loc[Error_counter, "Location of the error"] = Row_location[n][0][0] + 1
                Errors.loc[Error_counter, "Error type"] = 2
                Errors.loc[Error_counter, "Error log"] = "The data was lost due to telemetry failure."
                Error_counter += 1

            #Setting a negative value as a code for error 2
                Timeframe.loc[n, "Generation 4"] = -2

            if Test4.loc[Row_location[n][0][0], "Quality"] == 4:
                Errors.loc[Error_counter, "Location of the error"] = Row_location[n][0][0] + 1
                Errors.loc[Error_counter, "Error type"] = 4
                Errors.loc[Error_counter, "Error log"] = "The data was manually set."
                Error_counter += 1

            #Setting a negative value as a code for error 4
                Timeframe.loc[n, "Generation 4"] = -4
            
            if Test4.loc[Row_location[n][0][0], "Quality"] == 6:
                Errors.loc[Error_counter, "Location of the error"] = Row_location[n][0][0] + 1
                Errors.loc[Error_counter, "Error type"] = 6
                Errors.loc[Error_counter, "Error log"] = "The sample value was externally modified."
                Error_counter += 1

            #Setting a negative value as a code for error 6
                Timeframe.loc[n, "Generation 3"] = -6

            if Test4.loc[Row_location[n][0][0], "Quality"] == 7:
                Errors.loc[Error_counter, "Location of the error"] = Row_location[n][0][0] + 1
                Errors.loc[Error_counter, "Error type"] = 7
                Errors.loc[Error_counter, "Error log"] = "The sample was taken more than 15 seconds late."
                Error_counter += 1

            #Setting a negative value as a code for error 7
                Timeframe.loc[n, "Generation 4"] = -7

#Verifying the output of the time frame with all values in order
print(Timeframe)

#Verifying the output of the Errors 
print(Errors)

#Improvements to be made:
#- Change the date format from a single numeric value to a full date format
#- Add error detection via data analysis (Values that are too high, Frozen values, Unexpected negative values)
