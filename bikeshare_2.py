import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

MONTH_NUMBER = {"january": 1, "february": 2, "march": 3, "april": 4, "may": 5, "june": 6}

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    while True:
        # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
        city = input("Enter city (chicago, new york city, washington): ").strip().lower()
        
        if city in ["chicago", "new york city", "washington"]:

            # get user input for month (all, january, february, ... , june)
            month = input("Enter month (all, january, february, ... , june): ").strip().lower()
            if month in ["all", "january", "february", "march", "april", "may", "june"]:
                
                # get user input for day of week (all, monday, tuesday, ... sunday)
                day = input("Enter day of the week (all, monday, tuesday, ... sunday): ").strip().lower()
                if day in ["all", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]:
                    print('-'*40)
                    return city, month, day 
                else:
                    print("Invalid input. Please enter day of the week (all, monday, tuesday, ... sunday)")
            else:
                print("Invalid input. Please enter month (all, january, february, ... , june)")
        else:
            print("Invalid input. Please enter chicago, new york city, or washington.")


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
    # Get the file based on the selected city
    try:
        df = pd.read_csv(CITY_DATA[city])
    except Exception as e:
        raise FileNotFoundError(f"Could not load data for {city}: {e}")


    # filter based on month
    if month != "all":

        df['Start Time'] = pd.to_datetime(df['Start Time'])
        df['start_month'] = df['Start Time'].dt.month
        
        df['End Time'] = pd.to_datetime(df['End Time'])
        df['end_month'] = df['End Time'].dt.month
                
        df = df[(df['start_month'] <= MONTH_NUMBER[month]) & (df['end_month'] >= MONTH_NUMBER[month])]

    # convert start time into datetime and create day of week
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['day_of_week'] = df['Start Time'].dt.day_name()
    
    # filter based on day
    if day != "all":
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()


    # display the most common month
    most_common_month = pd.to_datetime(df['Start Time']).dt.month.mode()
    print("Most Common Month:", most_common_month)

    # display the most common day of week
    if 'day_of_week' in df.columns:
        most_common_day = df['day_of_week'].mode()[0]
        print("Most Common Day:", most_common_day)

    # display the most common start hour
    most_common_hour = pd.to_datetime(df['Start Time']).dt.hour.mode()
    print("Most Common Start Hour:", most_common_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    most_common_start_station = df['Start Station'].mode()
    print("Most commonly used start station:", most_common_start_station)

    # display most commonly used end station
    most_common_end_station = df['End Station'].mode()
    print("Most commonly used end station:", most_common_end_station)


    # display most frequent combination of start station and end station trip
    df['combined_station'] = df['Start Station'] + df['End Station']
    frequent_combination = df['combined_station'].mode()
    print("Most frequent combination of start station and end station trip:", frequent_combination)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print("Total Travel Time:", total_travel_time)

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print("Mean Travel Time:", mean_travel_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print(user_types)

    # Display counts of gender
    if 'Gender' in df.columns:

        gender_counts = df['Gender'].value_counts()
        print(gender_counts)
    else:
        print("Gender data not available for this city.")

    # Display earliest, most recent, and most common year of birth
    # check if year of birth column exists
    if 'Birth Year' in df.columns:

        earliest_year = int(df['Birth Year'].min())
        print("Earliest Year of Birth:", earliest_year)

        most_recent_year = int(df['Birth Year'].max())
        print("Most Recent Year of Birth:", most_recent_year)

        most_common_year = int(df['Birth Year'].mode()[0])
        print("Most Common Year of Birth:", most_common_year)

    else:
        print("Birth Year data not available for this city.")


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def display_raw_data(df):
    start = 0
    step = 5
    n = len(df)

    while True:
        while True:
            answer = input("\nWould you like to see 5 lines of raw data? Enter yes or no: ").strip().lower()
            if answer in ("yes", "no"):
                break
            print("Invalid input. Please enter 'yes' or 'no'.")

        if answer == "no":
            break

        # If no more rows, stop
        if start >= n:
            print("\nNo more raw data to display.")
            break

        end = min(start + step, n)
        print(df.iloc[start:end])

        # Move to next chunk
        start += step

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        display_raw_data(df)

        while True:
            restart = input('\nWould you like to restart? Enter yes or no: ').strip().lower()

            if restart in ("yes", "no"):
                break
            else:
                print("Invalid input. Please enter 'yes' or 'no'.")

        if restart == "no":
            break


if __name__ == "__main__":
	main()
