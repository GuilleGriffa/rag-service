FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Copy all scripts from the current directory to the container
COPY . .

# Install the required dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port where the API will run
EXPOSE 8000

# Command to run FastAPI with Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
