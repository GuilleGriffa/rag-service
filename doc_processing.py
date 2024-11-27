from io import BytesIO
from fastapi import UploadFile, HTTPException
import docx

async def load_document(file: UploadFile) -> str:
    """
    Load the DOCX file from the uploaded file and extract the text.
    
    :param file: Uploaded DOCX file
    :return: Extracted text from the document
    """
    try:
        # Check if the file is a DOCX file
        if not file.filename.endswith(".docx"):
            raise HTTPException(status_code=400, detail="Invalid file type. Only DOCX files are accepted.")
        
        file_content = await file.read()  # Read the content of the file
        doc = docx.Document(BytesIO(file_content))  # Use BytesIO to read the in-memory file

        # Extract text from paragraphs, ignoring empty paragraphs
        document_text = "\n\n".join(para.text for para in doc.paragraphs if para.text.strip() != "")
        return document_text
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading document: {e}")

def split_document_into_chunks(document_text: str) -> list:
    """
    Split the document text into chunks (by paragraphs).
    :param document_text: Text to be split into chunks
    :return: List of text chunks
    """

    chunks = document_text.split("\n\n")
    return chunks
