# Use the official Python 3.9 image
FROM python:3.11

ADD . /app
WORKDIR /app
# Copy the current directory contents into the container at /code
COPY ./requirements.txt /code/requirements.txt
 
# Install requirements.txt 
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
 
# Start the FastAPI app on port 7860, the default port expected by Spaces
# CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "7860"]
CMD ["python", "app.py"]