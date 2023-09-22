FROM python:3.11-slim

# Setup env
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONFAULTHANDLER 1

# Install compilation dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip, setuptools, wheel, aiohttp and pipenv
RUN python3 -m pip install --no-cache-dir --upgrade pip setuptools wheel aiohttp pipenv

# Create and switch to a new user
RUN useradd --create-home appuser
WORKDIR /home/appuser
USER appuser

# Get Rust
RUN curl https://sh.rustup.rs -sSf | sh -s -- -y
ENV PATH="/home/appuser/.local/bin:/home/appuser/.cargo/bin:${PATH}"

# Install application into container
COPY . .

# Install the requirements
RUN pipenv requirements > requirements.txt \
    && pip3 install --no-cache-dir -r requirements.txt

# Run the application
CMD ["python3", "sense-monitor-to-influxdb.py"]