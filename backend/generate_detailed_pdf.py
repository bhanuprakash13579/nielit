from fpdf import FPDF
import os

class QA_PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 15)
        self.cell(0, 10, 'Project SAMARTH - Detailed QA Execution Script', 0, 1, 'C')
        self.ln(5)

    def chapter_title(self, label):
        self.set_font('Arial', 'B', 12)
        self.set_fill_color(200, 220, 255)
        self.cell(0, 8, label, 0, 1, 'L', 1)
        self.ln(4)

    def test_case(self, id, title, steps, expected):
        self.set_font('Arial', 'B', 10)
        self.cell(20, 6, id, 0, 0)
        self.cell(0, 6, title, 0, 1)
        
        self.set_font('Arial', 'I', 9)
        self.cell(20, 6, "How:", 0, 0)
        self.set_font('Arial', '', 9)
        self.multi_cell(0, 6, steps)
        
        self.set_font('Arial', 'I', 9)
        self.cell(20, 6, "Expect:", 0, 0)
        self.set_font('Arial', '', 9)
        self.multi_cell(0, 6, expected)
        
        self.cell(0, 6, "[   ] Pass      [   ] Fail", 0, 1, 'R')
        self.ln(4)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(4)

pdf = QA_PDF()
pdf.add_page()
pdf.set_auto_page_break(auto=True, margin=15)

# SECTION 1
pdf.chapter_title("SECTION 1: RFP COMPLIANCE (Non-Negotiable)")
pdf.test_case("RFP-01", "Verify No Student Role", 
              "1. Logout if logged in.\n2. Look for 'Sign Up' button.\n3. Try to login as 'student'/'password'.", 
              "No Sign Up button exists. Student login fails with 'Invalid credentials'.")
pdf.test_case("RFP-02", "Verify Metadata Only (No Uploads)", 
              "1. Login as Admin.\n2. Go to 'Content' -> 'Add Content'.\n3. Look for a 'File Upload' button.", 
              "There is NO file upload button. Only Title, Duration text fields exist.")

# SECTION 2
pdf.chapter_title("SECTION 2: INVENTORY & REPORTS")
pdf.test_case("INV-01", "Create Inventory Item", 
              "1. Go to Inventory.\n2. Click 'Add Item'.\n3. Enter Kit ID: 'TEST-01', Name: 'Pi', State: 'Assam'.\n4. Click 'Save'.", 
              "Item appears in the list immediately.")
pdf.test_case("INV-02", "Check Hierarchical Location", 
              "1. Look at the 'Location' column for the item you just created.", 
              "It shows 'Assam / [District]' format, NOT just a generic string.")
pdf.test_case("INV-03", "Export Excel Report", 
              "1. Click the 'Export Excel' button on the top right.", 
              "A file 'Inventory_Report.xlsx' downloads. Open it to verify data.")

# SECTION 3
pdf.chapter_title("SECTION 3: DASHBOARD & AUDIT")
pdf.test_case("DSH-01", "Real-Time Audit Feed", 
              "1. Perform an action (like Add Item from INV-01).\n2. Go to Dashboard immediately.\n3. Look at 'Recent Audit Activity'.", 
              "You see 'CREATE_INVENTORY' logged with the current time (e.g. 14:05).")
pdf.test_case("DSH-02", "Execution Phase Tracker", 
              "1. Look at 'Project Execution Phases' widget on Dashboard.", 
              "It shows 'Phase 1: Mobilization' in Green. It exists.")

# SECTION 4
pdf.chapter_title("SECTION 4: TRAINING & NDU")
pdf.test_case("TRN-01", "View Attendance (Compliance)", 
              "1. Go to Training.\n2. Create a Schedule (if none).\n3. Click 'View Attendance' button.", 
              "An Alert pops up saying 'Compliance: Showing Attendance Sheet'.")

# Footer
pdf.ln(10)
pdf.set_font('Arial', 'I', 10)
pdf.cell(0, 10, "Tester Signature: _______________________      Date: _____________", 0, 1, 'C')

start_dir = os.path.expanduser("~")
output_path = os.path.join(start_dir, "Downloads", "Project_SAMARTH_QA_Detailed.pdf")
pdf.output(output_path)
print(f"PDF Generated at: {output_path}")
