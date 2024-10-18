import pandas as pd


def calculate_demographic_data(print_data=True):

    # Constants
    PERCENT = 100
    
    # Load the dataset
    data_frame = pd.read_csv("adult.data.csv")
    
    # Count the number of each race represented in the dataset
    # series
    race_count = data_frame['race'].value_counts()
    
    # Calculate the average age of men
    data_frame_men_only = data_frame[data_frame['sex'] == 'Male']
    average_age_men = round(data_frame_men_only['age'].mean(), 1)
    
    # Calculate the percentage of people who have a Bachelor's degree
    num_bachelors = data_frame[data_frame['education'] == 'Bachelors'].shape[0]
    total_people = data_frame.shape[0]
    percentage_bachelors = round((num_bachelors / total_people) * PERCENT, 1)

    # Calculate the percentage of people who have a Bachelor's degree
    #value_counts_normalized = data_frame['education'].value_counts(normalize=True)
    #percentage_bachelors = value_counts_normalized.get('Bachelors', 0) * PERCENT
    #percentage_bachelors = round(percentage_bachelors, 1)
    
    # Define the categories of advanced education
    advanced_education = ['Bachelors', 'Masters', 'Doctorate']
    
    # Separate people with and without advanced education
    higher_education = data_frame[data_frame['education'].isin(advanced_education)] #data_frame
    lower_education = data_frame[~data_frame['education'].isin(advanced_education)] #data_frame
    
    # Calculate the percentage of people with advanced education who make more than 50K
    num_higher_education_high_salary = higher_education[higher_education['salary'] == '>50K'].shape[0]
    total_higher_education = higher_education.shape[0]
    higher_education_rich = round((num_higher_education_high_salary / total_higher_education) * PERCENT, 1)
    
    # Calculate the percentage of people without advanced education who make more than 50K
    num_lower_education_high_salary = lower_education[lower_education['salary'] == '>50K'].shape[0]
    total_lower_education = lower_education.shape[0]
    lower_education_rich = round((num_lower_education_high_salary / total_lower_education) * PERCENT, 1)
    
    # Calculate the minimum number of hours a person works per week
    min_work_hours = data_frame['hours-per-week'].min() 
    
    # Calculate the percentage of rich among those who work the minimum number of hours per week
    min_workers = data_frame[data_frame['hours-per-week'] == min_work_hours] #data_frame
    num_min_workers_rich = min_workers[min_workers['salary'] == '>50K'].shape[0]
    rich_percentage = round((num_min_workers_rich / min_workers.shape[0]) * PERCENT, 1)
    
    # Identify the country with the highest percentage of people earning >50K
    country_salary_group = data_frame.groupby('native-country')['salary']
    series_countries_rich = country_salary_group.apply(lambda x: (x == '>50K').sum())
    series_countries_total = country_salary_group.size()
    series_rich_percentage_by_country = (series_countries_rich / series_countries_total) * PERCENT
    highest_earning_country = series_rich_percentage_by_country.idxmax()
    highest_earning_country_percentage = round(series_rich_percentage_by_country.max(), 1)
    
    # Identify the most popular occupation for those who earn >50K in India
    data_frame_india_occupations = data_frame[(data_frame['native-country'] == 'India') & (data_frame['salary'] == '>50K')]
    # string
    top_IN_occupation = data_frame_india_occupations['occupation'].value_counts().idxmax()

    # DO NOT MODIFY BELOW THIS LINE

    if print_data:
        print("Number of each race:\n", race_count) 
        print("Average age of men:", average_age_men)
        print(f"Percentage with Bachelors degrees: {percentage_bachelors}%")
        print(f"Percentage with higher education that earn >50K: {higher_education_rich}%")
        print(f"Percentage without higher education that earn >50K: {lower_education_rich}%")
        print(f"Min work time: {min_work_hours} hours/week")
        print(f"Percentage of rich among those who work fewest hours: {rich_percentage}%")
        print("Country with highest percentage of rich:", highest_earning_country)
        print(f"Highest percentage of rich people in country: {highest_earning_country_percentage}%")
        print("Top occupations in India:", top_IN_occupation)

    return {
        'race_count': race_count,
        'average_age_men': average_age_men,
        'percentage_bachelors': percentage_bachelors,
        'higher_education_rich': higher_education_rich,
        'lower_education_rich': lower_education_rich,
        'min_work_hours': min_work_hours,
        'rich_percentage': rich_percentage,
        'highest_earning_country': highest_earning_country,
        'highest_earning_country_percentage':
        highest_earning_country_percentage,
        'top_IN_occupation': top_IN_occupation
    }