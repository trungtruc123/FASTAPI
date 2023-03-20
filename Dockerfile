#FROM ubuntu:21.10
FROM python:3.9

# Install some basic utilities
#RUN apt-get update && apt-get install -y \
#    curl \
#    ca-certificates \
#    sudo \
#    git \
#    bzip2 \
#    libx11-6 \
# && rm -rf /var/lib/apt/lists/*

# Create a working directory
#RUN mkdir /app
WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
RUN echo "Done"
COPY . .

#ENV http_proxy 127.0.0.1:5432
#ENV http_proxy 127.0.0.1:5432
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]