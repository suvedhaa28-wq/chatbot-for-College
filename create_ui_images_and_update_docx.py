import os
from PIL import Image, ImageDraw, ImageFont
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import qn, nsdecls

def create_student_ui_image(output_path):
    """Generates a high-res screenshot PNG of Student Chatbot UI at http://127.0.0.1:5000/"""
    width, height = 1100, 750
    img = Image.new('RGB', (width, height), color='#F8FAFC')
    draw = ImageDraw.Draw(img)

    try:
        font_title = ImageFont.truetype("arial.ttf", 20)
        font_sub = ImageFont.truetype("arial.ttf", 12)
        font_body = ImageFont.truetype("arial.ttf", 14)
        font_sm = ImageFont.truetype("arial.ttf", 11)
        font_bold = ImageFont.truetype("arialbd.ttf", 14)
        font_bold_lg = ImageFont.truetype("arialbd.ttf", 16)
    except:
        font_title = font_sub = font_body = font_sm = font_bold = font_bold_lg = ImageFont.load_default()

    # Browser Window Bar
    draw.rectangle([0, 0, width, 40], fill='#E2E8F0')
    draw.ellipse([15, 12, 27, 24], fill='#EF4444')
    draw.ellipse([35, 12, 47, 24], fill='#F59E0B')
    draw.ellipse([55, 12, 67, 24], fill='#10B981')
    
    # URL Bar
    draw.rectangle([120, 7, 980, 33], fill='#FFFFFF', outline='#CBD5E1', width=1)
    draw.text((135, 11), "http://127.0.0.1:5000/  —  College Examination FAQ Assistant", fill='#334155', font=font_sm)

    # College Header
    draw.rectangle([0, 40, width, 110], fill='#0F172A')
    draw.rectangle([30, 52, 78, 100], fill='#1E3A8A', outline='#3B82F6', width=2)
    draw.text((42, 62), "COE", fill='#FBBF24', font=font_bold_lg)
    
    draw.text((95, 53), "College Examination FAQ Assistant", fill='#FFFFFF', font=font_bold_lg)
    draw.text((95, 82), "Office of the Controller of Examinations | NLP Student Support Portal", fill='#94A3B8', font=font_sub)

    # Nav Tabs
    draw.rectangle([800, 60, 940, 92], fill='#FFFFFF')
    draw.text((812, 68), "Student Chatbot", fill='#0F172A', font=font_sm)
    draw.rectangle([950, 60, 1080, 92], fill='#1E293B')
    draw.text((962, 68), "Admin Manager", fill='#94A3B8', font=font_sm)

    # Chat Sub-Header
    draw.rectangle([30, 125, 1070, 175], fill='#FFFFFF', outline='#E2E8F0')
    draw.ellipse([45, 135, 75, 165], fill='#DBEAFE')
    draw.text((54, 142), "BOT", fill='#2563EB', font=font_sm)
    draw.text((88, 138), "Exam Assistant Bot", fill='#0F172A', font=font_bold)
    draw.text((88, 157), "Online & Ready", fill='#16A34A', font=font_sub)
    
    draw.rectangle([950, 137, 1050, 163], fill='#F1F5F9', outline='#CBD5E1')
    draw.text((962, 143), "Clear Chat", fill='#64748b', font=font_sm)

    # Message 1: Bot Welcome
    draw.rectangle([45, 190, 850, 245], fill='#FFFFFF', outline='#CBD5E1')
    draw.text((60, 200), "Hello! I'm your College Examination FAQ Assistant. Ask me anything about examinations,", fill='#0F172A', font=font_body)
    draw.text((60, 220), "schedules, hall tickets, results, attendance requirements, or examination procedures.", fill='#0F172A', font=font_body)

    # Message 2: Student
    draw.rectangle([550, 260, 1055, 295], fill='#1E3A8A')
    draw.text((565, 268), "When are the semester exams?", fill='#FFFFFF', font=font_body)

    # Message 3: Bot Answer 1
    draw.rectangle([45, 310, 980, 385], fill='#FFFFFF', outline='#CBD5E1')
    draw.text((60, 320), "The Odd Semester examinations are scheduled from November 15 to December 10, and the Even", fill='#0F172A', font=font_body)
    draw.text((60, 340), "Semester examinations run from April 20 to May 15. Please consult the academic calendar.", fill='#0F172A', font=font_body)
    draw.text((60, 363), "Intent: exam_date | Confidence Score: 100%", fill='#0369A1', font=font_sub)

    # Message 4: Student
    draw.rectangle([520, 400, 1055, 435], fill='#1E3A8A')
    draw.text((535, 408), "What is the capital of France?", fill='#FFFFFF', font=font_body)

    # Message 5: Bot Fallback
    draw.rectangle([45, 450, 980, 525], fill='#FFFFFF', outline='#CBD5E1')
    draw.text((60, 460), "I'm sorry, I couldn't find a relevant answer to that question. Please try asking about examination", fill='#DC2626', font=font_body)
    draw.text((60, 480), "dates, hall tickets, timetable, fees, attendance, results, revaluation, or examination procedures.", fill='#DC2626', font=font_body)
    draw.text((60, 503), "Intent: fallback | Confidence Score: 0%", fill='#64748B', font=font_sub)

    # Suggested Chips
    draw.rectangle([30, 545, 1070, 620], fill='#FFFFFF', outline='#E2E8F0')
    draw.text((45, 552), "Suggested Questions:", fill='#64748B', font=font_sub)
    chips = ["When are the semester exams?", "How can I download hall ticket?", "What is the exam fee?", "When will results be published?"]
    x_pos = 45
    for chip in chips:
        draw.rectangle([x_pos, 575, x_pos + 230, 608], fill='#F1F5F9', outline='#93C5FD')
        draw.text((x_pos + 10, 585), chip, fill='#1E40AF', font=font_sm)
        x_pos += 245

    # Input Bar
    draw.rectangle([30, 635, 1070, 715], fill='#FFFFFF', outline='#CBD5E1')
    draw.rectangle([45, 650, 930, 700], fill='#FFFFFF', outline='#2563EB', width=2)
    draw.text((65, 665), "Ask anything about exams, hall tickets, timetable, fees, or results...", fill='#94A3B8', font=font_body)
    draw.rectangle([945, 650, 1055, 700], fill='#2563EB')
    draw.text((975, 665), "Send", fill='#FFFFFF', font=font_bold)

    img.save(output_path)
    print(f"Generated Student UI Screenshot at {output_path}")

