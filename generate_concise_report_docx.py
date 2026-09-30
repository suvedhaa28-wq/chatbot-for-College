import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import qn, nsdecls
import os

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def add_snippet_block(doc, title, code_snippet, language_label="Python"):
    h = doc.add_heading(title, level=3)
    h.runs[0].font.color.rgb = RGBColor(37, 99, 235)
    h.paragraph_format.space_before = Pt(8)
    h.paragraph_format.space_after = Pt(4)

    table = doc.add_table(rows=1, cols=1)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    
    cell = table.rows[0].cells[0]
    cell.width = Inches(6.5)
    set_cell_background(cell, "F8FAFC")
    set_cell_margins(cell, 120, 120, 150, 150)

    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.line_spacing = 1.1

    lines = code_snippet.strip().split('\n')
    for idx, line in enumerate(lines):
        run = p.add_run(line + ("\n" if idx < len(lines)-1 else ""))
        run.font.name = "Consolas"
        run.font.size = Pt(8.5)
        run.font.color.rgb = RGBColor(15, 23, 42)

    doc.add_paragraph().paragraph_format.space_after = Pt(6)

def generate_concise_report():
    base_dir = r"C:\Users\suved\.gemini\antigravity\scratch\college_exam_chatbot"
    doc = docx.Document()

    # Page Margins (1 inch everywhere)
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)

    NAVY = RGBColor(15, 23, 42)
    BLUE = RGBColor(37, 99, 235)
    GRAY = RGBColor(100, 116, 139)
    DARK = RGBColor(30, 41, 59)

    # =========================================================================
    # PAGE 1: TITLE / COVER PAGE
    # =========================================================================
    p_spacer = doc.add_paragraph()
    p_spacer.paragraph_format.space_before = Pt(36)

    title_p = doc.add_paragraph()
    title_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    title_run = title_p.add_run("DEVELOPMENT OF A COLLEGE FAQ CHATBOT USING NATURAL LANGUAGE PROCESSING")
    title_run.font.name = "Arial"
    title_run.font.size = Pt(24)
    title_run.font.bold = True
    title_run.font.color.rgb = NAVY
    title_p.paragraph_format.space_after = Pt(16)

    sub_p = doc.add_paragraph()
    sub_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    sub_run = sub_p.add_run("A Practical Artificial Intelligence & NLP Assignment Report\nDomain: College Examinations")
    sub_run.font.name = "Arial"
    sub_run.font.size = Pt(14)
    sub_run.font.italic = True
    sub_run.font.color.rgb = BLUE
    sub_p.paragraph_format.space_after = Pt(80)

    meta_table = doc.add_table(rows=4, cols=2)
    meta_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    
    meta_data = [
        ("Course:", "Artificial Intelligence & NLP Lab"),
        ("Project Domain:", "College Examination Office (http://127.0.0.1:5000/)"),
        ("Submission Date:", "30th September 2026"),
        ("Author / Student:", "[Insert Student Name / Roll Number Here]")
    ]

    for idx, (label, val) in enumerate(meta_data):
        row_cells = meta_table.rows[idx].cells
        row_cells[0].width = Inches(2.2)
        row_cells[1].width = Inches(4.3)
        
        p0 = row_cells[0].paragraphs[0]
        r0 = p0.add_run(label)
        r0.font.bold = True
        r0.font.size = Pt(11)
        r0.font.color.rgb = NAVY

        p1 = row_cells[1].paragraphs[0]
        r1 = p1.add_run(val)
        r1.font.size = Pt(11)
        r1.font.color.rgb = DARK

    doc.add_page_break()

    # =========================================================================
    # PAGE 2: 1. PROJECT OVERVIEW & 2. OBJECTIVES
    # =========================================================================
    h1 = doc.add_heading("1. Project Overview & Description", level=1)
    h1.runs[0].font.color.rgb = NAVY

    p1 = doc.add_paragraph(
        "Higher education institutions manage thousands of student inquiries each academic semester regarding "
        "examinations, schedules, hall ticket availability, fee structures, attendance rules, medical leave condonation, "
        "supplementary examinations, revaluation procedures, and malpractice rules. Traditional manual help desks lead to "
        "long queues, delayed responses, and administrative overhead."
    )
    p1.paragraph_format.space_after = Pt(10)
    p1.paragraph_format.line_spacing = 1.2

    p2 = doc.add_paragraph(
        "The College Examination FAQ Chatbot is an automated conversational agent built using Natural Language Processing (NLP) "
        "techniques. It enables students to ask questions in natural English and receive instant, authoritative answers from an "
        "official FAQ knowledge base. The system integrates TF-IDF vector representation, Cosine Similarity matching, and strict "
        "Domain Relevance Filtering to ensure high accuracy while rejecting unrelated queries with a standardized fallback message."
    )
    p2.paragraph_format.space_after = Pt(20)
    p2.paragraph_format.line_spacing = 1.2

    h2 = doc.add_heading("2. Project Objectives", level=1)
    h2.runs[0].font.color.rgb = NAVY

    objs = [
        ("Automated 24/7 Inquiry Support: ", "Deliver immediate answers to examination inquiries without human intervention."),
        ("Natural Language Understanding (NLU): ", "Recognize student intent across diverse phrasing variations for the same question."),
        ("Strict Domain Relevance Filtering: ", "Filter out irrelevant non-academic queries and return an informative fallback guidance response."),
        ("Comprehensive Examination FAQ Coverage: ", "Maintain a 30-entry pre-loaded knowledge base spanning 6 key academic categories."),
        ("Modern Responsive Student UI: ", "Provide an intuitive chat window with message bubbles, typing indicators, suggested questions, and clear chat option."),
        ("Admin FAQ Management Panel: ", "Equip administrators with a full CRUD panel to view, search, add, edit, and delete FAQ entries dynamically.")
    ]

    for title, desc in objs:
        p = doc.add_paragraph(style='List Bullet')
        r1 = p.add_run(title)
        r1.bold = True
        r1.font.color.rgb = BLUE
        r2 = p.add_run(desc)
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.line_spacing = 1.15

    doc.add_page_break()

    # =========================================================================
    # PAGE 3: 3. SYSTEM ARCHITECTURE & DESIGN
    # =========================================================================
    h3 = doc.add_heading("3. System Architecture & High-Level Design", level=1)
    h3.runs[0].font.color.rgb = NAVY

    p_arch = doc.add_paragraph(
        "The chatbot application is structured as a decoupled multi-tier architecture combining a Python Flask REST backend, "
        "a custom NLP classification engine, a JSON document store, and a responsive HTML5/CSS3/JavaScript frontend."
    )
    p_arch.paragraph_format.space_after = Pt(12)
    p_arch.paragraph_format.line_spacing = 1.2

    h3_sub = doc.add_heading("3.1 Core System Components", level=2)
    h3_sub.runs[0].font.color.rgb = BLUE

    components = [
        ("Web Application Layer (app.py): ", "Flask web server serving HTML interfaces and handling JSON REST API endpoints (/api/chat, /api/faqs, /api/stats)."),
        ("NLP Classification Engine (nlp_engine.py): ", "Core text preprocessor, TF-IDF vectorizer, cosine similarity matcher, and domain relevance validator."),
        ("Knowledge Base Storage (data/faqs.json): ", "Structured JSON storage containing 30 examination FAQs with intent keys, categories, and pattern variations."),
        ("Frontend Interface (index.html, style.css, app.js): ", "Interactive single-page application providing dual views for Student Chat and Admin Management.")
    ]

    for title, desc in components:
        p = doc.add_paragraph(style='List Bullet')
        r1 = p.add_run(title)
        r1.bold = True
        r2 = p.add_run(desc)
        p.paragraph_format.space_after = Pt(6)

    doc.add_heading("3.2 FAQ Knowledge Base Categories", level=2)
    
    cat_table = doc.add_table(rows=1, cols=3)
    cat_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    
    cat_hdr = cat_table.rows[0].cells
    cat_hdr[0].text = "Category Name"
    cat_hdr[1].text = "Scope / Topics Covered"
    cat_hdr[2].text = "FAQ Count"
    
    for c_idx in range(3):
        set_cell_background(cat_hdr[c_idx], "0F172A")
        set_cell_margins(cat_hdr[c_idx], 100, 100, 120, 120)
        p = cat_hdr[c_idx].paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        for r in p.runs:
            r.font.bold = True
            r.font.color.rgb = RGBColor(255, 255, 255)
            r.font.size = Pt(9.5)

    cat_data = [
        ("Schedule & Timetable", "Semester exam dates, internal assessment tests, duration, timetable, seating venue", "7 FAQs"),
        ("Hall Ticket & Eligibility", "Admit card download, availability, 75% attendance rule, medical leave condonation", "6 FAQs"),
        ("Registration & Fees", "Exam registration process, deadlines, fee structure per paper, late fines", "4 FAQs"),
        ("Results & Revaluation", "Result declaration, SGPA/CGPA, paper revaluation, mark sheets, supplementary exams", "6 FAQs"),
        ("Regulations & Rules", "Passing criteria, internal marks split-up, malpractice penalties, scribe rules", "5 FAQs"),
        ("Support & Office", "Controller of Examinations office location, working hours, contact info, grievances", "2 FAQs")
    ]

    for r_idx, row in enumerate(cat_data):
        cells = cat_table.add_row().cells
        bg = "F8FAFC" if r_idx % 2 == 0 else "FFFFFF"
        for c_idx, val in enumerate(row):
            cells[c_idx].text = val
            set_cell_background(cells[c_idx], bg)
            set_cell_margins(cells[c_idx], 80, 80, 100, 100)
            p = cells[c_idx].paragraphs[0]
            if c_idx == 2:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            for r in p.runs:
                r.font.size = Pt(9)

    doc.add_page_break()

    # =========================================================================
    # PAGE 4: 4. NLP METHODOLOGY & MATHEMATICAL FORMULATION
    # =========================================================================
    h4 = doc.add_heading("4. NLP Methodology & Mathematical Formulation", level=1)
    h4.runs[0].font.color.rgb = NAVY

    p_nlp_intro = doc.add_paragraph(
        "The chatbot uses an Information Retrieval (IR) based Vector Space Model (VSM) to convert user questions "
        "and FAQ intent patterns into numerical weight vectors for similarity calculation."
    )
    p_nlp_intro.paragraph_format.space_after = Pt(10)

    doc.add_heading("4.1 Text Preprocessing", level=2)
    p_pre = doc.add_paragraph(
        "Incoming text is normalized using standard lowercasing, regex-based punctuation removal, and stopword filtering. "
        "This focuses term weights on core domain keywords such as 'exam', 'timetable', 'hall ticket', 'fee', and 'revaluation'."
    )
    p_pre.paragraph_format.space_after = Pt(10)

    doc.add_heading("4.2 Term Frequency - Inverse Document Frequency (TF-IDF)", level=2)
    p_tfidf = doc.add_paragraph(
        "Each term t in document d is assigned a weight based on its local frequency (TF) and global inverse document frequency (IDF):"
    )
    p_tfidf.paragraph_format.space_after = Pt(4)

    p_eq1 = doc.add_paragraph()
    p_eq1.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_eq1 = p_eq1.add_run("TF(t, d) = (Count of term t in d) / (Total words in d)\nIDF(t) = log(1 + N / (1 + Document Frequency of t))\nTF-IDF(t, d) = TF(t, d) × IDF(t)")
    r_eq1.font.name = "Consolas"
    r_eq1.font.size = Pt(9.5)
    r_eq1.font.bold = True
    r_eq1.font.color.rgb = BLUE
    p_eq1.paragraph_format.space_after = Pt(12)

    doc.add_heading("4.3 Cosine Similarity Matching", level=2)
    p_cos = doc.add_paragraph(
        "The match score between user query vector U and pattern vector P is calculated as the cosine of the angle between them:"
    )
    p_cos.paragraph_format.space_after = Pt(4)

    p_eq2 = doc.add_paragraph()
    p_eq2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_eq2 = p_eq2.add_run("Similarity(U, P) = (U · P) / (||U|| × ||P||) = Σ (U_i × P_i) / ( √Σ U_i² × √Σ P_i² )")
    r_eq2.font.name = "Consolas"
    r_eq2.font.size = Pt(9.5)
    r_eq2.font.bold = True
    r_eq2.font.color.rgb = BLUE
    p_eq2.paragraph_format.space_after = Pt(12)

    doc.add_heading("4.4 Domain Relevance Filter Logic", level=2)
    p_dom = doc.add_paragraph(
        "To prevent matching on irrelevant queries (e.g. 'What is the capital of France?'), the engine verifies that the query contains "
        "at least one domain keyword or shares non-stopword tokens with candidate FAQ patterns, while enforcing a similarity threshold of 0.35. "
        "Queries failing this check are routed to the Fallback Handler."
    )
    p_dom.paragraph_format.space_after = Pt(12)

    doc.add_page_break()

    # =========================================================================
    # PAGE 5: 5. CORE SOURCE CODE SNIPPETS (PART 1 - BACKEND & NLP)
    # =========================================================================
    h5 = doc.add_heading("5. Core Source Code Snippets (http://127.0.0.1:5000/)", level=1)
    h5.runs[0].font.color.rgb = NAVY

    p_code_note = doc.add_paragraph(
        "Below are concise, representative code excerpts highlighting the primary backend routes and NLP matching engine:"
    )
    p_code_note.paragraph_format.space_after = Pt(8)

    # Snippet 1: Flask app.py
    flask_snippet = """# app.py - Flask Server REST API Endpoints

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.get_json() or {}
    user_message = data.get('message', '').strip()
    
    # Process query through NLP Engine pipeline
    result = nlp_engine.process_query(user_message)
    result['timestamp'] = datetime.now().strftime('%I:%M %p')
    return jsonify(result)

@app.route('/api/faqs', methods=['POST'])
def add_faq():
    data = request.get_json() or {}
    new_faq = {
        'id': max([f.get('id', 0) for f in nlp_engine.faqs], default=0) + 1,
        'intent': data.get('intent', '').strip().lower(),
        'category': data.get('category', 'General').strip(),
        'question': data.get('question', '').strip(),
        'patterns': data.get('patterns', []),
        'response': data.get('response', '').strip()
    }
    nlp_engine.faqs.append(new_faq)
    nlp_engine.save_faqs(nlp_engine.faqs)
    return jsonify({'success': True, 'faq': new_faq}), 201"""
    
    add_snippet_block(doc, "5.1 Flask Server API Endpoints (app.py)", flask_snippet)

    # Snippet 2: nlp_engine.py
    nlp_snippet = """# nlp_engine.py - Cosine Similarity & Domain Relevance Matching

def cosine_similarity(self, vec1, vec2):
    intersection = set(vec1.keys()) & set(vec2.keys())
    numerator = sum(vec1[token] * vec2[token] for token in intersection)
    sum1 = sum(v**2 for v in vec1.values())
    sum2 = sum(v**2 for v in vec2.values())
    denominator = math.sqrt(sum1) * math.sqrt(sum2)
    return (numerator / denominator) if denominator else 0.0

def process_query(self, user_query):
    query_tokens = self.preprocess(user_query)
    has_domain_kw = any(t in self.domain_keywords for t in query_tokens)
    user_vec = self.get_tfidf_vector(query_tokens)

    best_score, best_faq = 0.0, None
    for faq in self.faqs:
        for text in [faq["question"]] + faq.get("patterns", []):
            pattern_vec = self.get_tfidf_vector(self.preprocess(text))
            sim = self.cosine_similarity(user_vec, pattern_vec)
            if sim > best_score:
                best_score, best_faq = sim, faq

    # Enforce Domain Keyword Relevance & Threshold (0.35)
    if best_score >= 0.35 and best_faq and (has_domain_kw or best_score >= 0.50):
        return {"success": True, "response": best_faq["response"], "intent": best_faq["intent"], "confidence": round(best_score, 2)}
    return self.get_fallback_response()"""

    add_snippet_block(doc, "5.2 NLP Cosine Similarity Engine (nlp_engine.py)", nlp_snippet)

    doc.add_page_break()

    # =========================================================================
    # PAGE 6: 5. CORE SOURCE CODE SNIPPETS (PART 2 - FRONTEND HTML & JS)
    # =========================================================================
    h5_2 = doc.add_heading("5. Core Source Code Snippets (Continued)", level=1)
    h5_2.runs[0].font.color.rgb = NAVY

    # Snippet 3: index.html
    html_snippet = """<!-- templates/index.html - Chat Interface & Navigation Layout -->
<header class="app-header">
    <div class="brand-container">
        <div class="college-logo"><i class="fa-solid fa-graduation-cap"></i></div>
        <div class="brand-text">
            <h1>College Examination FAQ Assistant</h1>
            <p>Office of the Controller of Examinations</p>
        </div>
    </div>
    <div class="nav-tabs">
        <button class="nav-btn active" id="tab-student-btn" onclick="switchTab('student')">Student Chatbot</button>
        <button class="nav-btn" id="tab-admin-btn" onclick="switchTab('admin')">Admin FAQ Manager</button>
    </div>
</header>

<div class="chat-messages" id="chat-messages"><!-- Dynamic message bubbles --></div>
<div class="chat-input-bar">
    <input type="text" id="user-input" placeholder="Ask anything about exams, hall tickets, timetable..." />
    <button id="send-btn" onclick="sendMessage()"><i class="fa-solid fa-paper-plane"></i> Send</button>
</div>"""

    add_snippet_block(doc, "5.3 Web Chat Interface Template (index.html)", html_snippet)

    # Snippet 4: app.js
    js_snippet = """// static/js/app.js - Frontend Asynchronous Chat Handler

async function sendMessage(textOverride = null) {
    const inputElement = document.getElementById('user-input');
    const query = textOverride ? textOverride : inputElement.value.trim();
    if (!query) return;

    appendUserMessage(query);
    showTypingIndicator(true);

    const response = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: query })
    });
    const data = await response.json();

    setTimeout(() => {
        showTypingIndicator(false);
        appendBotMessage(data.response, data.intent, data.confidence, data.suggestions);
    }, 400);
}"""

    add_snippet_block(doc, "5.4 Asynchronous Frontend Logic (app.js)", js_snippet)

    doc.add_page_break()

    # =========================================================================
    # PAGE 7: 6. FAQ KNOWLEDGE BASE DATASET SAMPLE
    # =========================================================================
    h6 = doc.add_heading("6. FAQ Knowledge Base Dataset Sample (data/faqs.json)", level=1)
    h6.runs[0].font.color.rgb = NAVY

    p_json_note = doc.add_paragraph(
        "Below is a representative sample of intent entries from the 30-FAQ dataset stored in data/faqs.json:"
    )
    p_json_note.paragraph_format.space_after = Pt(8)

    json_snippet = """[
  {
    "id": 1,
    "intent": "exam_date",
    "category": "Schedule & Timetable",
    "question": "When are the semester examinations conducted?",
    "patterns": [
      "when are my semester exams", "when is the semester examination",
      "tell me the exam date", "semester exam date"
    ],
    "response": "The Odd Semester examinations are scheduled from November 15 to December 10, and Even Semester examinations run from April 20 to May 15."
  },
  {
    "id": 4,
    "intent": "hall_ticket_download",
    "category": "Hall Ticket & Eligibility",
    "question": "How can I download my examination hall ticket?",
    "patterns": [
      "how can i download my hall ticket", "how to get hall ticket online",
      "where to print hall ticket", "download exam admit card portal"
    ],
    "response": "Log in to the Student Portal (portal.college.edu), navigate to 'Examinations' > 'Hall Ticket', verify your subject codes, and click 'Download & Print PDF'."
  },
  {
    "id": 12,
    "intent": "attendance_requirement",
    "category": "Hall Ticket & Eligibility",
    "question": "What is the minimum attendance requirement to appear for examinations?",
    "patterns": [
      "what is the attendance requirement", "minimum attendance percentage to write exams",
      "is 75 percent attendance mandatory for exams"
    ],
    "response": "A minimum of 75% aggregate attendance in each registered course is strictly required to be eligible for end-semester examinations."
  }
]"""

    add_snippet_block(doc, "6.1 Sample Knowledge Base Entries (data/faqs.json)", json_snippet)

    doc.add_page_break()

    # =========================================================================
    # PAGE 8: 7. SAMPLE OUTPUT & CONVERSATION DIALOGUES
    # =========================================================================
    h7 = doc.add_heading("7. Sample Output & Conversation Dialogues", level=1)
    h7.runs[0].font.color.rgb = NAVY

    p_out_intro = doc.add_paragraph(
        "Below are realistic sample interactions demonstrating valid examination query matching, greeting responses, "
        "and irrelevant question rejection with the fallback handler:"
    )
    p_out_intro.paragraph_format.space_after = Pt(12)

    samples = [
        ("Student: ", "When are the semester exams?"),
        ("Chatbot: ", "The Odd Semester examinations are scheduled from November 15 to December 10, and the Even Semester examinations run from April 20 to May 15. Please consult the official academic calendar on the university portal for exact department-wise dates.\n[Intent: exam_date | Confidence: 100%]"),
        ("Student: ", "How can I download my hall ticket?"),
        ("Chatbot: ", "Log in to the Student Portal (portal.college.edu) using your Roll Number and Password, navigate to 'Examinations' > 'Hall Ticket', verify your subject codes, and click 'Download & Print PDF'.\n[Intent: hall_ticket_download | Confidence: 100%]"),
        ("Student: ", "What is the attendance requirement?"),
        ("Chatbot: ", "A minimum of 75% aggregate attendance in each registered course is strictly required to be eligible for end-semester examinations. Students with 65%-74% attendance due to illness may apply for condonation.\n[Intent: attendance_requirement | Confidence: 100%]"),
        ("Student: ", "What is the capital of France?"),
        ("Chatbot (Fallback): ", "I'm sorry, I couldn't find a relevant answer to that question. Please try asking about examination dates, hall tickets, timetable, fees, attendance, results, revaluation, or examination procedures.\n[Intent: fallback | Confidence: 0%]")
    ]

    for sender, msg in samples:
        p = doc.add_paragraph()
        p.paragraph_format.left_indent = Inches(0.25)
        r1 = p.add_run(sender)
        r1.bold = True
        r1.font.color.rgb = BLUE if "Student" in sender else NAVY
        r2 = p.add_run(msg)
        r2.font.size = Pt(9.5)
        p.paragraph_format.space_after = Pt(6)

    doc.add_page_break()

    # =========================================================================
    # PAGE 9: 8. SYSTEM VERIFICATION & ACCURACY TEST RESULTS
    # =========================================================================
    h8 = doc.add_heading("8. System Verification & Accuracy Test Results", level=1)
    h8.runs[0].font.color.rgb = NAVY

    p_test_intro = doc.add_paragraph(
        "The automated verification suite (test_chatbot.py) evaluated 22 query test cases covering core examination questions, "
        "phrasing variations, greetings, and irrelevant queries. The system achieved 100.0% accuracy:"
    )
    p_test_intro.paragraph_format.space_after = Pt(10)

    table = doc.add_table(rows=1, cols=4)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False

    hdr_cells = table.rows[0].cells
    headers = ["#", "Input Student Query", "Detected Intent", "Status"]
    col_widths = [Inches(0.5), Inches(3.1), Inches(1.8), Inches(1.1)]

    for idx, text in enumerate(headers):
        hdr_cells[idx].text = text
        set_cell_background(hdr_cells[idx], "0F172A")
        set_cell_margins(hdr_cells[idx], 100, 100, 120, 120)
        p = hdr_cells[idx].paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        for r in p.runs:
            r.font.bold = True
            r.font.color.rgb = RGBColor(255, 255, 255)
            r.font.size = Pt(9)

    test_rows_data = [
        ("1", "When are the semester exams?", "exam_date", "PASSED"),
        ("2", "Semester exam date?", "exam_date", "PASSED"),
        ("3", "Tell me the exam date.", "exam_date", "PASSED"),
        ("4", "When is the exam timetable released?", "exam_timetable", "PASSED"),
        ("5", "How can I download my hall ticket?", "hall_ticket_download", "PASSED"),
        ("6", "Where to print hall ticket", "hall_ticket_download", "PASSED"),
        ("7", "How much is the examination fee?", "exam_fee", "PASSED"),
        ("8", "What is the attendance requirement?", "attendance_requirement", "PASSED"),
        ("9", "is 75 percent attendance mandatory for exams", "attendance_requirement", "PASSED"),
        ("10", "When will the results be published?", "results", "PASSED"),
        ("11", "How do I apply for revaluation?", "revaluation", "PASSED"),
        ("12", "What happens if I miss an examination?", "missed_exam", "PASSED"),
        ("13", "What are the rules for malpractice?", "malpractice", "PASSED"),
        ("14", "When are practical examinations conducted?", "practical_exam", "PASSED"),
        ("15", "Hi", "greeting", "PASSED"),
        ("16", "What is the capital of France?", "fallback (Irrelevant)", "PASSED"),
        ("17", "How to make a delicious pizza at home?", "fallback (Irrelevant)", "PASSED"),
        ("18", "Tell me a funny joke", "fallback (Irrelevant)", "PASSED"),
        ("19", "Who won the cricket world cup match?", "fallback (Irrelevant)", "PASSED"),
        ("20", "What is the weather today?", "fallback (Irrelevant)", "PASSED"),
        ("21", "Where can I buy cheap shoes?", "fallback (Irrelevant)", "PASSED"),
        ("22", "How to code in Python programming?", "fallback (Irrelevant)", "PASSED")
    ]

    for row_idx, data in enumerate(test_rows_data):
        row_cells = table.add_row().cells
        bg_hex = "F8FAFC" if row_idx % 2 == 0 else "FFFFFF"
        
        for c_idx, val in enumerate(data):
            row_cells[c_idx].text = val
            set_cell_background(row_cells[c_idx], bg_hex)
            set_cell_margins(row_cells[c_idx], 60, 60, 80, 80)
            p = row_cells[c_idx].paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if c_idx in [0, 3] else WD_ALIGN_PARAGRAPH.LEFT
            for r in p.runs:
                r.font.size = Pt(8.5)
                if c_idx == 3:
                    r.font.bold = True
                    r.font.color.rgb = RGBColor(21, 128, 61)

    for row in table.rows:
        for idx, width in enumerate(col_widths):
            row.cells[idx].width = width

    doc.add_page_break()

    # =========================================================================
    # PAGE 10: 9. GITHUB LINK PLACEHOLDER & 10. CONCLUSION
    # =========================================================================
    h9 = doc.add_heading("9. Project Repository & Source Code Link", level=1)
    h9.runs[0].font.color.rgb = NAVY

    p_git_intro = doc.add_paragraph(
        "The complete source code, dataset files, web application scripts, automated test suite, and documentation "
        "for this project are hosted on GitHub:"
    )
    p_git_intro.paragraph_format.space_after = Pt(8)

    p_box = doc.add_paragraph()
    p_box.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_box.paragraph_format.space_before = Pt(12)
    p_box.paragraph_format.space_after = Pt(24)
    
    r_box_title = p_box.add_run("GitHub Repository Link Placeholder:\n")
    r_box_title.bold = True
    r_box_title.font.size = Pt(11)
    r_box_title.font.color.rgb = GRAY
    
    r_box_url = p_box.add_run("[ https://github.com/your-username/college-faq-chatbot ]")
    r_box_url.bold = True
    r_box_url.font.size = Pt(13)
    r_box_url.font.color.rgb = BLUE

    h10 = doc.add_heading("10. Conclusion", level=1)
    h10.runs[0].font.color.rgb = NAVY

    p_conc = doc.add_paragraph(
        "The developed College Examination FAQ Chatbot demonstrates an effective practical application of Natural Language Processing "
        "in educational administration. By combining TF-IDF vector matching with strict domain relevance filtering, the chatbot reliably "
        "answers student examination inquiries while gracefully handling unrelated questions, providing an interactive, scalable solution "
        "for university student support."
    )
    p_conc.paragraph_format.space_after = Pt(14)
    p_conc.paragraph_format.line_spacing = 1.25

    target_path = os.path.join(base_dir, "College_FAQ_Chatbot_Lab_Report.docx")
    doc.save(target_path)
    print(f"Concise 10-Page Lab Report Word Document generated successfully at: {target_path}")

if __name__ == "__main__":
    generate_concise_report()
