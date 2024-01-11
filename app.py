from fastapi import FastAPI
from transformers import pipeline
from langchain.llms import CTransformers #to get llm
from langchain.prompts import ChatPromptTemplate
import chromadb
from langchain.text_splitter import RecursiveCharacterTextSplitter#splitting text into chunks
from utils.VectorDBStorer import VectorDBStorer
from utils.UploadData import UploadData
import os
from flask import Flask, render_template, request, redirect, send_file
from werkzeug.utils import secure_filename

# Create a new FastAPI app instance
app = Flask(__name__)
BUCKET = "hfdataset"
UPLOAD_FOLDER = "uploads"
aws_access_key = "AKIA5FTZCAUESUQRSNZY"
aws_secret_key = "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"
region_name = "eu-north-1"
bucket_name = "hfdataset"


""" Finetuning LLM """

client = chromadb.Client()
collection_name = "new_scientific_papers"
text_splitter = RecursiveCharacterTextSplitter(chunk_size=256, chunk_overlap=20)
dataset_name = 'scientific_papers'

vector_db_storer = VectorDBStorer(client, collection_name, text_splitter, dataset_name)
collection = vector_db_storer.get_collection()

llm = CTransformers(
    model = "TheBloke/Llama-2-7B-Chat-GGML",
    model_type="llama",
    temperature = 0.2
    )


custom_prompt_template = """Use the following pieces of information to answer the user’s question.

Context: {context}
Question: {question}

"""

prompt = ChatPromptTemplate.from_template(custom_prompt_template)
chain = prompt | llm


@app.get("/generate")
def generate(text: str):
    """
    Using the text2text-generation pipeline from `transformers`, generate text
    from the given input text. The model used is `google/flan-t5-small`, which
    can be found [here](<https://huggingface.co/google/flan-t5-small>).
    """
    results = collection.query(
                 query_texts=text,
                 n_results=1)
    context = results['documents'][0][0]
    question = text
    # Use the pipeline to generate text from the given input text
    output = chain.invoke({"context": context, "question": question})
    print(output)
    # Return the generated text in a JSON response
    return {"output": output}


@app.route("/")
def home():
    return render_template('index.html')

@app.route("/upload", methods=['POST'])
def upload():
    if request.method == "POST":
        f = request.files['file']
        if f:
            cwd = os.getcwd()
            print(cwd)
            f.save(os.path.join(UPLOAD_FOLDER, secure_filename(f.filename)))
            path = os.path.join(cwd, UPLOAD_FOLDER,f.filename)
            print(path)
            data = UploadData()
            # Upload the file to S3
            success, upload_response = data.upload(path, BUCKET)
            os.remove(path)
            # Display success or error message
            if success:
                message = "File successfully uploaded to S3!"
            else:
                message = f"Error uploading file to S3: {upload_response}"

            return render_template("index.html", message=message)
        return redirect("/")
    

if __name__ == '__main__':
    app.run(debug=True)