FROM python
WORKDIR /app

# Install environment dependencies
RUN apt-get update && apt-get install -y \
  ffmpeg

# Get python dependencies needed
COPY ./requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
