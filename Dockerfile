FROM joyzoursky/python-chromedriver
COPY ./oil_monitor.py .
COPY requirements.txt .
RUN pip install -r requirements.txt
ENTRYPOINT [ "python", "./oil_monitor.py" ]