FROM python:3.9-slim

# Install dependencies
RUN pip install requests paho-mqtt

# Copy add-on files
COPY tuya_api.py /app/tuya_api.py
COPY run.sh /app/run.sh

# Set working directory
WORKDIR /app

# Make run.sh executable
RUN chmod +x run.sh

# Expose port for REST API
EXPOSE 8000

# Run the script
CMD ["./run.sh"]