# school_data.py
# Destin Saba
#
# A terminal-based application for computing and printing statistics based on given input.

import numpy as np
from given_data import year_2013, year_2014, year_2015, year_2016, year_2017, year_2018, year_2019, year_2020, year_2021, year_2022
import csv

# Declare global variables
# Load the enrollment data into a 3D NumPy array
years = np.array([year_2013, year_2014, year_2015, year_2016, year_2017, year_2018, year_2019, year_2020, year_2021, year_2022])
years3D = years.reshape(10,20,3)

# Create a dictionary to map school names to their codes and indices
school_dict = {}
with open('Assignment3Data.csv','r') as file:
    csv_reader = csv.DictReader(file)
    count = 0
    for row in csv_reader:
        school_name = row['School Name']
        school_code = row['School Code']
        if school_name not in school_dict:
            school_dict[school_name] = [school_code,count]
            count += 1

# You may add your own additional classes, functions, variables, etc.

def getInput():
    """
    Prompt the user to enter a school name or school code and return the corresponding school code and name.

    Returns:
    tuple: (school_code, school_name)
    """
    while True:
        try:
            user_input = input("Please enter the high school name or school code: ")
            # Check if the input matches a school code
            if any(user_input == details[0] for details in school_dict.values()):
                name = [k for k, v in school_dict.items() if v[0] == user_input]
                return user_input, name[0]
            # Check if the input matches a school name
            elif user_input in school_dict:
                return school_dict[user_input][0], user_input
            else:
                raise ValueError
        except ValueError:
            print("You must enter a valid school name or code.")
    
def getEnrollment(grade, name): 
    """
    Given a grade and a school name, return the enrollment numbers for that grade across all years.
    
    Parameters:
    grade (int): The grade (10, 11, or 12)
    name (str): The name of the school
    
    Returns:
    np.ndarray: An array of enrollment numbers for the specified grade and school
    """

     # Get the index of the school from the school_dict
    school_index = school_dict[name][1]

    # Map the grade to the corresponding column index in the data
    grade_col_index = grade - 10

    # Extract the enrollment data for the specified grade and school
    enrollment_data = years3D[:, school_index, grade_col_index]

    return enrollment_data

def getSchoolStatistics(name):
    """
    Calculate and return statistics for the specified school, including:
    - Highest enrollment for a single grade within the entire time period
    - Lowest enrollment for a single grade within the entire time period
    - Total enrollment for each year from 2013 to 2022
    
    Parameters:
    name (str): The name of the school
    
    Returns:
    dict: A dictionary containing the statistics
    """

    # Get the index of the school from the school_dict
    school_index = school_dict[name][1]

    # Extract the enrollment data for the specified school
    school_data = years3D[:, school_index, :]

    # Calculate the highest, lowest, and total enrollment for the specified school
    highest_enrollment = np.nanmax(school_data)
    lowest_enrollment = np.nanmin(school_data)
    total_enrollment_per_year = np.nansum(school_data, axis=1)

    # Prepare the statistics dictionary
    statistics = {
        'highest_enrollment': highest_enrollment,
        'lowest_enrollment': lowest_enrollment,
        'total_enrollment_per_year': total_enrollment_per_year
    }

    return statistics
def checkEnrollmentOver500(name):
    """
    Check if there are any enrollments over 500 for the specified school. If yes, print the median of these enrollments.
    If no, print "No enrollments over 500."
    
    Parameters:
    name (str): The name of the school
    """
    
    # Get the index of the school from the school_dict
    school_index = school_dict[name][1]
    
    # Extract the enrollment data for the specified school
    school_data = years3D[:, school_index, :]
    
    # Find enrollments over 500
    over_500_enrollments = school_data[school_data > 500]
    
    if len(over_500_enrollments) == 0:
        print("No enrollments over 500.")
    else:
        median_over_500 = int(np.nanmedian(over_500_enrollments))
        print(f"For all enrollments over 500, the median value was: {median_over_500}")

def generalStatistics():
    """
    Calculate and print general statistics:
    - Mean enrollment in 2013
    - Mean enrollment in 2022
    - Total graduating class of 2022 across all schools
    - Highest enrollment for a single grade within the entire time period across all schools
    - Lowest enrollment for a single grade within the entire time period across all schools
    """
    # Calculate mean enrollment in 2013 and 2022
    mean_enrollment_2013 = np.nanmean(years3D[0, :, :])
    mean_enrollment_2022 = np.nanmean(years3D[9, :, :])
    
    # Calculate total graduating class of 2022 across all schools (Grade 12 in 2022)
    total_graduating_class_2022 = np.nansum(years3D[9, :, 2])
    
    # Calculate highest and lowest enrollment for a single grade within the entire time period across all schools
    highest_enrollment_all = np.nanmax(years3D)
    lowest_enrollment_all = np.nanmin(years3D)

     # Print the general statistics
    print(f"Mean enrollment in 2013: {int(mean_enrollment_2013)}")
    print(f"Mean enrollment in 2022: {int(mean_enrollment_2022)}")
    print(f"Total graduating class of 2022: {int(total_graduating_class_2022)}")
    print(f"Highest enrollment for a single grade: {int(highest_enrollment_all)}")
    print(f"Lowest enrollment for a single grade: {int(lowest_enrollment_all)}")


def main():
    print("ENSF 692 School Enrollment Statistics")

    # Print Stage 1 requirements here
    print(f"Shape of full data array: {years3D.shape}")
    print(f"Dimensions of full data array: {years3D.ndim}")

    # Prompt for user input
    code,name = getInput()


    # Print Stage 2 requirements here
    print("\n***Requested School Statistics***\n")
    print(f"School Name: {name}, School Code: {code}")
    
    # Compute and print mean enrollment for each grade
    for grade in range(10,13):
        enrollment_data = getEnrollment(grade, name)
        # Calculate integer mean using integer division
        mean_enrollment = np.nansum(enrollment_data) // np.count_nonzero(~np.isnan(enrollment_data))
        # Print the integer mean without decimals
        print(f"Mean enrollment for Grade {grade}: {int(mean_enrollment)}")
    
    # Get statistics for the specified school
    stats = getSchoolStatistics(name)

    # Print highest and lowest enrollment  
    print(f"Highest enrollment for a single grade: {int(stats['highest_enrollment'])}")
    print(f"Lowest enrollment for a single grade: {int(stats['lowest_enrollment'])}")
    total = 0
    # Print total enrollment for each year
    for year, enrolled in zip(range(2013, 2022+1), stats['total_enrollment_per_year']):
        print(f"Total enrollment for {year}: {int(enrolled)}")
        total += enrolled
    print(f"Total ten year enrollment: {int(total)}")   
    print(f"Mean total enrollment over 10 years: {int(total)//len(years)}")  
    # Check enrollments over 500 and print the median if applicable
    checkEnrollmentOver500(name)


    # Print Stage 3 requirements here
    print("\n***General Statistics for All Schools***\n")
    generalStatistics()

if __name__ == '__main__':
    main()

