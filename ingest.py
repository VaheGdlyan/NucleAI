import os
import glob
from dotenv import load_dotenv
import pypdf
import chromadb
from chromadb.utils import embedding_functions

# Load environment variables from .env
load_dotenv()

def split_text(text, chunk_size=1000, chunk_overlap=200):
    """
    Pure Python text chunker that splits text into manageable pieces with overlap.
    Bypasses the need for langchain_text_splitters (which loads heavy/buggy PyTorch on Windows).
    """
    chunks = []
    paragraphs = text.split("\n\n")
    current_chunk = ""
    
    for paragraph in paragraphs:
        paragraph = paragraph.strip()
        if not paragraph:
            continue
        
        # If paragraph is too large, split it further by lines
        if len(paragraph) > chunk_size:
            sub_parts = paragraph.split("\n")
            for part in sub_parts:
                part = part.strip()
                if not part:
                    continue
                
                # If a line is still too large, split by spaces (words)
                if len(part) > chunk_size:
                    words = part.split(" ")
                    for word in words:
                        if len(current_chunk) + len(word) + 1 > chunk_size:
                            if current_chunk:
                                chunks.append(current_chunk)
                            overlap_start = max(0, len(current_chunk) - chunk_overlap)
                            current_chunk = current_chunk[overlap_start:] + " " + word if current_chunk else word
                        else:
                            current_chunk = current_chunk + " " + word if current_chunk else word
                else:
                    if len(current_chunk) + len(part) + 1 > chunk_size:
                        if current_chunk:
                            chunks.append(current_chunk)
                        overlap_start = max(0, len(current_chunk) - chunk_overlap)
                        current_chunk = current_chunk[overlap_start:] + "\n" + part if current_chunk else part
                    else:
                        current_chunk = current_chunk + "\n" + part if current_chunk else part
        else:
            if len(current_chunk) + len(paragraph) + 2 > chunk_size:
                if current_chunk:
                    chunks.append(current_chunk)
                overlap_start = max(0, len(current_chunk) - chunk_overlap)
                current_chunk = current_chunk[overlap_start:] + "\n\n" + paragraph if current_chunk else paragraph
            else:
                current_chunk = current_chunk + "\n\n" + paragraph if current_chunk else paragraph
                
    if current_chunk:
        chunks.append(current_chunk)
        
    return [c.strip() for c in chunks if c.strip()]


def main():
    data_dir = "./data"
    persist_dir = "./chroma_db"
    
    # 1. Verify OpenAI API Key is present
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("[ERROR] OPENAI_API_KEY is not set in your .env file!")
        return

    # 2. Find all PDFs in the data folder
    pdf_files = glob.glob(os.path.join(data_dir, "*.pdf"))
    if not pdf_files:
        print(f"[ERROR] No PDF files found in {data_dir}!")
        return

    print(f"Found {len(pdf_files)} PDF files to process:")
    for f in pdf_files:
        print(f" - {os.path.basename(f)}")

    # 3. Load and parse documents using pypdf
    all_chunks = []
    chunk_metadata = []
    chunk_ids = []
    chunk_counter = 0

    for pdf_path in pdf_files:
        filename = os.path.basename(pdf_path)
        print(f"\nParsing {filename}...")
        try:
            reader = pypdf.PdfReader(pdf_path)
            print(f"  Loaded {len(reader.pages)} pages.")
            
            for page_num, page in enumerate(reader.pages):
                text = page.extract_text()
                if not text or not text.strip():
                    continue
                
                # Split this page's text
                page_chunks = split_text(text, chunk_size=1000, chunk_overlap=200)
                
                for idx, chunk in enumerate(page_chunks):
                    all_chunks.append(chunk)
                    chunk_metadata.append({
                        "source": filename,
                        "page": page_num + 1
                    })
                    chunk_ids.append(f"{filename}_p{page_num+1}_c{idx}")
                    chunk_counter += 1
                    
        except Exception as e:
            print(f"  Error loading {filename}: {str(e)}")

    if not all_chunks:
        print("[ERROR] No text could be extracted from PDFs. Exiting.")
        return

    print(f"\nExtracted a total of {chunk_counter} chunks from all PDFs.")

    # 4. Initialize OpenAI Embeddings via ChromaDB Native Client
    print("Initializing OpenAI Embeddings (text-embedding-3-small)...")
    openai_ef = embedding_functions.OpenAIEmbeddingFunction(
        api_key=api_key,
        model_name="text-embedding-3-small"
    )

    # 5. Create and persist Vector Store using PersistentClient
    print(f"Saving embeddings to local Chroma vector store at '{persist_dir}'...")
    try:
        client = chromadb.PersistentClient(path=persist_dir)
        
        # Get or create the collection
        collection = client.get_or_create_collection(
            name="nuclear_hub",
            embedding_function=openai_ef
        )
        
        # Batch insert to avoid size limits
        batch_size = 100
        for i in range(0, len(all_chunks), batch_size):
            batch_chunks = all_chunks[i:i+batch_size]
            batch_metadata = chunk_metadata[i:i+batch_size]
            batch_ids = chunk_ids[i:i+batch_size]
            
            collection.add(
                documents=batch_chunks,
                metadatas=batch_metadata,
                ids=batch_ids
            )
            print(f"  Processed {min(i + batch_size, len(all_chunks))}/{len(all_chunks)} chunks...")
            
        print(f"\nSuccessfully created local vector store with {len(all_chunks)} embedded chunks!")
    except Exception as e:
        print(f"[ERROR] Error creating vector store: {str(e)}")

if __name__ == "__main__":
    main()
