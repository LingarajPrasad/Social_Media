FROM python:3.10.1

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file to the container
COPY . /app

# Install dependencies
RUN pip install -r requirements.txt

# Copy the rest of the project files to the container
# COPY . .

# Expose the port that the application will be running on
# EXPOSE 8000

# Run the application
# CMD ["uvicorn app.main:app"]