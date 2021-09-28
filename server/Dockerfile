FROM python:3
WORKDIR .
COPY . .
CMD ["server-main.py $(hostname -i) 4444"]
ENTRYPOINT ["python3"]
LABEL name="a1"

EXPOSE 4444
EXPOSE 5000