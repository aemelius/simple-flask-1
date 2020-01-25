FROM aemel/simple-flask-1-base:2

COPY app app
COPY main.py boot.sh ./

# run-time configuration
EXPOSE 5000
ENTRYPOINT ["./boot.sh"]
