# Development of a College FAQ Chatbot Using Natural Language Processing

**Practical AI Assignment Project**  
**Selected Domain:** Examinations  
**Institution:** Office of the Controller of Examinations  

---

## 1. Project Overview

The **College Examination FAQ Chatbot** is a full-stack, interactive AI web application designed to help college students quickly find official answers to examination-related queries using **Natural Language Processing (NLP)**.

Students can ask questions in free-form English regarding semester dates, hall ticket downloads, examination fees, attendance eligibility, revaluation procedures, supplementary exams, and malpractice regulations. The chatbot uses **Term Frequency-Inverse Document Frequency (TF-IDF)** and **Cosine Similarity** vector matching to identify student intent and return accurate, predefined answers along with contextual suggested questions.

---

## 2. Key Features

- **College-Themed Chat UI:** Clean, responsive interface featuring message bubbles, timestamps, bot avatar, online status badge, and auto-scrolling chat history.
- **Natural Language Understanding (NLU):** Handles different phrasing variations for the same underlying question (e.g., *"When are my semester exams?"*, *"Tell me the exam date"*, *"Semester exam date?"*).
- **30 Comprehensive Examination FAQs:** Pre-loaded knowledge base covering all 28+ required examination topics.
- **Typing Indicator & Loading Feedback:** Realistic typing animation prior to returning answers.
- **Suggested Quick Questions:** Interactive clickable chip buttons below messages and fallback responses.
- **Graceful Fallback Mechanism:** Informative guidance and prompt suggestions when confidence falls below matching threshold.
- **Session Control:** Clear Chat button to reset conversation state.
- **Admin FAQ Management Panel:** Full CRUD interface to View, Search, Filter by Category, Add, Edit, and Delete FAQ entries dynamically.

---

## 3. Technology Stack

- **Backend:** Python (Flask Web Framework)
- **NLP Engine:** Custom TF-IDF Vectorizer & Cosine Similarity Intent Classifier (`nlp_engine.py`)
- **Database / Knowledge Base:** JSON Document Store (`data/faqs.json`)
- **Frontend:** HTML5, CSS3 (Modern Flex/Grid academic theme), JavaScript (ES6 Fetch API)
- **Icons:** Font Awesome 6.4

---

## 4. Project Folder Structure

```
college_exam_chatbot/
├── data/
│   └── faqs.json                 # 30 pre-loaded examination FAQs with patterns & responses
├── static/
│   ├── css/
│   │   └── style.css             # Responsive college theme stylesheet
│   └── js/
│       └── app.js                # Chatbot interaction & Admin CRUD logic
├── templates/
│   └── index.html                # Single-Page Application (Chatbot + Admin Manager)
├── app.py                        # Flask server & REST API endpoints
├── nlp_engine.py                 # Core NLP Pipeline (Preprocessing, TF-IDF, Cosine Sim)
├── test_chatbot.py               # Automated verification test suite
└── README.md                     # Documentation & Execution Guide
```

---

## 5. NLP Pipeline & Mathematical Logic

```
[Student Input Question]
           │
           ▼
[Text Preprocessing & Tokenization] (Lowercase, Punctuation & Stopword Removal)
           │
           ▼
[TF-IDF Feature Vector Computation]
           │
           ▼
[Cosine Similarity Vector Comparison vs Knowledge Base Patterns]
           │
           ▼
[Confidence Threshold Check (Sim >= 0.22)]
 ├── YES ──> [Return Matched Answer + Intent Badge + Related Suggestions]
 └── NO  ──> [Return Fallback Message + Default Quick Question Chips]
```

### Mathematical Formula:
$$\text{Similarity}(\vec{U}, \vec{P}) = \frac{\sum U_i P_i}{\sqrt{\sum U_i^2} \cdot \sqrt{\sum P_i^2}}$$

---

## 6. How to Run the Project

### Prerequisites:
- Python 3.8 or higher installed on your system.
- Flask installed (`py -m pip install flask`).

### Step-by-Step Execution:

1. **Navigate to Project Directory:**
   ```bash
   cd C:\Users\suved\.gemini\antigravity\scratch\college_exam_chatbot
   ```

2. **Run the Flask Web Application:**
   ```bash
   py app.py
   ```

3. **Access the Chatbot in Web Browser:**
   Open your browser and navigate to:
   ```
   http://127.0.0.1:5000
   ```

4. **Run Automated NLP Test Suite:**
   ```bash
   py test_chatbot.py
   ```

---

## 7. Practical Examination Verification Questions

Test the application using the following sample student queries:

| # | Test Question | Expected Intent |
|---|---|---|
| 1 | When are the semester exams? | `exam_date` |
| 2 | When is the exam timetable released? | `exam_timetable` |
| 3 | How can I download my hall ticket? | `hall_ticket_download` |
| 4 | How much is the examination fee? | `exam_fee` |
| 5 | What is the attendance requirement? | `attendance_requirement` |
| 6 | When will the results be published? | `results` |
| 7 | How do I apply for revaluation? | `revaluation` |
| 8 | What happens if I miss an examination? | `missed_exam` |
| 9 | What are the rules for malpractice? | `malpractice` |
| 10 | When are practical examinations conducted? | `practical_exam` |

---

## 8. Conclusion

This project demonstrates how **Natural Language Processing (NLP)** and **Information Retrieval (IR)** techniques can be combined with a modern web frontend to automate student inquiry handling in higher education institutions, significantly reducing administrative workload and improving student satisfaction.
