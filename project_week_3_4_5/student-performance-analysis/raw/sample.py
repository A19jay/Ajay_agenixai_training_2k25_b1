import pandas as pd
import numpy as np
import random

# Set random seed for reproducibility
np.random.seed(42)

# Parameters for dataset generation
num_students = 1000  # Number of students to simulate

# Generate Student IDs
student_ids = [f"S{str(i).zfill(4)}" for i in range(1, num_students + 1)]

# Generate Student Demographics
ages = np.random.randint(15, 22, size=num_students)  # Age between 15 and 21
genders = np.random.choice(['Male', 'Female'], size=num_students, p=[0.5, 0.5])
socioeconomic_statuses = np.random.choice(['Low', 'Middle', 'High'], size=num_students, p=[0.3, 0.5, 0.2])

# Generate Academic Performance Data
grades = np.random.uniform(50, 100, size=num_students)  # Grades between 50 and 100
attendance = np.random.uniform(60, 100, size=num_students)  # Attendance percentage between 60% and 100%

# Generate Learning Activities Data
time_spent_on_homework = np.random.uniform(0.5, 4, size=num_students)  # Time spent on homework in hours
class_participation = np.random.choice(['Low', 'Medium', 'High'], size=num_students, p=[0.2, 0.5, 0.3])

# Generate Academic Performance Status (Pass/Fail)
# Pass if grades >= 60, otherwise Fail
academic_performance_status = ['Pass' if grade >= 60 else 'Fail' for grade in grades]

# Create DataFrame
data = pd.DataFrame({
    'StudentID': student_ids,
    'Age': ages,
    'Gender': genders,
    'SocioeconomicStatus': socioeconomic_statuses,
    'Grades': grades,
    'Attendance': attendance,
    'TimeSpentOnHomework': time_spent_on_homework,
    'ClassParticipation': class_participation,
    'AcademicPerformanceStatus': academic_performance_status
})

# Save to CSV
data.to_csv('student_performance_data.csv', index=False)

print("Synthetic dataset generated and saved as 'student_performance_data.csv'.")
