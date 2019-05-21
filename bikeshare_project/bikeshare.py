import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

cities = ['chicago', 'new york city', 'washington']
allowed_months = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
days = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday',
            'sunday']

def get_filters():
    city = None
    month = None
    day = None
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    while True:
        print('Which city would you like to explore? (chicago, new york city, washington)')
        city = str(input()).lower()
        if city in cities:
            break

    while True:
        print('Which month(s) would you like to explore? (all, january, february, ... june)')
        month = str(input()).lower()
        if month in allowed_months:
            break

    while True:
        print('Which day(s) would you like to expore? (all, monday, tuesday, ... sunday)')
        day = str(input()).lower()
        if day in days:
            break

    print('-'*40)
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

    df['dow'] = df['Start Time'].dt.weekday_name

    if month != 'all':
        month_num = allowed_months.index(month)
        #print('here ' + str(month_num))
        #print(allowed_months[month_num])
        df = df[df['month'] == month_num]

    if day != 'all':
        df = df[df['dow'] == day.title()]

    print(df.head())
    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    month_count = pd.value_counts(df['month'])
    common_month = allowed_months[month_count.idxmax()].title()
    print('Most common month is {}'.format(common_month))

    day_count = pd.value_counts(df['dow'])
    common_dow = day_count.idxmax()
    print('Most common day of the week is {}'.format(common_dow))

    hour_count = pd.value_counts(df['Start Time'].dt.hour)
    common_hour = hour_count.idxmax()
    print('Most comman hour in {}:00'.format(common_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    start_count = pd.value_counts(df['Start Station'])
    common_start = start_count.idxmax()
    print('Most common start station is {}'.format(common_start))

    end_count = pd.value_counts(df['End Station'])
    common_end = end_count.idxmax()
    print('Most common end station is {}'.format(common_end))

    common_both = df.groupby(['Start Station','End Station']).size().idxmax()
    print('Most common start/end stations are {}'.format(common_both))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    total_travel_time = df['Trip Duration'].sum()
    print('Total time traveled is {} seconds, or {} minutes'.format(total_travel_time, total_travel_time / 60))

    mean_travel_time = df['Trip Duration'].mean()
    print('Mean time traveled is {} seconds, or {} minutes'.format(mean_travel_time, mean_travel_time / 60))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    user_type_count = pd.value_counts(df['User Type'])
    print('User types\n{}'.format(user_type_count))

    gender_count = pd.value_counts(df['Gender'])
    print('Male(s): {} \nFemale(s): {}'.format(gender_count['Male'], gender_count['Female']))

    min_birth = df['Birth Year'].min()
    max_birth = df['Birth Year'].max()
    common_birth = pd.value_counts(df['Birth Year']).idxmax()
    print('Earliest birth year is {}\nMost recent birth year is {}\nMost common birth year is {}'.format(min_birth, max_birth, common_birth))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
	main()
