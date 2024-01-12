import os
from langchain.document_loaders import PyPDFLoader
import shutil

# Define DatasetLoader class to load the scientific dataset
class DatasetLoader:
    def __init__(self, client, resource, local, bucket) -> None:
        self.client = client
        self.resource = resource
        self.local = local
        self.bucket = bucket
        if not os.path.exists(self.local):
            os.makedirs(self.local)

    def download_dir(self):
        # select bucket
        my_bucket = self.resource.Bucket(self.bucket)

        # download file into current directory
        for s3_object in my_bucket.objects.all():
            # Need to split s3_object.key into path and file name, else it will give error file not found.
            path, filename = os.path.split(s3_object.key)
            my_bucket.download_file(s3_object.key, os.path.join(self.local, filename))

    def load_dataset(self):
        self.download_dir()
        try:
            print("Loading Files Started...")
            # Get a list of all files in the folder
            all_files = os.listdir(self.local)
            
            # Filter for files with a .pdf extension
            pdf_files = [file for file in all_files if file.lower().endswith(".pdf")]
            
            # Initialize a list to store loaded documents
            loaded_documents = []

            # Load documents from each PDF file
            for pdf_file in pdf_files:
                file_path = os.path.join(self.local, pdf_file)
                loader = PyPDFLoader(file_path)  # Replace with your actual document loader
                documents = loader.load()
                loaded_documents.extend(documents)
            print("Documents loaded succesfully.")
            try:
                # Delete the folder and its contents
                shutil.rmtree(self.local)
                print(f"Folder '{self.local}' and its contents successfully deleted.")
            except Exception as e:
                print(f"Error: {e}")
            return loaded_documents

        except FileNotFoundError:
            print(f"Error: Folder not found - {self.local}")
        except Exception as e:
            print(f"Error: Unable to load documents - {e}")

        return None