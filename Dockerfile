FROM python:3.10.6-buster

# Set working directory to /app
WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
#RUN pip install -e .

COPY setup.py setup.py

COPY olympics_folder olympics_folder

# Add /app to PYTHONPATH for imports to work
ENV PYTHONPATH="${PYTHONPATH}:/app"

# Expose the port for FastAPI
EXPOSE 8000

CMD ["uvicorn", "olympics_folder.api_calls:app", "--host", "0.0.0.0", "--port", "$PORT"]
#CMD uvicorn olympics_folder.api_calls:app --host 0.0.0.0 --port $PORT
