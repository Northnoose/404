# Use an official Python runtime as a parent image
FROM python:3.13-slim-bookworm

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory inside the container
WORKDIR /app

# --- Adjustments for your file structure ---
# Copy the requirements file from the backend subdirectory
COPY backend/requirements.txt /app/
# Install Python dependencies
RUN pip install -r requirements.txt

# Copy the entire backend project code into the container's work directory
COPY backend/ /app/
# --- End of Adjustments ---

RUN python manage.py collectstatic --noinput --clear

# Expose the port the app runs on
EXPOSE 8000

# Command to run the application using Gunicorn
# Replace 'config' if your project directory (containing wsgi.py) is named differently
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "config.wsgi:application"]