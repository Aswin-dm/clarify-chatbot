Clarify - Smart College Inquiry Chatbot
Clarify is an intelligent chatbot designed to streamline college-related inquiries. It provides students and parents with instant, accurate information regarding tuition fees, admission eligibility, scholarship opportunities, and more. By utilizing Natural Language Processing (NLP), Clarify understands user intent and retrieves the most relevant data from its integrated database.

🚀 Key Features
Instant Answers: Get immediate responses to common questions about college courses and administration.

NLP Integration: Uses advanced processing to understand human-like queries rather than just keywords.

Fee & Scholarship Tracking: Detailed information on financial aid and program costs.

User-Friendly Interface: A clean, web-based chat interface for a seamless experience.

Chat History: Built-in history to keep track of previous inquiries.

🛠 Tech Stack
Backend: Python (Flask/Django or similar framework)

Frontend: HTML, CSS, JavaScript

NLP: Python-based NLP libraries (e.g., NLTK, Spacy, or Transformers)

Storage: Database for storing course and scholarship metadata

📂 Project Structure
```
clarify-chatbot/
├── chat.py             # Core logic for handling chat responses and NLP
├── index.html          # Main frontend user interface
├── .gitattributes      # Git configuration file
└── README.md           # Project documentation
```
⚙️ Installation & Setup
Clone the repository:

Bash
```
git clone https://github.com/Aswin-dm/clarify-chatbot.git
cd clarify-chatbot
```
Set up a Virtual Environment (Recommended):

Bash
```
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```
Install Dependencies:
(Ensure you have a requirements.txt; if not, you may need to install libraries like Flask and NLTK manually)

Bash
```
pip install -r requirements.txt
```
Run the Application:

Bash
```
python chat.py
```
Open http://127.0.0.1:5000 (or the specified port) in your web browser.

💡 How to Use
Once the application is running, type your question in the chat box (e.g., "What is the eligibility for Computer Science?" or "Are there any scholarships for international students?").

The chatbot will process your input and display the answer directly in the chat window.
