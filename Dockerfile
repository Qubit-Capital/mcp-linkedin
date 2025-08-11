# Use a lightweight Python base image
FROM python:3.11-alpine

WORKDIR /app


# Copy Python dependency files and install
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . .

# Expose HTTP port
EXPOSE 8080

# Start the MCP server
CMD ["python", "main.py"]