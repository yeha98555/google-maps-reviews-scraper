FROM python:3.12-slim

WORKDIR /app

RUN pip install poetry
RUN apt-get update && apt-get install -y make
# Install Node.js, npm
RUN apt-get update && apt-get install -y curl
RUN curl -fsSL https://deb.nodesource.com/setup_16.x | bash -
RUN apt-get install -y nodejs

ENV CHROMEDRIVER_VERSION=124.0.6367.60 
# Install chrome
RUN apt-get update && apt-get install -y wget && apt-get install -y zip
RUN wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN apt-get install -y ./google-chrome-stable_current_amd64.deb
# Install chromedriver
RUN wget https://storage.googleapis.com/chrome-for-testing-public/$CHROMEDRIVER_VERSION/linux64/chromedriver-linux64.zip \
  && unzip chromedriver-linux64.zip && rm -dfr chromedriver_linux64.zip \
  && mv ./chromedriver-linux64/chromedriver /usr/local/share/chromedriver \
  && ln -s /usr/local/share/chromedriver /usr/local/bin/chromedriver \
  && ln -s /usr/local/share/chromedriver /usr/bin/chromedriver \
  && chmod +x /usr/bin/chromedriver

ENV PATH /usr/bin/chromedriver:$PATH

ENV GOOGLE_APPLICATION_CREDENTIALS=/app/crawler_gcp_keyfile.json

COPY . /app

RUN make install

# # Clean
# RUN make clean

# # RUN
# RUN make run

# Bash
CMD ["bash"]
