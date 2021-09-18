"""
Author: Niv Sahar
Last Updated: 05/09/2021
Summary:
    This is a script which gives us the full stack of the most common error from a log file or choosen one.
OS: Linux/Windows
"""

#import usefull libraries
import io, pandas as pd
import re,os
from datetime import datetime
from sys import exit
import sys


#dictionary for storing the errors with the amount of impressions.
error_dict = {}
#errors we should ignored
list_ignore_error = ["Failure during method invocation","Webservice GetCustomerOTT failed","Webservice GetCustomer360View failed","java.sql.SQLRecoverableException: Listener refused the connection with the following erro"]

if len(sys.argv) == 1:
        print("Please insert log file")
        exit()
elif os.stat(sys.argv[1]).st_size == 0:
        print("The file is empty")
        exit()
else:
        log_file = sys.argv[1]

def main():


    #total errors
    counter = 0

    #read the log file
    try:
        with open(log_file) as f:
            data_string = f.read()
    except IOError as e:
        #print the error
        print(e)
        #abort program
        exit()

    #convert the string to a dateframe
    data = io.StringIO(data_string)
    df = pd.read_csv(data, sep="\n")

    #run over all the lines of the log file.
    for i in range(0,len(df)):
        #if its error
        if 'ERROR' in df.iloc[i,0]:

            #get the type of the error
            m = re.search('c.k.'+'(.+?) -', df.iloc[i,0])

            if m and all(err not in df.iloc[i,0] for err in list_ignore_error):

                #sum of errors
                counter = counter + 1
                #insert the error to the dictionary, if he exist increase by 1 the amount of impressions.
                #else create a new key(error) with value(amount impressions) of 1.
                if m.group(1) in error_dict:
                    error_dict[m.group(1)] = error_dict[m.group(1)] + 1
                else:
                    error_dict[m.group(1)] = 1
    #if there is no errors, exit the program
    if counter == 0:
        print(log_file + ": contains no ERRORS")
        exit()
    #Take the error that appears most frequently in the log file
    max_error = max(error_dict, key=error_dict.get)
    stack_error = ""

    check = False

    #print the ERRORS that be founded and the amout
    print("ERRORS found:\n")

    for item in error_dict.items():
        if str(item[0]) == str(max_error):
            print("\033[31m{} \033[00m".format(str(item)))
        else:
            print(item)

    #print the total errors
    print('\nTotal critical ERRORS: ' + str(counter))

    #specific error for full stack.
    check_error = input("\nChoose ERROR for get full stack: ")

    # if we found errors
    if check_error != "":
        #extract the full stack error for the specific error we found.
        for i in range(0,len(df)-1):
            if 'ERROR' in df.iloc[i,0] and check_error in df.iloc[i,0]:
                check = True
            if 'ERROR' in df.iloc[i+1,0] or 'INFO' in df.iloc[i+1,0]:
                if stack_error != "":
                    break
                else:
                    check = False
            if check:
                # build the full stack error
                stack_error = stack_error + str(df.iloc[i,0]) + "\n"

        #get the current time
        # now = datetime.now()
        # current_time = now.strftime("%d.%m.%Y")

        #create the file and insert it the results of the full stack error.
        #try and catch exception, if there an error
        try:
            if stack_error != "":
                print("\n" + stack_error)
                #f = open("stack_error_"+current_time+".txt","w+")
                #print to the terminal the results
                #if f:                    
                #    print("\nfull stack error output file, Successfully created!")

                #if f:
                #    f.write(str(datetime.now())+"\n")
                #    f.write("\n")
                #    f.write(stack_error)
                #    f.close()
            else:
                print()
                print(check_error + " ERROR full stack not found...")
                exit()

        except IOError as e:
            #print the error
            print("Something went wrong: " + e)
            #abort program
            exit()
    else:
        #print exception
        print("\nthere is no full stack for empty string, EXIT...")
        exit()


#main function
if __name__ == "__main__":
    main()
