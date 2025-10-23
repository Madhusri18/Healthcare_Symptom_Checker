# Healthcare_Symptom_Checker
Healthcare Symptom Checker is an AI-powered web application that helps users understand their symptoms and provides structured, educational summaries.
It analyzes the user’s input using the Google Gemini API, then returns likely conditions, recommended next steps, and a medical disclaimer.
All queries are stored in a local SQLite database for history and analysis.

---
## Demo Video

https://github.com/user-attachments/assets/c27a374d-ff24-4644-a510-d155384a51dc

---
## Key Features
- **Symptom Analysis:** Input multiple symptoms along with duration and severity.  
- **AI-Powered Insights:** Get a list of possible conditions with reasoning and highlighted warning signs.  
- **Next-Step Suggestions:** Receive actionable guidance and professional consultation reminders.   
- **User-Friendly Design:** Simple, responsive, and intuitive interface suitable for all users.  
- **Medical Safety:** Clear disclaimers encourage users to seek professional help for serious conditions.

---

## Tech Stack
- Frontend: HTML, CSS, JavaScript
- Backend: Python (FastAPI)
- Database: SQLite (via SQLAlchemy)
- AI Model: Google Gemini 2.5 Flash API

---
## Database:
All user queries and AI analyses are stored in:
backend/symptoms.db

## How It Works

- Enter your symptoms and get instant AI-driven analysis
- Structured results with:

1)Possible Conditions
2)Next Steps
3)Disclaimer

- Interactive, responsive, and healthcare-themed interface
- Stores all symptom queries and results in a SQLite database
- Built with FastAPI backend and Gemini API integration

---

git clone https://github.com/Madhusri18/Healthcare_Symptom_Checker

- Author : Madhusri Nallapati
- Mail id : madhusri1304@gmail.com
- Git link : https://github.com/Madhusri18
