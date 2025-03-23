FROM python:3.10.6-buster

COPY requirements.txt requirements.txt
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
#RUN pip install -e .

COPY setup.py setup.py

COPY olympics_folder olympics_folder

CMD uvicorn olympics_folder.api_calls:app --host 0.0.0.0 --port $PORT
