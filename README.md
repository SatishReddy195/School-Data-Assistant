🏫 School Data Assistant

An AI-powered school data assistant that allows a school principal to ask natural-language questions about students, marks, fees, attendance, complaints, sports, and teachers.

The application uses Google Gemini function calling to understand the principal's question, select the appropriate Python tool, retrieve or calculate the required information from structured school data, and generate a clear final response.

🚀 Project Overview

School administrators often need information from multiple datasets such as:

Student records
Examination marks
Fee payments
Attendance
Complaints
Sports participation
Teacher information

Instead of manually searching Excel files or depending on others to prepare reports, this application provides a conversational interface.

A principal can simply ask:

"How many female students are in class 8?"

or:

"What is the total revenue for 2026-27?"

or:

"What is the overall student pass percentage?"

The AI agent determines what information is required, calls the appropriate tool, performs the calculation using Python and Pandas, and returns the verified result.

🎯 Project Goal

The primary goal of this project is to demonstrate how an Agentic AI system can safely work with structured business data.

The design intentionally separates:

AI reasoning from data execution.

Gemini decides:

What needs to be done?

Python decides:

How should the data operation actually be executed?

This prevents the LLM from directly executing arbitrary Python code against the data.

🏗️ Architecture
                    PRINCIPAL
                        │
                        │ Natural-language question
                        ▼
                ┌─────────────────┐
                │   Streamlit UI  │
                │     app.py      │
                └────────┬────────┘
                         │
                         ▼
                ┌─────────────────┐
                │   assistant.py  │
                │                 │
                │   Gemini Agent  │
                └────────┬────────┘
                         │
                  Gemini chooses
                    a tool
                         │
              ┌──────────┴──────────┐
              │                     │
              ▼                     ▼
    ┌─────────────────────┐ ┌─────────────────────┐
    │ query_school_data() │ │ get_school_metric() │
    │                     │ │                     │
    │ Generic Data Tool   │ │ Business Metric     │
    │                     │ │ Tool                │
    └──────────┬──────────┘ └──────────┬──────────┘
               │                       │
               ▼                       ▼
        Pandas DataFrames       derived_metrics.py
               │                       │
               └──────────┬────────────┘
                          ▼
                    Excel Data
                          │
                          ▼
                    Tool Result
                          │
                          ▼
                        Gemini
                          │
                          ▼
                    Final Answer
                          │
                          ▼
                      Principal

Gemini function calling is used as the bridge between natural-language requests and application-side functions. The model selects a declared function and provides structured arguments; the application executes the function and returns the result to the model for the final response.

🤖 Agentic AI Workflow

The application follows this workflow:

1. Principal asks a question
              ↓
2. Gemini understands the question
              ↓
3. Gemini decides whether a tool is required
              ↓
4. Gemini selects the appropriate tool
              ↓
5. Python executes the tool
              ↓
6. Pandas processes the school data
              ↓
7. Tool result is returned to Gemini
              ↓
8. Gemini generates the final response
              ↓
9. Streamlit displays the answer
Example

Principal asks:

"What is the total revenue for 2026-27?"

Gemini determines that this is a predefined school business metric and selects:

get_school_metric

with:

metric = total_revenue
academic_year = 2026-27

Python then filters the fee data and calculates:

sum(amount_paid)

The result is returned to Gemini, which generates the final response for the principal.

🛠️ AI Tools

The application currently exposes 2 custom Gemini function-calling tools.

1. query_school_data

A generic structured-data query tool.

It works across the following datasets:

students
marks
fees
attendance
complaints
sports
teachers
Supported operations
records
count
sum
average
min
max
Supported filters
==
!=
>
<
>=
<=
Supported grouping

The tool can group results by a selected column.

Example questions
How many students are there?

How many female students are there?

Show students in class 8.

What is the average Mathematics mark?

How many complaints are there?

How many teachers are there by department?

What is the total amount paid in fees?
2. get_school_metric

A specialized tool for predefined school business calculations.

Supported metrics
student_pass_percentage
total_revenue
total_outstanding_fees
average_attendance
students_below_attendance
pending_complaints
active_student_count
sports_participation
teacher_count
Example questions
What is the overall student pass percentage?

What is the total revenue?

How much fee is outstanding?

What is the average attendance?

How many students have attendance below 75%?

How many complaints are pending?

How many active students are there?

How many students participate in sports?

How many teachers are there?
🔐 Safe Tool-Based Architecture

A key design principle of this project is:

Gemini does not directly execute Python code.

Instead, Gemini can only request predefined tools.

For example, Gemini may generate a structured request such as:

Tool:
query_school_data

Dataset:
students

Operation:
count

Condition:
gender == Female

The Python application validates these arguments and executes the predefined function.

This provides a controlled boundary between:

LLM reasoning
      ↓
Structured tool call
      ↓
Python execution

The model therefore does not receive unrestricted access to Python, the operating system, or arbitrary code execution.

📊 School Datasets

The project currently works with seven structured datasets.

