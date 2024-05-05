import streamlit as st
import PyPDF2
from reportlab.lib.pagesizes import letter
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from streamlit_pdf_viewer import pdf_viewer
import webbrowser

# Function to add tables to PDF
def add_tables_to_pdf(original_pdf_path, output_pdf_path, data_table1, data_table2, data_table3):
    # Open the original PDF
    with open(original_pdf_path, 'rb') as pdf_file:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        pdf_writer = PyPDF2.PdfWriter()

        # Get the first page of the original PDF
        first_page = pdf_reader.pages[0]

        # Create a canvas
        c = canvas.Canvas("temp.pdf", pagesize=letter)

        # Draw the original PDF page onto the canvas
        first_page.merge_page(first_page)

        # Add table 1 at the top of the page
        table1 = Table(data_table1)
        table1.setStyle(TableStyle([('GRID', (0, 0), (-1, -1), 1, colors.black)]))  # Set grid lines for the table
        table1.wrapOn(c, 0, 0)
        table1.drawOn(c, 50, 700)  # Move table1 to coordinates (50, 700) at the top of the page

        # Add table 2
        table2 = Table(data_table2)
        table2.setStyle(TableStyle([('GRID', (0, 0), (-1, -1), 1, colors.black)]))  # Set grid lines for the table
        table2.wrapOn(c, 0, 0)
        table2.drawOn(c, 50, 400)  # Move table2 to coordinates (50, 400) on the page

        # Add table 3 at the bottom of the page
        table3 = Table(data_table3)
        table3.setStyle(TableStyle([('GRID', (0, 0), (-1, -1), 1, colors.black)]))  # Set grid lines for the table
        table3.wrapOn(c, 0, 0)
        table3.drawOn(c, 50, 70)  # Move table3 to coordinates (50, 50) at the bottom of the page

        # Save the canvas
        c.save()

        # Merge the canvas page with the original PDF page
        first_page.merge_page(PyPDF2.PdfReader("temp.pdf").pages[0])

        # Add the modified page (after the first page) to the PDF writer
        pdf_writer.add_page(first_page)

        # Add the remaining pages from the original PDF
        for page in pdf_reader.pages[1:]:
            pdf_writer.add_page(page)

        # Write the output PDF file
        with open(output_pdf_path, 'wb') as output_pdf_file:
            pdf_writer.write(output_pdf_file)

# Example data for tables
data_table1 = [['Date', 'Bill no', 'Name of customer'],
               ['2024-05-04', '12345', 'John Doe']]

data_table2 = [['Sr no', 'Category of clothes', 'Cost'],
               ['1', 'Saree', '$100'],
               ['2', 'Lehengha', '$150'],
               ['3', 'Gown', '$120']]

data_table3 = [['Total amount', '$370']]

add_tables_to_pdf("Bill_template.pdf", "output.pdf", data_table1, data_table2, data_table3)

st.title("View PDF")


pdf_viewer("output.pdf")
# def read_pdf_file(file_path):
#     with open(file_path, "rb") as file:
#         pdf_bytes = file.read()
#     return pdf_bytes

# pdf_file_path = "output.pdf"

# # Read the PDF file
# pdf_bytes = read_pdf_file(pdf_file_path)

# # Display the PDF in Streamlit
# st.write(pdf_bytes, media_type="application/pdf")

import subprocess
import os

def print_pdf(pdf_file_path, printer_name=None):
    if not os.path.exists(pdf_file_path):
        print("Error: PDF file does not exist.")
        return

    # Use default printer if printer_name is not provided
    printer_option = ""
    if printer_name:
        printer_option = f"/d:{printer_name}"

    # Print PDF using default PDF viewer
    try:
        subprocess.run(['start', 'AcroRd32', '/p', pdf_file_path], shell=True)
    except FileNotFoundError:
        print("Error: Adobe Acrobat Reader not found. Please install Adobe Acrobat Reader.")

    # Alternative way without relying on default PDF viewer
    # subprocess.run(['AcroRd32', '/t', pdf_file_path, printer_option], shell=True)

# Example usage
pdf_file_path_1 = "output.pdf"
printer_name = "Your_Printer_Name"  # Change this to your printer's name
cb = st.checkbox("Print PDF")
if cb:
    print_pdf(pdf_file_path_1, printer_name)

def open_pdf_in_new_tab(pdf_file_path):
    url = f"file:///{pdf_file_path}"
    webbrowser.open_new_tab(url)

# Example usage Replace this with the path to your PDF file
script_directory = os.path.dirname(os.path.abspath(__file__))
pdf_file_path_2 = os.path.join(script_directory, "output.pdf")

cb2 = st.checkbox("Open PDF")
if cb2:
    open_pdf_in_new_tab(pdf_file_path_2)
#########################################################################
def download_pdf(pdf_file_path):
    with open(pdf_file_path, "rb") as file:
        pdf_bytes = file.read()
    st.download_button(label="Download PDF", data=pdf_bytes, file_name="output.pdf", mime="application/pdf")

# Example usage
pdf_file_path = "output.pdf"  # Replace this with the path to your PDF file
download_pdf(pdf_file_path)
