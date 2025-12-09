# Step 1: Use official Python image
FROM python:3.10

# Step 2: Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Step 3: Set work directory
WORKDIR /app

# Step 4: Install dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Step 5: Copy project code
COPY . /app/

# Step 6: Expose port (informational only)
EXPOSE 8000

# Step 7: Run the application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
