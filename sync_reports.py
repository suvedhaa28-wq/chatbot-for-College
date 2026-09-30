import os
import shutil

base_dir = r"C:\Users\suved\.gemini\antigravity\scratch\college_exam_chatbot"
src = os.path.join(base_dir, "College_FAQ_Chatbot_Lab_Report.docx")
dest = os.path.join(base_dir, "College_FAQ_Chatbot_Project_Report.docx")

if os.path.exists(src):
    shutil.copyfile(src, dest)
    print(f"Copied updated report to {dest}")
