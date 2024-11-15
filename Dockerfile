# Use the official Python image as a base
FROM python:3.10
# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container
COPY . /app/

# Install the required dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Define the command to run the application
CMD ["python", "modeles_SQLAlchemy.py"]
