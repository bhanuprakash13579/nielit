from fpdf import FPDF
import os

pdf = FPDF()
pdf.add_page()
pdf.set_auto_page_break(auto=True, margin=15)

# Title
pdf.set_font("Arial", 'B', 16)
pdf.cell(0, 10, "Project SAMARTH - Master QA Suite", ln=True, align='C')
pdf.ln(10)

# Content
content = """
MASTER QA SUITE - PROJECT SAMARTH
Status: CONFIDENTIAL
Target: 100% Compliance

SECTION 1: CRITICAL RFP COMPLIANCE
[ ] RFP-01: No Student Role (Verify absence of signup)
[ ] RFP-02: No LMS Videos (Verify inability to upload mp4)
[ ] RFP-03: No Video Player (Verify content is metadata only)
[ ] RFP-04: Two Roles Only (Super Admin / Admin)
[ ] RFP-05: Offline Inventory (Physical location support)

SECTION 2: AUTHENTICATION & SECURITY
[ ] SEC-01: Valid Admin Login (Access Dashboard)
[ ] SEC-02: Invalid Password (Error Alert)
[ ] SEC-03: SQL Injection Attempt (Blocked)
[ ] SEC-04: Direct URL Access (Redirects to Login)
[ ] SEC-05: Session Persistence (Refresh works)
[ ] SEC-06: Logout (Clears session)

SECTION 3: INVENTORY MANAGEMENT
[ ] INV-01: Add Item (Happy Path)
[ ] INV-02: Duplicate ID Check (Error shown)
[ ] INV-03: Location Hierarchy Display (State/District)
[ ] INV-04: Export Excel (Download works)
[ ] INV-05: Export PDF (Download works)
[ ] INV-06: Empty Search Results
[ ] INV-07: Audit Log Verification

SECTION 4: TRAINING & BATCHES
[ ] TRN-01: Create Schedule
[ ] TRN-02: NDU Sync Button
[ ] TRN-03: View Attendance Button (Compliance Alert)
[ ] TRN-04: Batch Details View

SECTION 5: CONTENT METADATA
[ ] CNT-01: Add Practical Video Metadata
[ ] CNT-02: Verify Quality Flags (QC, Safe Checkboxes)
[ ] CNT-03: Dashboard Counter Increment
[ ] CNT-04: Validation (Required fields)

SECTION 6: EXECUTIVE DASHBOARD
[ ] DSH-01: Live Counters Match List
[ ] DSH-02: Milestone Phase Tracking (Phase 1)
[ ] DSH-03: Real-Time Audit Feed
[ ] DSH-04: Responsive Layout

SECTION 7: STABILITY
[ ] STB-01: Server Restart Recovery
[ ] STB-02: Data Persistence
[ ] STB-03: Stress Click Test

Tester Signature: _______________________
Date: _______________________
"""

pdf.set_font("Arial", size=11)
for line in content.split('\n'):
    if "SECTION" in line:
        pdf.set_font("Arial", 'B', 12)
        pdf.ln(5)
        pdf.cell(0, 10, line, ln=True)
        pdf.set_font("Arial", size=11)
    else:
        pdf.multi_cell(0, 7, line)

start_dir = os.path.expanduser("~")
output_path = os.path.join(start_dir, "Downloads", "Project_SAMARTH_QA_Suite.pdf")
pdf.output(output_path)
print(f"PDF Generated at: {output_path}")
