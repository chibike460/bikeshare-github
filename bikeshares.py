import time
import pandas as pd
import numpy as np
import datetime
import calendar

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
	"""
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """

	print('Hello! Let\'s explore some US bikeshare data!')
	# get user input for city (chicago,  new york city, washington). HINT: Use a while loop to handle invalid inputs

	#Defining the variable "city" as an input
	city = input('Please indicate what Bikeshare city you would like to explore. Kindly choose between: Chicago, New York City or Washington\n').lower()
	while city not in ('chicago', 'new york city', 'washington'):
		print('That\'s not  a valid city. Try again!\n')
		city = input('Please indicate what Bikeshare city you would like to explore. Kindly choose between: Chicago, New York City or Washington\n').lower()

	#Defining variable "month" as an input
	month = input("Would you like to sort your data by month?\nIf yes, kindly input any month from January through June.\nIf you do not want to sort by any month, type 'All.'\n").lower()
	while month not in ('january', 'february', 'march', 'april', 'may', 'june', 'all'):
		print("That\'s not a valid month. Try again! ")
		month = input("Would you like to sort your data by month?\nIf yes, kindly input any month from January through June.\nIf you do not want to sort by any month, type 'all'\n").lower()

		#Defining variable "day" as an output
	day = input("Would you like to sort your data by day?\nIf yes, input day of choice. e.g: Sunday. Or type 'All' to sort by no day filter.\n").lower()
	while day not in ('monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all'):
		print('Thats not a valid day. Try Again! ')
		day = input("Would you like to sort your data by day?\nIf yes, input day of choice. e.g: Sunday. Or type 'All' to sort by no day filter.\n").lower()

	print('_'*40)
	return city, month, day

def load_data(city, month, day):
	"""
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    #Load data file into dataframe
	df = pd.read_csv(CITY_DATA[city])

	#Convert [Sart Time] column to datetime module
	df['Start Time'] = pd.to_datetime(df['Start Time'], infer_datetime_format=True)

	#Create new column of DOW - Day of week and Month, by extracting Month and DOW from Start Time
	df['month'] = df['Start Time'].dt.month
	df['day_of_week'] = df['Start Time'].dt.weekday_name

	#Filtering by month if applicable!
	if month != 'all':
		months = ['january', 'february', 'march', 'april', 'may', 'june']
		month = months.index(month) + 1
		#Getting new dataframe by filtering month
		df= df[df['month']==month]

	#Filtering by day_of_week if applicable!'
	if day != 'all':
		#Getting new dataframe by filtering DOW
		day = df[df['day_of_week']==day.title()]

	return df

def clean_headings(df):
    """This function cleans the column heads for an efficient code run"""

    ##clean up column headings
    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_').str.replace('(', '').str.replace(')', '')

def time_stats(df):
	"""Displays statistics on the most frequent times of travel."""

	print('\nCalculating The Most Frequent Times of Travel...\n')
	start_time = time.time()



	# display the most common month
	print("The most common month of hire is: \n")
	#Setting Month to Real Month Names
	df['month'] = df['month'].apply(lambda x: calendar.month_name[x])
	mode_of_month = df.month.mode()
	print(mode_of_month.iloc[0])

	#Display the most common day of week
	print("The most common day of week bikes were hired is: \n")
	print(df.day_of_week.mode().iloc[0])

	# Display the most common start hour
	print("\nThe most common time a bike is hired is: ")
	start_time_mode = df.start_time.mode().iloc[0]
	print(start_time_mode.strftime('%X'))

	print("\nThis took %s seconds." % (time.time() - start_time))
	print('_'*40)

def station_stats(df):

    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')

    start_time = time.time()

    # Display most commonly used start station
    print('The start station with the highest use rate is:\n')
    print(df.start_station.mode().iloc[0])

    # Display most commonly used end station
    print('\nThe end station with the highest use rate is: \n')
    print(df.end_station.mode().iloc[0])

    # Display most frequent combination of start station and end station trip
    print('\nThe most frequent start and end station combo is: ')

    df['start_end_station'] = 'From ' + df['start_station'] + ' to ' + df['end_station']
    print(df['start_end_station'].mode().iloc[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('_'*40)

def trip_duration_stats(df):
	"""Displays statistics on the total and average trip duration."""
	print('\nCalculating Trip Duration...\n')
	start_time = time.time()

	#Display total travel time
	print("The total travel time in hours is: \n")
	print(round((df.trip_duration.sum() / 3600)))

	#Display mean travel time
	print("\nThe average travel time in seconds is: \n")
	print(round((df.trip_duration.mean()), 1))
	print("\nThis took %s seconds." % (time.time() - start_time))
	print('_'*40)

def user_stats(df):
	"""Displays statistics on bikeshare users."""

	df['birth_year'] = df['birth_year'].astype(pd.Int64Dtype())

	print('\nCalculating User Stats...\n')
	start_time = time.time()

	#Displaying user_count types
	print("\nThe various user type count are:\n")
	print(df['user_type'].value_counts().to_string())

	# Displaying counts of gender
	print("\nThe various gender count are: \n")
	print(df.groupby('gender').size().to_string())

	# Display earliest, most recent, and most common year of birth
	print('\nEarliest year of birth:')
	early_yob = df.birth_year.min()
	print(early_yob)

	print('\nThe most recent year of birth is: \n')
	max_yob = df.birth_year.max()
	print(max_yob)

	print('\nThe most common year of birth is: \n')
	mod_yob = df.birth_year.mode().iloc[0]
	print(mod_yob)

	print("\nThis took %s seconds." % (time.time() - start_time))
	print('_'*40)

def raw_data(df):
    #Input to print first five rows
    five_rows = input('Are you interested in seeing the first five rows of the data?\n Yes or No? \n').lower()

    initial = 0
    final = 5

    #while loop to specify whether to print first five and subsequent 5

    while five_rows == 'yes':
    	if five_rows == 'yes':
     	   print(df.iloc[initial:final])
     	   initial += 5
     	   final += 5
     	   five_rows = input('Would you like to see the next five rows? Yes or No?  ').lower()

def main():
	while True:
		city, month, day = get_filters()
		df = load_data(city, month, day)

		if city == 'washington':
			clean_headings(df)
			time_stats(df)
			station_stats(df)
			print("\nNo user stats are available for Washington")
			trip_duration_stats(df)
			raw_data(df)

		else:
			clean_headings(df)
			time_stats(df)
			station_stats(df)
			trip_duration_stats(df)
			user_stats(df)
			raw_data(df)
		restart = input('\nWould you like to restart? Enter yes or no.\n')
		if restart.lower() != 'yes':
			break

if __name__ == "__main__":
	main()
