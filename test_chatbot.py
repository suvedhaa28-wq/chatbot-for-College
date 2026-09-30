"""
Automated Test Suite for College Examination FAQ Chatbot NLP Engine
Verifies valid examination questions AND irrelevant question rejection.
"""

import os
import sys
from nlp_engine import ExamChatbotNLPEngine

def run_tests():
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')

    data_path = os.path.join(os.path.dirname(__file__), 'data', 'faqs.json')
    engine = ExamChatbotNLPEngine(data_path)
    
    test_cases = [
        # --- VALID EXAMINATION QUESTIONS ---
        ("When are the semester exams?", "exam_date"),
        ("Semester exam date?", "exam_date"),
        ("Tell me the exam date.", "exam_date"),
        ("When is the exam timetable released?", "exam_timetable"),
        ("How can I download my hall ticket?", "hall_ticket_download"),
        ("Where to print hall ticket", "hall_ticket_download"),
        ("How much is the examination fee?", "exam_fee"),
        ("What is the attendance requirement?", "attendance_requirement"),
        ("is 75 percent attendance mandatory for exams", "attendance_requirement"),
        ("When will the results be published?", "results"),
        ("How do I apply for revaluation?", "revaluation"),
        ("What happens if I miss an examination?", "missed_exam"),
        ("What are the rules for malpractice?", "malpractice"),
        ("When are practical examinations conducted?", "practical_exam"),
        ("Hi", "greeting"),

        # --- IRRELEVANT QUESTIONS (MUST ALL TRIGGER FALLBACK) ---
        ("What is the capital of France?", "fallback"),
        ("How to make a delicious pizza at home?", "fallback"),
        ("Tell me a funny joke", "fallback"),
        ("Who won the cricket world cup match yesterday?", "fallback"),
        ("What is the weather today?", "fallback"),
        ("Where can I buy cheap shoes?", "fallback"),
        ("How to code in Python programming?", "fallback")
    ]

    print("===============================================================")
    print("   RUNNING DOMAIN RELEVANCE & NLP INTENT VERIFICATION TESTS   ")
    print("===============================================================\n")

    passed = 0
    total = len(test_cases)

    for idx, (query, expected_intent) in enumerate(test_cases, 1):
        result = engine.process_query(query)
        detected_intent = result.get('intent')
        confidence = result.get('confidence', 0.0)

        is_match = (detected_intent == expected_intent)
        if is_match:
            passed += 1
            status_str = "PASSED"
        else:
            status_str = "FAILED"

        clean_resp = result['response'].encode('ascii', 'replace').decode()[:85]
        print(f"[{status_str}] Test #{idx:02d}: '{query}'")
        print(f"         Expected: {expected_intent:<20} | Detected: {detected_intent:<20} | Score: {confidence}")
        print(f"         Response: {clean_resp}...\n")

    print(f"Test Summary: {passed}/{total} tests passed ({round(passed/total*100, 1)}% Accuracy)")
    return passed == total

if __name__ == "__main__":
    run_tests()
