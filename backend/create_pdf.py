"""
Script to generate notes.pdf
Run this script to create the sample PDF file:
python create_pdf.py
"""
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def create_notes_pdf():
    """Create a sample notes.pdf file"""
    pdf_path = "data/notes.pdf"
    c = canvas.Canvas(pdf_path, pagesize=letter)
    width, height = letter
    
    # Add title
    c.setFont("Helvetica-Bold", 16)
    c.drawString(100, height - 100, "Event Planning Notes")
    
    # Add content
    c.setFont("Helvetica", 12)
    y_position = height - 150
    
    notes = [
        "Conference Planning Notes - March 2026",
        "",
        "Venue Selection:",
        "After reviewing multiple venues, we selected City Convention Hall.",
        "Reasons: Central location, adequate capacity, good amenities.",
        "",
        "Logistics Decisions:",
        "- Transportation: Two charter buses arranged",
        "- Catering: ABC Caterers selected for quality and reliability",
        "- Security: Professional security team hired",
        "",
        "Budget Breakdown:",
        "- Venue rental: $5,000",
        "- Catering: $6,000",
        "- Transportation: $2,000",
        "- Security: $1,000",
        "- Miscellaneous: $1,000",
        "Total: $15,000",
        "",
        "Timeline:",
        "- March 12: Event day",
        "- March 10: Final confirmations",
        "- March 8: Equipment testing",
        "",
        "Important Contacts:",
        "- Venue: Jane Smith (555) 123-4567",
        "- Caterer: Bob Johnson (555) 234-5678",
        "- Bus Company: City Transport (555) 345-6789",
    ]
    
    for line in notes:
        c.drawString(100, y_position, line)
        y_position -= 20
        
        if y_position < 100:  # New page if needed
            c.showPage()
            y_position = height - 100
            c.setFont("Helvetica", 12)
    
    c.save()
    print(f"✅ Created {pdf_path}")

if __name__ == "__main__":
    # Check if reportlab is installed
    try:
        from reportlab.lib.pagesizes import letter
        from reportlab.pdfgen import canvas
        create_notes_pdf()
    except ImportError:
        print("⚠️  reportlab not installed. Install with: pip install reportlab")
        print("Creating a simple text version instead...")
        
        # Create a text version
        with open("data/notes_text_version.txt", "w") as f:
            f.write("""Conference Planning Notes - March 2026

Venue Selection:
After reviewing multiple venues, we selected City Convention Hall.
Reasons: Central location, adequate capacity, good amenities.

Logistics Decisions:
- Transportation: Two charter buses arranged
- Catering: ABC Caterers selected for quality and reliability
- Security: Professional security team hired

Budget Breakdown:
- Venue rental: $5,000
- Catering: $6,000
- Transportation: $2,000
- Security: $1,000
- Miscellaneous: $1,000
Total: $15,000

Timeline:
- March 12: Event day
- March 10: Final confirmations
- March 8: Equipment testing

Important Contacts:
- Venue: Jane Smith (555) 123-4567
- Caterer: Bob Johnson (555) 234-5678
- Bus Company: City Transport (555) 345-6789
""")
        print("✅ Created text version: data/notes_text_version.txt")
