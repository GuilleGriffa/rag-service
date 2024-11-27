from io import BytesIO
from fastapi import UploadFile, HTTPException
import docx

async def load_document(file: UploadFile) -> str:
    """
    Load the DOCX file from the uploaded file and extract the text.
    
    :param file: Uploaded DOCX file
    :return: Extracted text from the document
    """
    file_content = await file.read()  # Read the content of the file
    doc = docx.Document(BytesIO(file_content))  # Use BytesIO to read the in-memory file
    document_text = "\n\n".join([para.text for para in doc.paragraphs if para.text.strip() != ""])
    return document_text

def split_document_into_chunks(document_text: str) -> list:
    """Split the document text into chunks (by paragraphs)."""
    chunks = document_text.split("\n\n")
    return chunks
