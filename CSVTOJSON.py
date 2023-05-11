#!/usr/bin/env python
# coding: utf-8

# In[4]:


import sys
import pandas as pd                  #imported panda for transformation
import numpy as np                   #imported numpy for null function
import os as os                      #imported os to deal with windows with pathes 
import time                          #imported time to calculate time at start of function and at the end to calculate excution time
from urllib.parse import urlparse    #here imported urlparsing function to parse url directly
    
def json_csv_convertor(source_dir , target_dir=None ,  unix_time="no"):     #takes sourec dir as a much, target optional, unix_time optional, if not given then readable time
    start_time = time.time()                                                 #here to calculate the starting time
    def get_netloc(url):                                                     #here noticed that there is direct fields in the table not just url, so made function to distinguish, if it's a value return .path which contain the value of the url, if it has get_noc which is www.site.com, return it
        parsed_url = urlparse(url)                                           #here parsing the url and put it into variable
        if parsed_url.netloc:                                                #netloc field contain the url as www.site.com or similar, so checking if the field it self is a url or normal string
            return parsed_url.netloc
        else:
            return parsed_url.path                                           #if it's not url and it's a string then return it as it is, for example direct websites
    if not os.path.exists(source_dir):                                       #checking if the given destination exist on the source file device or not
        print(f"the location {source_dir} does not exist or entered wrong, please retry")
        return                                                               #return is needed so it return that message instead of error message 
    
    if target_dir is None:                                                   #if targetfile not given, then put the file with the source file
        target_dir = source_dir
    
    count = 0 ;                                                              #counting number of files made to make sure that all files are parsed, incase of any errors in big scale files
    for file_name in os.listdir(source_dir):                                 #now iterating in the directory for all files inside
        if file_name.endswith('.json'):                                      #filtering the files and excuting code only on json files
            temp_df = pd.read_json(os.path.join(source_dir, file_name),lines=True)
            temp_df = temp_df [['a', 'r', 'u', 'cy', 'll' , 'tz' , 't' , 'hc']]    #here brought from dataframe only the columns we need
            df_final = temp_df.rename(columns={'a': 'user_agent',
                            'r': 'from_url', 'u': 'to_url', 'cy': 'city', 'll': 'longitude_latitude' ,
                            'tz': 'time_zone' , 't': 'time_in', 'hc': 'time_out',
                            })                       #here renamed the columns as wanted and put it inside variable called df_final
            
            df_final[['web_browser', 'operating_sys']] = df_final['user_agent'].str.split(' ', n=1, expand=True)   #here we want to spilt the user_agent column into web_browser and operating_sys with n=1 means it spilts with space separator only once, and expand to make separate columns
            df_final['operating_sys'] = df_final['operating_sys'].str.extract(r'^(.*?)AppleWebKit') #here to extract only the windows part 
            df_final = df_final.drop(columns=['user_agent'])                  #after expanding the column, we don't need the main one so we delete it
            df_final['from_url'] = df_final['from_url'].apply(get_netloc)     #here applied the function to the from_url and to_url
            df_final['to_url'] = df_final['to_url'].apply(get_netloc)         #applying the function we just made it, to filter all urls or strings!
            df_final['longitude_latitude'] = df_final['longitude_latitude'].fillna('[0,0]')     #because we can't spilt null values, we put instead of nulls [0,0] then after expanding, willl replace it by nulls again
            df_final['longitude_latitude'] = df_final['longitude_latitude'].astype(str).apply(lambda x: x.strip('[]'))              #now converting it to string, then applying function that remove the brackets from it to spilt it easily
            df_final[['latitude', 'longitude']] = df_final['longitude_latitude'].str.split(',', expand=True).astype(float).round(2)  #here spilting the column of longitude_latitude into 2 columns of longitude and latitude, then converting it to number and rounding it to look better
            df_final['latitude'] = df_final['latitude'].replace(0, np.nan)                     #here replacing 0 by null back to let it come as it was
            df_final['longitude'] = df_final['longitude'].replace(0, np.nan) 
            df_final = df_final.drop('longitude_latitude', axis=1)                             #we don't need the main table now so dropping it
            df_final.dropna(subset=['city', 'longitude', 'latitude'], inplace=True)            #here we want to deal with null values, in my point of view, same records missing values, exist in the 3 column of it, after studying data, i see no value in replacing nulls of those columns by mean or mode, as it will make so unrealistic data, so for analysis i think removing it better
            mode = df_final['operating_sys'].mode()[0]                                         #for lacking of data in operating system, i think replacing it with mode is sufficint as we can do analysis with number easily, and it's not so important
            df_final['operating_sys'].fillna(mode, inplace=True)
            df_final = df_final.reset_index(drop=True)                                         #after deleting some rows, index was messed up so wanted to reset it
            if unix_time == "no":                                                                 #here the if condition that check if unix_time is false will change time, if true will keep it as numbers
                df_final['time_in'] = pd.to_datetime(df_final['time_in'], unit='s')            
                df_final['time_out'] = pd.to_datetime(df_final['time_out'], unit='s')
            
            csv_file_name = file_name.replace('.json', '.csv')                                 #here making the csv file name with .csv extentions
            count += 1                                                                         #counting the number of files converted
            print(f"* {file_name} converted to {csv_file_name} successfully")   
            duplicate_check = df_final.duplicated()                                            #checking if there is duplicates in files
            if duplicate_check.any():
                print(f"* File {file_name} has duplicates in : \n {df_final[duplicate_check]}")#if duplicates exist , will print message, a row for each duplicate showing the duplicate row
                df_final = df_final.drop_duplicates()                                          #since duplicate exist, we don't want exact duplicates!
            else:
                print(f"* file named {file_name} has no duplicates ")                     
            print(f"* Converted {len(df_final)} rows from {file_name} to {os.path.join(target_dir, csv_file_name)}.")  #here printing the rows that got transformed after removing duplicates of course
            df_final.to_csv(os.path.join(target_dir, csv_file_name))                           #saving the file to csv and we put it after duplicate to save files without duplicates

    print(f"* you converted total of {count} number of files from json to csv")                 #declaring amount of files transformed
    end_time = time.time()                                                                      #calculating ending time
    print(f"* Total execution time: {end_time - start_time:.4f} seconds")                       #calculating excuting of function time