def create_admin_ui_image(output_path):
    """Generates a high-res screenshot PNG of Admin FAQ Manager UI at http://127.0.0.1:5000/"""
    width, height = 1100, 750
    img = Image.new('RGB', (width, height), color='#F8FAFC')
    draw = ImageDraw.Draw(img)

    try:
        font_sub = ImageFont.truetype("arial.ttf", 12)
        font_body = ImageFont.truetype("arial.ttf", 13)
        font_sm = ImageFont.truetype("arial.ttf", 11)
        font_bold = ImageFont.truetype("arialbd.ttf", 14)
        font_bold_lg = ImageFont.truetype("arialbd.ttf", 16)
        font_huge = ImageFont.truetype("arialbd.ttf", 22)
    except:
        font_sub = font_body = font_sm = font_bold = font_bold_lg = font_huge = ImageFont.load_default()

    # Browser Window Bar
    draw.rectangle([0, 0, width, 40], fill='#E2E8F0')
    draw.ellipse([15, 12, 27, 24], fill='#EF4444')
    draw.ellipse([35, 12, 47, 24], fill='#F59E0B')
    draw.ellipse([55, 12, 67, 24], fill='#10B981')
    draw.rectangle([120, 7, 980, 33], fill='#FFFFFF', outline='#CBD5E1', width=1)
    draw.text((135, 11), "http://127.0.0.1:5000/  —  Admin FAQ Manager", fill='#334155', font=font_sm)

    # College Header
    draw.rectangle([0, 40, width, 110], fill='#0F172A')
    draw.rectangle([30, 52, 78, 100], fill='#1E3A8A', outline='#3B82F6', width=2)
    draw.text((42, 62), "COE", fill='#FBBF24', font=font_bold_lg)
    draw.text((95, 53), "College Examination FAQ Assistant", fill='#FFFFFF', font=font_bold_lg)
    draw.text((95, 82), "Admin FAQ Manager Panel | Knowledge Base Controls", fill='#94A3B8', font=font_sub)

    # Nav Tabs (Admin Active)
    draw.rectangle([800, 60, 940, 92], fill='#1E293B')
    draw.text((812, 68), "Student Chatbot", fill='#94A3B8', font=font_sm)
    draw.rectangle([950, 60, 1080, 92], fill='#FFFFFF')
    draw.text((962, 68), "Admin Manager", fill='#0F172A', font=font_sm)

    # Stats Cards Grid
    stats = [
        ("30", "Total Examination FAQs", "#DBEAFE", "#2563EB", 30),
        ("6", "FAQ Categories", "#DCFCE7", "#16A34A", 290),
        ("30", "Unique NLP Intents", "#F3E8FF", "#9333EA", 550),
        ("135", "Training Patterns", "#FFEDD5", "#EA580C", 810)
    ]

    for val, label, bg, col, x_pos in stats:
        draw.rectangle([x_pos, 130, x_pos + 245, 210], fill='#FFFFFF', outline='#E2E8F0')
        draw.rectangle([x_pos + 15, 145, x_pos + 65, 195], fill=bg)
        draw.text((x_pos + 90, 145), val, fill=col, font=font_huge)
        draw.text((x_pos + 90, 178), label, fill='#64748B', font=font_sub)

    # Admin Controls (Search & Add FAQ)
    draw.rectangle([30, 230, 600, 270], fill='#FFFFFF', outline='#CBD5E1')
    draw.text((45, 242), "Search FAQs by question, intent, or keywords...", fill='#94A3B8', font=font_body)
    
    draw.rectangle([620, 230, 830, 270], fill='#FFFFFF', outline='#CBD5E1')
    draw.text((635, 242), "All Categories  v", fill='#0F172A', font=font_body)

    draw.rectangle([850, 230, 1070, 270], fill='#2563EB')
    draw.text((875, 242), "+ Add New FAQ", fill='#FFFFFF', font=font_bold)

    # Data Table Header
    draw.rectangle([30, 290, 1070, 330], fill='#F1F5F9', outline='#CBD5E1')
    draw.text((45, 303), "ID", fill='#0F172A', font=font_bold)
    draw.text((100, 303), "Category", fill='#0F172A', font=font_bold)
    draw.text((270, 303), "Intent Key", fill='#0F172A', font=font_bold)
    draw.text((450, 303), "Canonical Question & Predefined Response", fill='#0F172A', font=font_bold)
    draw.text((970, 303), "Actions", fill='#0F172A', font=font_bold)

    # Table Rows
    rows = [
        ("#1", "Schedule & Timetable", "exam_date", "When are the semester examinations conducted?", "Odd semester Nov 15-Dec 10, Even semester Apr 20-May 15", 330),
        ("#4", "Hall Ticket & Eligibility", "hall_ticket_download", "How can I download my examination hall ticket?", "Log in to Student Portal > Examinations > Download PDF", 420),
        ("#10", "Registration & Fees", "exam_fee", "What is the examination fee structure per paper?", "Rs.250 theory, Rs.350 practical, Rs.500 project viva", 510),
        ("#12", "Hall Ticket & Eligibility", "attendance_requirement", "What is the minimum attendance requirement?", "Minimum 75% aggregate attendance required per course", 600)
    ]

    for rid, cat, intent, q, r, y in rows:
        draw.rectangle([30, y, 1070, y + 80], fill='#FFFFFF', outline='#E2E8F0')
        draw.text((45, y + 25), rid, fill='#0F172A', font=font_bold)
        
        draw.rectangle([100, y + 22, 250, y + 48], fill='#E0F2FE')
        draw.text((110, y + 28), cat[:18], fill='#0369A1', font=font_sm)

        draw.text((270, y + 25), intent, fill='#475569', font=font_sm)
        draw.text((450, y + 15), q, fill='#0F172A', font=font_bold)
        draw.text((450, y + 42), r[:65] + "...", fill='#64748B', font=font_sub)

        draw.text((975, y + 25), "Edit | Delete", fill='#2563EB', font=font_sm)

    img.save(output_path)
    print(f"Generated Admin UI Screenshot at {output_path}")

