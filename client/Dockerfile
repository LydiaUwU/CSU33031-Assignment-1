FROM python:3
WORKDIR .
COPY . .
RUN pip install --no-cache-dir inputimeout
CMD ["-i", "client-main.py"]
ENTRYPOINT ["python3"]
LABEL name="a1"

EXPOSE 4444