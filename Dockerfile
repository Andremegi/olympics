FROM  python:3.10-slim

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY olympics_folder olympics_folder

CMD uvicorn olympics_folder.api_calls:app -- host 0.0.0.0