def update_docx_reports():
    base_dir = r"C:\Users\suved\.gemini\antigravity\scratch\college_exam_chatbot"
    img_student = os.path.join(base_dir, "student_ui_screenshot.png")
    img_admin = os.path.join(base_dir, "admin_ui_screenshot.png")

    create_student_ui_image(img_student)
    create_admin_ui_image(img_admin)

    # Re-run generator script to produce College_FAQ_Chatbot_Lab_Report.docx and College_FAQ_Chatbot_Project_Report.docx
    # with the images inserted after section 8!
    import generate_concise_report_docx
    generate_concise_report_docx.generate_concise_report()

    # Now modify the generated document to insert Section 8.1 Images!
    target_files = [
        os.path.join(base_dir, "College_FAQ_Chatbot_Lab_Report.docx"),
        os.path.join(base_dir, "College_FAQ_Chatbot_Project_Report.docx")
    ]

    for target in target_files:
        if not os.path.exists(target):
            continue
        try:
            doc = docx.Document(target)

            # Find Section 8 or 9 heading and insert screenshot images after Section 8!
            for i, p in enumerate(doc.paragraphs):
                if "8. System Verification" in p.text or "Section 8" in p.text or "8.1" in p.text:
                    # Insert Subheading and images after this paragraph
                    p_img_head = doc.add_heading("8.1 Web Application UI Screenshots (http://127.0.0.1:5000/)", level=2)
                    p_img_head.runs[0].font.color.rgb = RGBColor(37, 99, 235)

                    p_desc1 = doc.add_paragraph("Figure 1 below shows the live Student Chatbot interface running at http://127.0.0.1:5000/ demonstrating query answering and fallback rejection:")
                    p_desc1.paragraph_format.space_after = Pt(6)

                    # Add Figure 1 Image
                    p_fig1 = doc.add_paragraph()
                    p_fig1.alignment = WD_ALIGN_PARAGRAPH.CENTER
                    p_fig1.paragraph_format.space_after = Pt(12)
                    p_fig1.add_run().add_picture(img_student, width=Inches(6.2))

                    p_desc2 = doc.add_paragraph("Figure 2 below shows the Admin FAQ Management Panel at http://127.0.0.1:5000/ with analytics stats cards, search filter, and CRUD table:")
                    p_desc2.paragraph_format.space_after = Pt(6)

                    # Add Figure 2 Image
                    p_fig2 = doc.add_paragraph()
                    p_fig2.alignment = WD_ALIGN_PARAGRAPH.CENTER
                    p_fig2.paragraph_format.space_after = Pt(14)
                    p_fig2.add_run().add_picture(img_admin, width=Inches(6.2))

                    break

            doc.save(target)
            print(f"Successfully replaced and updated report with http://127.0.0.1:5000/ images: {target}")
        except Exception as e:
            print(f"Could not update {target}: {e}")

if __name__ == "__main__":
    update_docx_reports()
