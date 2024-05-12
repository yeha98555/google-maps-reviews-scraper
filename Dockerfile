FROM python:3.12-slim

WORKDIR /app

RUN pip install poetry
RUN apt-get update && apt-get install -y make
# Install Node.js, npm
RUN apt-get update && apt-get install -y curl
RUN curl -fsSL https://deb.nodesource.com/setup_16.x | bash -
RUN apt-get install -y nodejs

ENV GOOGLE_APPLICATION_CREDENTIALS=/app/crawler_gcp_keyfile.json

COPY . /app

RUN make install

# # Clean
# RUN make clean

# # RUN
# RUN make run

# Bash
CMD ["bash"]
