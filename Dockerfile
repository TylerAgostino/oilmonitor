FROM joyzoursky/python-chromedriver
COPY ./oil_monitor.py .
COPY entrypoint.sh .
RUN pip install -r requirements.txt
ENTRYPOINT [ "./entrypoint.sh" ] 