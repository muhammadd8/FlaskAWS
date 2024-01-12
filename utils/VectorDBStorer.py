# Import necessary modules
from utils.DatasetLoader import DatasetLoader
from utils.DataPreprocessor import DataPreprocessor
import boto3
import os

class VectorDBStorer:
    def __init__(self, client, collection_name, text_splitter, bucket):
        self.client = client
        self.collection_name = collection_name
        self.text_splitter = text_splitter
        self.bucket = bucket
        self.aws_access_key = "AKIA5FTZCAUESUQRSNZY"
        self.aws_secret_key = "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"
        self.region_name = "eu-north-1"

    def store_Vectordb(self):
        # Try to store Vectordb
        try:
            collection = self.client.get_or_create_collection(name=self.collection_name)
            print(f"Collection '{self.collection_name}' exists!")

            if len(collection.get()['documents']) == 0:
                # Load articles from dataset
                client = boto3.client('s3', aws_access_key_id=self.aws_access_key, aws_secret_access_key=self.aws_secret_key, region_name=self.region_name)
                resource = boto3.resource('s3', aws_access_key_id=self.aws_access_key, aws_secret_access_key=self.aws_secret_key, region_name=self.region_name)
                path = os.path.join(os.getcwd(),'temp')
                articles = DatasetLoader(client, resource, path, bucket=self.bucket).load_dataset()
                # Preprocess articles
                docs = DataPreprocessor(self.text_splitter).preprocessing_dataset(articles)
                
                # Add documents to collection
                collection.add(
                    ids=[str(i) for i in range(len(docs))],
                    documents=[str(i.page_content) for i in docs],
                    metadatas=[{"type": "support"} for _ in range(len(docs))],
                )
        except ValueError:
            print(f"Collection '{self.collection_name}' does not exist.")

        return collection

    def get_collection(self):
        return self.store_Vectordb()
    
    def get_collection_only(self):
        return self.client.get_collection(name=self.collection_name)
