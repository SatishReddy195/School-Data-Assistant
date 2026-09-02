# 🏫 School Data Assistant

An AI-powered assistant that allows a school principal to ask questions about school data using natural language.

Instead of manually searching Excel files, the principal can simply ask questions such as:

* How many students are there?
* What is the total revenue?
* What is the overall pass percentage?
* What is the average attendance?
* How many complaints are pending?
* How many teachers are there?

## 🚀 How It Works

```text
Principal
    ↓
Streamlit
    ↓
Gemini AI Agent
    ↓
Function Calling
    ↓
Python Tools
    ↓
Pandas + Excel
    ↓
Result
    ↓
Gemini
    ↓
Answer
```

Gemini understands the question and selects the appropriate tool. Python and Pandas then retrieve or calculate the actual data.

## 🛠️ Technologies

* Python
* Google Gemini
* Function Calling
* Agentic AI
* Pandas
* Excel
* Streamlit
* Git & GitHub

## 🤖 AI Tools

The application uses **2 custom tools**.

### 1. `query_school_data`

Used for general data queries such as:

* Filtering students
* Counting records
* Calculating averages
* Calculating sums
* Finding minimum/maximum values
* Grouping data

Works with:

```text
Students
Marks
Fees
Attendance
Complaints
Sports
Teachers
```

### 2. `get_school_metric`

Used for school-specific calculations such as:

* Student pass percentage
* Total revenue
* Outstanding fees
* Average attendance
* Students below attendance threshold
* Pending complaints
* Active students
* Sports participation
* Teacher count

## 📊 Data

The project uses Excel files containing:

* Student information
* Marks
* Fees
* Attendance
* Complaints
* Sports
* Teacher information

## 📁 Project Structure

```text
School_Data_Assistant/
│
├── app.py
├── assistant.py
├── query_engine.py
├── derived_metrics.py
├── data_loader.py
├── inspect_data.py
├── requirements.txt
│
└── Student_Data/
    ├── students.xlsx
    ├── marks.xlsx
    ├── fees.xlsx
    ├── attendance.xlsx
    ├── complaints.xlsx
    ├── sports.xlsx
    └── teachers.xlsx
```

## ▶️ Run Locally

Clone the repository and install the dependencies:

```bash
pip install -r requirements.txt
```

Set your Gemini API key:

```text
GEMINI_API_KEY=your_api_key
```

Run the application:

```bash
python -m streamlit run app.py
```

## 🎯 Key Features

* Natural-language questions
* Gemini AI agent
* Function calling
* Safe Python tool execution
* Excel data processing
* Pandas-based calculations
* Streamlit chat interface

## 🔮 Future Improvements

* SQL database integration
* Interactive dashboards
* Authentication
* Automated reports
* Year-over-year analysis

## 👨‍💻 Author

**Satish Kumar**

AI / GenAI Developer

Interested in building AI agents and intelligent applications using Python, Gemini, and modern Generative AI technologies.