def main():                                                                            #here the function main to be called in cmd when we call the function
    if len(sys.argv) <= 1:                                                             #checking if the source destination wasn't mentioned
        print("You haven't provided enough information. Please provide the source folder destination.")
    else:                                                                              
            source = sys.argv[1]                                                       #declaring variable called source to put destination of the source files inside
            if len(sys.argv) > 2 and sys.argv[2] == "-u" and len(sys.argv)<4:          #incase he put only the source and -u for unix time
                unix_time = True                                                       #unix time is true to change it
                target = None                                                          #target is none means he didnt provide by target and will take it as source
                json_csv_convertor(source,target, unix_time)                           
            elif len(sys.argv) > 5 and sys.argv[3] == "-t" and sys.argv[2] == "-u":    #incase he provides -u first then -t and target        
                unix_time = True
                target = sys.argv[4]                                                   #delcaring variable called target to put target destination inside
                json_csv_convertor(source,target,unix_time)
            elif len(sys.argv) > 3 and sys.argv[2] == "-t" and len(sys.argv) < 5:      #incase he put -t and target file only without -u, also handed error if he entered -t only without target file, will put int he source file with the args limit          
                target = sys.argv[3]                                           
                json_csv_convertor(source,target)
            elif len(sys.argv) > 3 and sys.argv[2] == "-t" and sys.argv[4] == "-u":    #incase he put -t first then target then -u
                unix_time = True
                target = sys.argv[3]
                json_csv_convertor(source,target, unix_time)
            
            else:
                json_csv_convertor(source)                                              #incase he give us only source or source with wrong paramter, tried to handle all possible errors, hope i could
                
if (__name__ == "__main__"):                                                            #here calling the function main that calls our function
    main ()

