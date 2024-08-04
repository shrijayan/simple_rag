import os
import PyPDF2
from tqdm import tqdm

def pdf_extractor(pdf_path):
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
    return text

def process_pdfs(folder_path='data/raw_pdf', 
                 output_folder='data/processed_data', 
                 combined_output_file='data/processed_data/combined_text.txt'):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    combined_text = ""
    
    for filename in tqdm(os.listdir(folder_path)):
        if filename.endswith('.pdf'):
            pdf_path = os.path.join(folder_path, filename)
            text = pdf_extractor(pdf_path)
            
            # Save individual text file
            output_text_path = os.path.join(output_folder, f"{os.path.splitext(filename)[0]}.txt")
            with open(output_text_path, 'w', encoding='utf-8') as text_file:
                text_file.write(text)
            
            # Append to combined text
            combined_text += text
            
            # Delete the original PDF
            os.remove(pdf_path)
    
    # Save the combined text file
    with open(combined_output_file, 'w', encoding='utf-8') as combined_file:
        combined_file.write(combined_text)
    
    print(f"All PDFs have been processed and combined text is saved to {combined_output_file}")

# Main guard to allow running as a script or importing
if __name__ == '__main__':
    folder_path = '../data/raw_pdf'
    output_folder = '../data/processed_data'
    combined_output_file = '../data/processed_data/combined_text.txt'
    process_pdfs()
