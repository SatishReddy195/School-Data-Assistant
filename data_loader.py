import pandas as pd
from pathlib import Path


DATA_DIRECTORY = Path(__file__).parent / "Student_Data"


students_df = pd.read_excel(DATA_DIRECTORY / "students.xlsx")
marks_df = pd.read_excel(DATA_DIRECTORY / "marks.xlsx")
fees_df = pd.read_excel(DATA_DIRECTORY / "fees.xlsx")
attendance_df = pd.read_excel(DATA_DIRECTORY / "attendance.xlsx")
complaints_df = pd.read_excel(DATA_DIRECTORY / "complaints.xlsx")
sports_df = pd.read_excel(DATA_DIRECTORY / "sports.xlsx")
teachers_df = pd.read_excel(DATA_DIRECTORY / "teachers.xlsx")


print("All school data loaded successfully.")