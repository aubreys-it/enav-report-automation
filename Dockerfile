# Use Microsoft's official Azure Functions Python base image
FROM mcr.microsoft.com/azure-functions/python:4-python3.11

# Set the working directory
WORKDIR /home/site/wwwroot

# Copy requirements and install Python packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install Playwright and its Chromium browser
RUN playwright install chromium
RUN playwright install-deps chromium

# Copy the rest of your app
COPY . .

CMD ["python", "main.py"]