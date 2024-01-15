# Use the official Python 3.9 image
FROM python:3.11

ADD . /app
WORKDIR /app
# Copy the current directory contents into the container at /code
COPY ./requirements.txt /code/requirements.txt

# Install requirements.txt 
RUN pip install --upgrade -r /code/requirements.txt

EXPOSE 5000
CMD ["python", "app.py","--port", "5000"]