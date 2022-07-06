import time
import pandas as pd
import numpy as np
import datetime, calendar#, datetime_object

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
    print('Hello! Let\'s some formating changes i supposedexplore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington).
    #HINT: Use a while loop to handle invalid inputs
    while True:
        city = input('Choose a city (chicago, new york city, or washington?\n').lower()
        if city in CITY_DATA.keys():
            break
        else:
            print('\n Not a valid city \n')
            continue


    # TO DO: get user input for month (all, january, february, ... , june)
    while True:
        month = input('which month: january, february, march, april, may, june or all?\n').lower()
        months = ['january','february','march','april','may','june']
        if month == 'all':
            break
        elif month in months:
            break
        else:
            print('\n invalid month. \n')
            continue


    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input('which day: monday, tuesday, wednesday, thursday, friday, saturday, sunday or all?\n').lower()
        days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        if day == 'all':
            break
        elif day in days:
            break
        else:
            print('\n invalid day. \n')
            continue

    #print('city ' + city + ' month ' + month + ' day ' + day +' got it? \n')
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
    df['day_of_week'] = df['Start Time'].dt.weekday

    #print(df)   #300k rows
    if month != 'all':
        #Use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        #Filter by month to create the new dataframe maybe some commenting changes
        df = df[df['month'] == month]
    #print(df)   #51k rows april

    if day != 'all':
        #Filter by day of week to create the new dataframe
        daysl = ['monday','tuesday','wednesday','thursday','friday','saturday','sunday']
        dday = daysl.index(day)+1
        #print('dday is ' + str(dday) + ' yes it is \n')
        df = df[df['day_of_week'] == dday]

    #print(df)   #51k rows april
    #print(df)   #6k rows april and wednesday
    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    common_month = df['month'].mode()[0]

    datetime_object = datetime.datetime.strptime(str(common_month), "%m")
    month_name = datetime_object.strftime("%B")

    print(f"The most common month is: {month_name}")

    # TO DO: display the most common day of week
    common_day = df['day_of_week'].mode()[0]
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    #days[common_day]
    print(f"\n the most common day is: {days[common_day]}")

    # TO DO: display the most common start hour
    common_hour = df['Start Time'].dt.hour.mode()[0]

    print(f"\n the most common hour is: {common_hour}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    common_start_station = df['Start Station'].mode()[0]

    print(f"The most common something else to modify to make it look nice start station: {common_start_station}")

    # TO DO: display most commonly used end station
    common_end_station = df['End Station'].mode()[0]

    print(f"\nThe most common end station: {common_end_station}")

    # TO DO: display most frequent combination of start station and end station trip
    df['Start To End'] = df['Start Station'].str.cat(df['End Station'], sep=' to ')
    combo = df['Start To End'].mode()[0]

    print(f"\nThe most frequent combination of trips are from {combo}.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_duration = df['Trip Duration'].sum()
    minute, second = divmod(total_duration, 60)

    hour, minute = divmod(minute, 60)
    print(f"The total trip duration is {hour} hours, {minute} minutes and {second} seconds.")

    # TO DO: display mean travel time
    average_duration = round(df['Trip Duration'].mean())
    mins, sec = divmod(average_duration, 60)
    if mins > 60:
        hrs, mins = divmod(mins, 60)
        print(f"\nThe average trip duration is {hrs} hours, {mins} minutes and {sec} seconds.")
    else:
        print(f"\nThe average trip duration is {mins} minutes and {sec} seconds.")



    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_type = df['User Type'].value_counts().to_frame()

    print(f"The types of users by number are given below:\n\n{user_type}")


    # TO DO: Display counts of gender
    try:
        gender = df['Gender'].value_counts().to_frame()

        print(f"\nThe types of users by gender are given below:\n\n{gender}")
    except:
        print("\nThere is no 'Gender' column in this file.")

    # TO DO: Display earliest, most recent, and most common year of birth
    try:
        earliest = int(df['Birth Year'].min())
        recent = int(df['Birth Year'].max())
        common_year = int(df['Birth Year'].mode()[0])
        print(f"\nThe earliest year of birth: {earliest}\n")
        print(f"\nThe most recent year of birth: {recent}\n")
        print(f"\nThe most common year of birth: {common_year}")
    except:
        print("There are no birth year details in this file.")


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_data(df):
    rownum = 0
    #print(df[rownum:rownum+5])
    #rownum += 5
    moredata = input('Would you like to see raw data? yes or no\n').lower()
    while True:
        if moredata == 'yes':
            print(df[rownum:rownum+5])
            rownum += 5
            moredata = input('Would you like to see more raw data? yes or no\n').lower()
        elif moredata == 'no':
            break
        else:
            print('\n Not a valid response \n')
            moredata = input('Would you like to see more raw data? yes or no\n').lower()
            continue

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        #df = load_data("chicago", "april", "wednesday")
        #show_data(df)
        display_data(df)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            print('\n Thank you for using the bike share query system. Have a nice day! \n')
            break

if __name__ == "__main__":
	main()
