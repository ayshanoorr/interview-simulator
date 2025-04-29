import os
from PyPDF2 import PdfReader
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA

def extract_text(file):
    reader = PdfReader(file.file)
    return " ".join([page.extract_text() for page in reader.pages if page.extract_text()])

async def process_interview(resume_file, jobdesc_file, difficulty):
    from app.resources.utils import extract_text

    resume_text = extract_text(resume_file)
    jobdesc_text = extract_text(jobdesc_file)

    combined = f"Resume:\n{resume_text}\n\nJob Description:\n{jobdesc_text}"
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    docs = splitter.create_documents([combined])

    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_documents(docs, embeddings)
    retriever = vectorstore.as_retriever()

    llm = ChatOpenAI(model_name="gpt-4", temperature=0.7)
    qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)

    prompt = f"""
    You're an AI interviewer. Conduct a {difficulty}-level mock interview.
    Ask the user 3 interview questions based on their resume and the job description.
    Output each question on a new line. Don’t include answers.
    """

    response = qa_chain.run(prompt)
    return {"interview_round": response}
