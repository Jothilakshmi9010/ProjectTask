import pandas as pd
import os
import json

# Define grade point values (customize based on your institution's grading system)
grade_point_values = {
    'O': 10.0,
    'A+': 9.0,
    'A': 8.0,
    'B+': 7.0,
    'B': 6.0,
    'C': 5.0,
    'U': 'RE',
    'SA': 0.0
}

# Function to calculate GPA for a semester
def calculate_semester_gpa(csv_file):
    df = pd.read_csv(csv_file)
    
    # Filter out subjects marked as 'RE'
    df = df[df['grade'] != 'RE']
    
    df['Grade Point'] = df['grade'].map(grade_point_values)
    df['Total Grade Points'] = df['Grade Point'] * df['credits']
    total_credit_hours = df['credits'].sum()
    total_grade_points = df['Total Grade Points'].sum()
    gpa = total_grade_points / total_credit_hours
    return gpa, total_credit_hours, total_grade_points

# Process each semester CSV file
semester_files = ['semester1.csv', 'semester2.csv']  # Add more files as needed
cgpa_total_grade_points = 0
cgpa_total_credit_hours = 0

output_data = {'semesters': []}

for semester_file in semester_files:
    semester_gpa, semester_credit_hours, semester_grade_points = calculate_semester_gpa(semester_file)
    
    semester_data = {
        'semester_file': semester_file,
        'gpa': round(semester_gpa, 2),
        'total_credit_hours': semester_credit_hours,
        'total_grade_points': semester_grade_points
    }
    
    output_data['semesters'].append(semester_data)
    
    # Accumulate grade points and credit hours for CGPA calculation
    cgpa_total_grade_points += semester_grade_points
    cgpa_total_credit_hours += semester_credit_hours

# Calculate CGPA
cgpa = cgpa_total_grade_points / cgpa_total_credit_hours
output_data['overall_cgpa'] = round(cgpa, 2)

# Write output data to a JSON file
with open('gpa_cgpa_results.json', 'w') as json_file:
    json.dump(output_data, json_file, indent=4)

print("Output saved to gpa_cgpa_results.json")
