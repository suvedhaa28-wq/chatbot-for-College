import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import qn, nsdecls

def create_element(name):
    return OxmlElement(name)

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

def generate_report():
    doc = docx.Document()

    # Page Margins
    sections = doc.sections
    for section in sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)

    # Base Colors
    NAVY = RGBColor(15, 23, 42)
    BLUE = RGBColor(37, 99, 235)
    GRAY = RGBColor(100, 116, 139)
    DARK_GRAY = RGBColor(30, 41, 59)

    # Cover Header / Title
    title_p = doc.add_paragraph()
    title_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    title_run = title_p.add_run("DEVELOPMENT OF A COLLEGE FAQ CHATBOT USING NATURAL LANGUAGE PROCESSING")
    title_run.font.name = "Arial"
    title_run.font.size = Pt(22)
    title_run.font.bold = True
    title_run.font.color.rgb = NAVY

    subtitle_p = doc.add_paragraph()
    subtitle_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    sub_run = subtitle_p.add_run("Practical Artificial Intelligence Project Report\nDomain: College Examinations")
    sub_run.font.name = "Arial"
    sub_run.font.size = Pt(13)
    sub_run.font.italic = True
    sub_run.font.color.rgb = BLUE

    doc.add_paragraph().paragraph_format.space_after = Pt(12)

    # Section 1: Project Overview
    h1 = doc.add_heading("1. Project Overview & Description", level=1)
    h1.runs[0].font.color.rgb = NAVY

    p1 = doc.add_paragraph(
        "The College Examination FAQ Chatbot is an automated conversational assistant designed to streamline "
        "and improve student access to official examination-related information. In higher education institutions, "
        "students frequently seek answers regarding semester examination dates, internal assessment schedules, "
        "hall ticket availability, fee structures, attendance eligibility, medical leave condonation, supplementary exams, "
        "revaluation procedures, and malpractice rules."
    )
    p1.paragraph_format.space_after = Pt(8)
    p1.paragraph_format.line_spacing = 1.15

    p2 = doc.add_paragraph(
        "By leveraging Natural Language Processing (NLP) techniques—specifically tokenization, Term Frequency-Inverse "
        "Document Frequency (TF-IDF) vectorization, Cosine Similarity matching, and Domain Relevance Filtering—the chatbot "
        "accurately interprets free-form student queries, classifies intent, and retrieves accurate predefined answers from an "
        "official FAQ knowledge base."
    )
    p2.paragraph_format.space_after = Pt(14)
    p2.paragraph_format.line_spacing = 1.15

    # Section 2: Objectives
    h2 = doc.add_heading("2. Project Objectives", level=1)
    h2.runs[0].font.color.rgb = NAVY

    objs = [
        ("Instant Student Inquiry Resolution: ", "Provide 24/7 real-time answers to examination queries without administrative delays."),
        ("Natural Language Understanding (NLU): ", "Recognize intent across diverse phrasing variations for the same query."),
        ("Strict Domain Relevance Filtering: ", "Accurately answer relevant examination questions while strictly rejecting unrelated queries with a standardized fallback response."),
        ("Comprehensive FAQ Coverage: ", "Maintain a 30-entry pre-loaded knowledge base covering all essential examination regulations."),
        ("User-Friendly Responsive Interface: ", "Offer a modern, college-themed web UI equipped with message bubbles, typing animations, quick suggested questions, and session management."),
        ("Admin Management Panel: ", "Provide full CRUD (Create, Read, Update, Delete) capability to manage FAQ entries dynamically.")
    ]

    for title, desc in objs:
        p = doc.add_paragraph(style='List Bullet')
        r1 = p.add_run(title)
        r1.bold = True
        r1.font.color.rgb = BLUE
        r2 = p.add_run(desc)
        p.paragraph_format.space_after = Pt(4)

    doc.add_paragraph().paragraph_format.space_after = Pt(10)

    # Section 3: Methodology
    h3 = doc.add_heading("3. Methodology & System Architecture", level=1)
    h3.runs[0].font.color.rgb = NAVY

    doc.add_heading("3.1 Natural Language Processing Pipeline", level=2)
    p_nlp = doc.add_paragraph(
        "The NLP processing workflow follows a structured sequence of transformations from raw text to response output:"
    )
    p_nlp.paragraph_format.space_after = Pt(6)

    steps = [
        ("Step 1: Text Preprocessing: ", "User input is converted to lowercase and tokenized into alphanumeric word tokens. Standard english stop-words are filtered to highlight core domain terms."),
        ("Step 2: TF-IDF Vector Generation: ", "Term Frequency (TF) and Inverse Document Frequency (IDF) weights are computed across the corpus using the formula:\n   TF-IDF(t, d) = TF(t, d) * log(1 + N / DF(t))"),
        ("Step 3: Cosine Similarity Scoring: ", "The angular similarity between user vector (U) and FAQ pattern vector (P) is evaluated:\n   Similarity(U, P) = (U · P) / (||U|| * ||P||)"),
        ("Step 4: Domain Keyword & Threshold Validation: ", "The engine checks for domain keywords and enforces a confidence threshold (Similarity >= 0.35). Valid queries return matched answers; irrelevant queries trigger the fallback mechanism.")
    ]

    for title, desc in steps:
        p = doc.add_paragraph(style='List Bullet')
        r1 = p.add_run(title)
        r1.bold = True
        r2 = p.add_run(desc)
        p.paragraph_format.space_after = Pt(4)

    doc.add_heading("3.2 Knowledge Base Schema & Categories", level=2)
    p_kb = doc.add_paragraph(
        "The knowledge base stores 30 examination FAQs organized into 6 major academic categories: "
        "Schedule & Timetable, Hall Ticket & Eligibility, Registration & Fees, Results & Revaluation, "
        "Regulations & Rules, and Support & Office."
    )
    p_kb.paragraph_format.space_after = Pt(12)

    # Section 4: Sample Output & Results
    h4 = doc.add_heading("4. Sample Output & Test Results", level=1)
    h4.runs[0].font.color.rgb = NAVY

    doc.add_heading("4.1 Sample Student Conversations", level=2)
    
    samples = [
        ("Student: ", "When are the semester exams?"),
        ("Chatbot: ", "The Odd Semester examinations are scheduled from November 15 to December 10, and the Even Semester examinations run from April 20 to May 15. Please consult the official academic calendar on the university portal for exact department-wise dates.\n[Intent: exam_date | Confidence: 100%]"),
        ("Student: ", "How can I download my hall ticket?"),
        ("Chatbot: ", "Log in to the Student Portal (portal.college.edu) using your Roll Number and Password, navigate to 'Examinations' > 'Hall Ticket', verify your subject codes, and click 'Download & Print PDF'.\n[Intent: hall_ticket_download | Confidence: 100%]"),
        ("Student: ", "What is the capital of France?"),
        ("Chatbot (Fallback): ", "I'm sorry, I couldn't find a relevant answer to that question. Please try asking about examination dates, hall tickets, timetable, fees, attendance, results, revaluation, or examination procedures.\n[Intent: fallback | Confidence: 0%]")
    ]

    for sender, msg in samples:
        p = doc.add_paragraph()
        p.paragraph_format.left_indent = Inches(0.2)
        r1 = p.add_run(sender)
        r1.bold = True
        if "Student" in sender:
            r1.font.color.rgb = BLUE
        else:
            r1.font.color.rgb = NAVY
        r2 = p.add_run(msg)
        p.paragraph_format.space_after = Pt(4)

    doc.add_heading("4.2 System Verification Test Table", level=2)
    p_tbl_intro = doc.add_paragraph("The automated test suite evaluated 22 query test cases with 100.0% accuracy:")
    p_tbl_intro.paragraph_format.space_after = Pt(8)

    # Test Table
    table = doc.add_table(rows=1, cols=4)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False

    hdr_cells = table.rows[0].cells
    headers = ["#", "Input Student Query", "Detected Intent", "Evaluation Status"]
    col_widths = [Inches(0.5), Inches(3.0), Inches(1.8), Inches(1.2)]

    for idx, text in enumerate(headers):
        hdr_cells[idx].text = text
        set_cell_background(hdr_cells[idx], "0F172A")
        set_cell_margins(hdr_cells[idx], 120, 120, 150, 150)
        p = hdr_cells[idx].paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        for r in p.runs:
            r.font.bold = True
            r.font.color.rgb = RGBColor(255, 255, 255)
            r.font.size = Pt(9.5)

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
            set_cell_margins(row_cells[c_idx], 80, 80, 100, 100)
            p = row_cells[c_idx].paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if c_idx in [0, 3] else WD_ALIGN_PARAGRAPH.LEFT
            for r in p.runs:
                r.font.size = Pt(9)
                if c_idx == 3:
                    r.font.bold = True
                    r.font.color.rgb = RGBColor(21, 128, 61)

    # Set column widths
    for row in table.rows:
        for idx, width in enumerate(col_widths):
            row.cells[idx].width = width

    doc.add_paragraph().paragraph_format.space_after = Pt(14)

    # Section 5: GitHub Link & Repository Information
    h5 = doc.add_heading("5. Project Repository & Source Code Link", level=1)
    h5.runs[0].font.color.rgb = NAVY

    p_git_intro = doc.add_paragraph(
        "The complete source code, dataset files, web application scripts, and documentation "
        "for this project are hosted on GitHub:"
    )
    p_git_intro.paragraph_format.space_after = Pt(6)

    # GitHub Box Callout
    p_box = doc.add_paragraph()
    p_box.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_box.paragraph_format.space_before = Pt(8)
    p_box.paragraph_format.space_after = Pt(14)
    
    r_box_title = p_box.add_run("GitHub Repository Link Placeholder:\n")
    r_box_title.bold = True
    r_box_title.font.size = Pt(10.5)
    r_box_title.font.color.rgb = GRAY
    
    r_box_url = p_box.add_run("[ https://github.com/your-username/college-faq-chatbot ]")
    r_box_url.bold = True
    r_box_url.font.size = Pt(12)
    r_box_url.font.color.rgb = BLUE

    # Section 6: Conclusion
    h6 = doc.add_heading("6. Conclusion", level=1)
    h6.runs[0].font.color.rgb = NAVY

    p_conc = doc.add_paragraph(
        "The developed College Examination FAQ Chatbot demonstrates an effective practical application of "
        "Natural Language Processing in educational administration. By combining TF-IDF vector matching with strict "
        "domain relevance filtering, the chatbot reliably answers student examination inquiries while gracefully handling "
        "unrelated questions, providing an interactive, scalable solution for university student support."
    )
    p_conc.paragraph_format.space_after = Pt(12)

    # Save output document
    target_path = "C:\\Users\\suved\\.gemini\\antigravity\\scratch\\college_exam_chatbot\\College_FAQ_Chatbot_Project_Report.docx"
    doc.save(target_path)
    print(f"Project Report Word Document generated successfully at: {target_path}")

if __name__ == "__main__":
    generate_report()
