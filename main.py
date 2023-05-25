import time
import pandas as pd
import numpy as np

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
    print('Hello! Let\'s explore some US bikeshare data!')

    city = None
    while city not in ["chicago", "new york city", "washington"]:
        city = input(
            "Would you like to see data for Chicago, New York City, or Washington? choose valid option\n").lower()

    choice = None
    month = None
    day = None
    while choice not in ["month", "day", "both", "none"]:
        choice = input(
            "Would you like to filter the data by month, day, both or not at all? type 'none' for no time filter\n")

        if choice == "month":
            while month not in ["january", "february", "march", "april", "may", "june", "all"]:
                month = input(
                    "Which month? January, February, March, April, May, or June? type 'all' for all months.\n").lower()
                day = "all"

        elif choice == "day":
            while day not in ['1', '2', '3', '4', '5', '6', '7', 'all']:
                day = input(
                    "Which day? please enter your response as an integer. (e.g 1=Sunday) type 'all' for all days.\n")
                month = "all"

            days_of_week = ["", "sunday", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday"]
            if day != "all":
                day = days_of_week[int(day)]

        elif choice == "both":
            while month not in ["january", "february", "march", "april", "may", "june", "all"]:
                month = input(
                    "Which month? January, February, March, April, May, or June? type 'all' for all months\n").lower()
            while day not in ['1', '2', '3', '4', '5', '6', '7', 'all']:
                day = input(
                    "Which day? please enter your response as an integer. (e.g 1=Sunday) type 'all' for all days.\n")

            days_of_week = ["", "sunday", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday"]
            if day != "all":
                day = days_of_week[int(day)]

        elif choice == "none":
            month, day = "all", "all"

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
    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        df = df[df['month'] == month]

    if day != 'all':
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    print("The most common month: ", df['month'].mode()[0])

    # display the most common day of week
    print("The most common day of week: ", df['day_of_week'].mode()[0])

    # display the most common start hour
    print("The most common start hour: ", df['Start Time'].dt.hour.mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print("The most commonly used start station: ", df['Start Station'].mode()[0])

    # display most commonly used end station
    print("The most commonly used end station: ", df['End Station'].mode()[0])

    # display most frequent combination of start station and end station trip
    print("The most frequent combination of start station and end station trip: ",
          df.groupby(['Start Station', 'End Station']).size().idxmax())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print("The total trip duration: ", df['Trip Duration'].sum())

    # display mean travel time
    print("The average of travel duration: ", df['Trip Duration'].mean())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print("The types of users:\n", df['User Type'].value_counts())

    if city != "washington":
        # Display counts of gender
        print("The types of genders: ", df['Gender'].value_counts())

        # Display earliest, most recent, and most common year of birth
        print("The earliest year of birth: {}, The most recent year of birth: {}, The most common year of birth: {}. ".format(df['Birth Year'].min(), df['Birth Year'].max(), df['Birth Year'].mode()[0]))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


city, month, day = get_filters()
df = load_data(city, month, day)
time_stats(df)
station_stats(df)
trip_duration_stats(df)
user_stats(df)

# ['Unnamed: 0', 'Start Time', 'End Time', 'Trip Duration', 'Start Station',
# 'End Station', 'User Type', 'Gender', 'Birth Year', 'month', 'day_of_week']
