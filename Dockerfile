# Python runtime
FROM python:3.13-slim-bookworm

# Set environment variables with corrected format
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Work dir i container
WORKDIR /app

# Copy requirements first for layer caching
# Assuming backend/requirements.txt exists in your build context
COPY backend/requirements.txt ./requirements.txt
# Python dependencies
RUN pip install -r ./requirements.txt

# Kopi av backend code til container work dir
# Changed from "COPY backend/ /app/" to "COPY backend/ ."
# This copies the *contents* of your host's 'backend' directory
# into the current WORKDIR (/app) in the container.
COPY backend/ .

# Add and make the entrypoint script executable
# Assuming entrypoint.sh is in the same directory as your Dockerfile
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# Collect static files
# This assumes manage.py is now at /app/manage.py (copied from backend/manage.py)
RUN python manage.py collectstatic --noinput --clear

# Porten appen er tilgjengelig på
EXPOSE 8000

ENTRYPOINT ["/app/entrypoint.sh"]

# Command to run the application using Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "config.wsgi:application"]