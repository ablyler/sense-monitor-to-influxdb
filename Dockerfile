FROM python:3.9-slim

# Setup env
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONFAULTHANDLER 1

# Install pipenv and compilation dependencies
RUN pip install pipenv
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    python3-aiohttp \
    && rm -rf /var/lib/apt/lists/*

# Create and switch to a new user
RUN useradd --create-home appuser
WORKDIR /home/appuser
USER appuser

# Install application into container
COPY . .

# Install the requirements
RUN pipenv requirements > requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Run the application
CMD ["python", "sense-monitor-to-influxdb.py"]