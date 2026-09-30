import json
import re
import math
import os
from collections import Counter

class ExamChatbotNLPEngine:
    def __init__(self, data_filepath):
        self.data_filepath = data_filepath
        self.faqs = []
        self.idf = {}
        self.corpus_size = 0
        self.default_suggestions = [
            "When are the semester exams?",
            "How can I download my hall ticket?",
            "What is the examination fee?",
            "What is the attendance requirement?",
            "When will results be published?",
            "How can I apply for revaluation?"
        ]
        
        # Domain-specific examination keywords list
        self.domain_keywords = {
            "exam", "exams", "examination", "examinations", "test", "tests", "semester",
            "internal", "internals", "iat", "midterm", "datesheet", "schedule", "timetable",
            "hall", "ticket", "admit", "card", "download", "seat", "seating", "venue", "room",
            "block", "center", "centre", "fee", "fees", "cost", "payment", "paid", "late",
            "penalty", "fine", "attendance", "percent", "percentage", "condonation", "medical",
            "absent", "sickness", "leave", "75", "result", "results", "mark", "marks",
            "grade", "cgpa", "sgpa", "gpa", "score", "sheet", "revaluation", "rechecking",
            "retotaling", "photocopy", "script", "answer", "supplementary", "supply", "arrear",
            "backlog", "fail", "failed", "passed", "pass", "passing", "clearing", "practical",
            "lab", "laboratory", "viva", "project", "voce", "external", "evaluator", "malpractice",
            "cheating", "copying", "phone", "smartphone", "suspension", "disciplinary",
            "punishment", "lost", "misplaced", "duplicate", "missed", "miss", "grievance",
            "complaint", "error", "correction", "office", "coe", "controller", "contact",
            "phone", "email", "scribe", "grace", "credit", "nss", "sports"
        }

        self.greetings = {"hi", "hello", "hey", "greetings", "good morning", "good afternoon", "good evening"}

        self.load_and_index()

    def load_and_index(self):
        """Loads FAQs from JSON file and builds the TF-IDF search index."""
        if not os.path.exists(self.data_filepath):
            self.faqs = []
            return

        with open(self.data_filepath, 'r', encoding='utf-8') as f:
            self.faqs = json.load(f)

        # Build IDF dictionary
        doc_count = 0
        df = Counter()

        for faq in self.faqs:
            all_texts = [faq.get("question", "")] + faq.get("patterns", [])
            for text in all_texts:
                tokens = set(self.preprocess(text))
                for token in tokens:
                    df[token] += 1
                doc_count += 1

        self.corpus_size = doc_count
        self.idf = {}
        for token, freq in df.items():
            self.idf[token] = math.log(1.0 + (self.corpus_size / (1.0 + freq)))

    def preprocess(self, text):
        """Tokenizes text into cleaned lowercase words."""
        if not text:
            return []
        words = re.findall(r'\b[a-z0-9]+\b', text.lower())
        
        stopwords = {
            "a", "an", "the", "is", "are", "am", "was", "were", "be", "been", "being",
            "in", "on", "at", "to", "for", "of", "with", "by", "from", "up", "about",
            "into", "over", "after", "can", "could", "should", "would", "do", "does",
            "did", "doing", "i", "you", "he", "she", "it", "we", "they", "my", "your",
            "me", "tell", "please", "want", "know", "give", "what", "when", "where",
            "how", "which", "who", "why"
        }
        
        filtered = [w for w in words if w not in stopwords]
        return filtered if filtered else words

    def get_tfidf_vector(self, tokens):
        """Calculates normalized TF-IDF vector for token list."""
        tf = Counter(tokens)
        total_count = len(tokens)
        if total_count == 0:
            return {}

        vector = {}
        for token, count in tf.items():
            term_freq = count / total_count
            weight = term_freq * self.idf.get(token, math.log(1.0 + self.corpus_size))
            vector[token] = weight
        return vector

    def cosine_similarity(self, vec1, vec2):
        """Calculates cosine similarity score between two TF-IDF vectors."""
        intersection = set(vec1.keys()) & set(vec2.keys())
        numerator = sum(vec1[token] * vec2[token] for token in intersection)

        sum1 = sum(v**2 for v in vec1.values())
        sum2 = sum(v**2 for v in vec2.values())
        denominator = math.sqrt(sum1) * math.sqrt(sum2)

        if not denominator:
            return 0.0
        return numerator / denominator

    def process_query(self, user_query):
        """
        Main NLP pipeline with Domain Relevance Filtering.
        Strictly answers examination queries and returns fallback for unrelated queries.
        """
        if not user_query or not user_query.strip():
            return {
                "success": False,
                "response": "Please type a valid examination question.",
                "intent": None,
                "confidence": 0.0,
                "suggestions": self.default_suggestions
            }

        cleaned_query = user_query.strip().lower()

        # Check for simple greeting
        if cleaned_query in self.greetings or any(g == cleaned_query for g in self.greetings):
            return {
                "success": True,
                "response": "Hello! I'm your College Examination FAQ Assistant. Ask me anything about examinations, schedules, hall tickets, results, attendance requirements, or examination procedures.",
                "intent": "greeting",
                "category": "General",
                "question": "Hello",
                "confidence": 1.0,
                "suggestions": self.default_suggestions
            }

        query_tokens = self.preprocess(user_query)
        if not query_tokens:
            return self.get_fallback_response()

        # Check domain relevance: Does query contain any examination keyword or overlapping corpus word?
        has_domain_keyword = any(token in self.domain_keywords for token in query_tokens)
        user_vec = self.get_tfidf_vector(query_tokens)

        best_score = 0.0
        best_faq = None
        matched_pattern = None

        # Compare against all FAQs and patterns
        for faq in self.faqs:
            candidate_texts = [faq["question"]] + faq.get("patterns", [])
            for text in candidate_texts:
                pattern_tokens = self.preprocess(text)
                
                # Verify token intersection (must share at least one non-stopword token)
                common_tokens = set(query_tokens) & set(pattern_tokens)
                if not common_tokens:
                    continue

                pattern_vec = self.get_tfidf_vector(pattern_tokens)
                sim = self.cosine_similarity(user_vec, pattern_vec)

                # Bonus ONLY if user query is a substantial exact match (8+ chars)
                if len(cleaned_query) >= 8 and (cleaned_query in text.lower() or text.lower() in cleaned_query):
                    sim += 0.20

                if sim > best_score:
                    best_score = sim
                    best_faq = faq
                    matched_pattern = text

        # Strict Confidence Threshold (0.35) AND Must possess domain relevance
        if best_score >= 0.35 and best_faq and (has_domain_keyword or best_score >= 0.50):
            category = best_faq.get("category", "")
            related_suggestions = [
                f["question"] for f in self.faqs 
                if f.get("category") == category and f["id"] != best_faq["id"]
            ][:3]
            
            if len(related_suggestions) < 3:
                for s in self.default_suggestions:
                    if s not in related_suggestions and s != best_faq["question"]:
                        related_suggestions.append(s)
                    if len(related_suggestions) >= 3:
                        break

            return {
                "success": True,
                "response": best_faq["response"],
                "intent": best_faq["intent"],
                "category": best_faq.get("category", "General"),
                "question": best_faq["question"],
                "confidence": round(float(min(best_score, 1.0)), 2),
                "matched_pattern": matched_pattern,
                "suggestions": related_suggestions
            }
        else:
            # Irrelevant or low-confidence query -> Return Fallback Response
            return self.get_fallback_response()

    def get_fallback_response(self):
        """Returns standard fallback message with suggested questions."""
        return {
            "success": False,
            "response": "I'm sorry, I couldn't find a relevant answer to that question. Please try asking about examination dates, hall tickets, timetable, fees, attendance, results, revaluation, or examination procedures.",
            "intent": "fallback",
            "confidence": 0.0,
            "suggestions": self.default_suggestions
        }

    def save_faqs(self, faqs_data):
        """Saves updated FAQs to disk and re-indexes."""
        with open(self.data_filepath, 'w', encoding='utf-8') as f:
            json.dump(faqs_data, f, indent=2)
        self.load_and_index()
