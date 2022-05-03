FROM python:3.9-slim as base

# Setup env
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONFAULTHANDLER 1


FROM base AS python-deps

# Install pipenv and compilation dependencies
RUN pip install pipenv
RUN apt-get update && apt-get install -y --no-install-recommends gcc python3-aiohttp

# Generate requirements.txt in /
COPY Pipfile .
COPY Pipfile.lock .
RUN pipenv requirements > requirements.txt


FROM base AS runtime

# install python packages
RUN apt-get update && apt-get install -y --no-install-recommends python3-aiohttp

# Create and switch to a new user
RUN useradd --create-home appuser
WORKDIR /home/appuser
USER appuser

# Install application into container
COPY --from=python-deps /requirements.txt .
COPY . .

# Install the requirements
RUN pip install --no-cache-dir -r requirements.txt

# Run the application
CMD ["python", "sense-monitor-to-influxdb.py"]