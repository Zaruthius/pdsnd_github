import time
import datetime
import pandas as pd
# imported for use with pandas
import numpy as np
import calendar

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print("Hello! Let\'s explore some US bikeshare data!")
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    cities = ['chicago', 'new york city', 'washington']
    # the input is forced to lower case to ensure no errors occur
    city = input("Please enter a city (Chicago, New York City or Washington): ").lower()
    # ensure a valid city is entered.
    while not (city in cities):
        # the input is forced to lower case to ensure no errors occur
        city = input("Not a valid city. Please choose from Chicago, New York City or Washington: ").lower()

    # get user input for month (all, january, february, ... , june)
    months = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
    # the month variable is set to global to be used in an if statement relating to the filtered dataframe
    global month
    # the input is forced to lower case to ensure no errors occur
    month = input("Please enter a month you wish to filter for (January to June or all for no filter): ").lower()
    while not (month in months):
        # the input is forced to lower case to ensure no errors occur
        month = input("You did not enter a valid month. Please only choose from January to June or all: ").lower()

    # get user input for day of week (all, monday, tuesday, ... sunday)
    days = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    # the day variable is set to global to be used in an if statement relating to the filtered dataframe
    global day
    # the input is forced to lower case to ensure no errors occur
    day = input("Please enter a day you wish to filter for (all for no filter): ").lower()
    while not (day in days):
        # the input is forced to lower case to ensure no errors occur
        day = input("You did not enter a valid day. Please re-enter the day: ").lower()

    print('-' * 40)
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

    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    # get the name of the day of the week
    df['day_of_week'] = df['Start Time'].dt.strftime("%A")

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print("\nCalculating The Most Frequent Times of Travel...\n")
    start_time = time.time()

    # display the most common month
    # display the most common month if all is chosen else indicate the filter set by the user
    if month == 'all':
        print("The month in which the most trips were taken was: ", calendar.month_name[df['month'].mode()[0]])
    else:
        print("The data was filtered to", calendar.month_name[df['month'].mode()[0]])
    # display the most common day of week
    # display the most common day if all is chosen else indicate the filter set by the user
    if day == 'all':
        print("The most common day is: ", df['day_of_week'].mode()[0])
    else:
        print("The data was filtered to", df['day_of_week'].mode()[0])
    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    # display the hour in 24h formatting
    print("The most common hour is: ", (str(df['hour'].mode()[0]).zfill(2)) + ":00")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print("\nCalculating The Most Popular Stations and Trip...\n")
    start_time = time.time()

    # display most commonly used start station
    print("Most trips starts at: ", df['Start Station'].mode()[0])
    # display most commonly used end station
    print("Most trips ends at: ", df['End Station'].mode()[0])
    # display most frequent combination of start station and end station trip
    # concatenate the start and end stations to enable the calculation of the most common trip
    df['Trip_Combo'] = df['Start Station'] + " to " + df['End Station']
    print("The most frequent trips were made from", df['Trip_Combo'].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print("\nCalculating Trip Duration...\n")
    start_time = time.time()

    # display total travel time
    # ensure the times displays as days, hh:mm:ss
    print("The total duration of all trips were: ", str(datetime.timedelta(seconds=int(df['Trip Duration'].sum()))))
    # display mean travel time
    print("The average trip duration was: ", str(datetime.timedelta(seconds=int(df['Trip Duration'].mean()))))
    print("Trips typically lasted for: ", str(datetime.timedelta(seconds=int(df['Trip Duration'].mode()[0]))))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print("\nCalculating User Stats...\n")
    start_time = time.time()

    # display counts of user types
    # do not display the field name and datatype in the output
    print("The following client types made trips:\n", df['User Type'].value_counts().to_string())
    # display counts of gender
    # error checking to ensure the data works with the washington data set.
    try:
        print("\nThe number of men and woman who made trips were as follows:\n", df['Gender'].value_counts().to_string())
    except:
        print("No Gender field was found in the data")
    # display earliest, most recent, and most common year of birth
    # error checking to ensure the data works with the washington data set.
    try:
        print("\nThe oldest person who made a trip was born in: ", int(df['Birth Year'].min()))
        print("The youngest person who made a trip was born in: ", int(df['Birth Year'].max()))
        print("The most common year of birth for people who made a trips was: ", int(df['Birth Year'].mode()[0]))
    except:
        print("No birth year field was found in the data")
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        # df = load_data("new york city", "all", "monday") -- Used during testing

        time_stats(df)
        # create a user managed delay between calculations
        input("Press Enter to continue to station statistics\n")
        station_stats(df)
        input("Press Enter to continue trip duration statistics\n")
        trip_duration_stats(df)
        input("Press Enter to continue user statistics\n")
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()

""" Additional resources used:
Udacity Python classroom content
Stack Overflow community
Python.org website
"""