Dataset	Purpose
students.xlsx	Student information
marks.xlsx	Examination marks
fees.xlsx	Fee payments and outstanding fees
attendance.xlsx	Student attendance
complaints.xlsx	Student complaints
sports.xlsx	Sports participation
teachers.xlsx	Teacher information
📁 Project Structure
School_Data_Assistant/
│
├── app.py
├── assistant.py
├── query_engine.py
├── derived_metrics.py
├── data_loader.py
├── inspect_data.py
│
├── requirements.txt
├── .gitignore
│
└── Student_Data/
    │
    ├── students.xlsx
    ├── marks.xlsx
    ├── fees.xlsx
    ├── attendance.xlsx
    ├── complaints.xlsx
    ├── sports.xlsx
    └── teachers.xlsx
📌 File Responsibilities
app.py

Responsible for the Streamlit user interface.

Main responsibilities:

Display the application
Accept natural-language questions
Maintain chat history
Send questions to the AI agent
Display the final answer
assistant.py

Responsible for the AI agent and Gemini integration.

Main responsibilities:

Connect to Gemini
Define the system instructions
Declare the available tools
Receive the principal's question
Process Gemini function calls
Execute the requested Python tools
Return tool results to Gemini
Generate the final response

This is the main agent orchestration layer.

query_engine.py

Contains the implementation of the structured-data tools.

Main responsibilities:

Select the appropriate dataset
Validate datasets
Validate operations
Apply filtering conditions
Perform aggregations
Perform grouping
Return structured results

The two exposed tools are:

query_school_data()
get_school_metric()
derived_metrics.py

Contains deterministic school-specific business calculations.

Examples:

student_pass_percentage()
total_revenue()
total_outstanding_fees()
average_attendance()
students_below_attendance()
pending_complaints_count()
active_student_count()
sports_participation_count()
teacher_count()

These calculations are implemented in Python rather than asking the LLM to perform the calculations.

data_loader.py

Responsible for loading Excel files into Pandas DataFrames.

Example:

students_df = pd.read_excel(
    DATA_DIRECTORY / "students.xlsx"
)

The loaded DataFrames are then used by the query engine and business-metric functions.

inspect_data.py

A development and data-quality utility.

It can be used to inspect:

Number of rows
Number of columns
Column names
Sample records
Missing values

It is not part of the main runtime request flow.

💡 Example Questions

The principal can ask questions such as:

Students
How many students are there?

How many female students are there?

How many students are in class 8?

Show students in class 10.
Marks
What is the average Mathematics mark?

Show the marks of student STU2026001.

What is the highest mark in Mathematics?

How many students scored above 80?
Fees
What is the total revenue?

How much fee is outstanding?

What is the total amount paid in 2026-27?
Attendance
What is the average attendance?

How many students have attendance below 75%?

What is the attendance for class 8?
Complaints
How many complaints are pending?

How many complaints were received?

Show complaints for a particular academic year.
Sports
How many students participate in sports?

How many students participated in sports in 2026-27?
Teachers
How many teachers are there?

How many active teachers are there?
🔄 Example End-to-End Request
User question
What is the total outstanding fee for 2026-27?
Gemini decision
Tool:
get_school_metric

Metric:
total_outstanding_fees

Academic Year:
2026-27
Python execution
fees.xlsx
    ↓
Pandas DataFrame
    ↓
Filter academic_year = 2026-27
    ↓
Sum amount_pending
Result
Verified calculated value
Gemini

Gemini receives the result and converts it into a natural-language response.

Streamlit

The final answer is displayed to the principal.

🧠 Why Use Gemini + Python Instead of Asking Gemini to Calculate Everything?

LLMs are useful for:

Understanding natural language
Determining user intent
Selecting tools
Extracting parameters
Generating natural-language responses

Python and Pandas are better suited for:

Filtering datasets
Aggregations
Numerical calculations
Grouping
Data validation
Deterministic business logic

Therefore, this project follows:

Gemini
"Understand what the user wants."

        ↓

Python Tools
"Execute the requested operation."

        ↓

Pandas
"Process the structured data."

        ↓

Gemini
"Explain the verified result."

This separation makes the system easier to control, test, and extend.

🧰 Technology Stack
Technology	Purpose
Python	Application and business logic
Google Gemini	AI reasoning and function calling
Google GenAI SDK	Gemini API integration
Pandas	Data processing
Excel	Structured data source
Streamlit	Web application UI
Git	Version control
GitHub	Source-code hosting and collaboration
🔑 Environment Setup

Create a Python virtual environment:

python -m venv .venv

Activate it on Windows:

.\.venv\Scripts\Activate.ps1

Install dependencies:

pip install -r requirements.txt
🔐 API Key Configuration

The application requires a Gemini API key.

Set the following environment variable:

GEMINI_API_KEY

For local development, the key can be stored in an environment configuration that is excluded from Git.

Important

Do not commit API keys or other secrets to GitHub.

The repository should use:

.env
.streamlit/secrets.toml

in .gitignore.

▶️ Run the Application

From the project root:

python -m streamlit run app.py

The Streamlit application will open in the browser.
