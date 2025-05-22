# Python runtime 
FROM python:3.13-slim-bookworm

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Work dir i container
WORKDIR /app

# Justeringer for vår spesielle filstruktur
COPY backend/requirements.txt /app/
# Python dependencies
RUN pip install -r requirements.txt


# Kopi av backend code til container work dir
COPY backend/ /app/


RUN python manage.py collectstatic --noinput --clear

# Porten appen er tilgjengelig på
EXPOSE 8000

# Command to run the application using Gunicorn
# Replace 'config' if your project directory (containing wsgi.py) is named differently
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "config.wsgi:application"]