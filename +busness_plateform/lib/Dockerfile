From python:3.2.14-slim
WOKDIR/app
COPY ..
RUN pip install
--no-cache-dir -r 
requirements.txt
EXPOSE 8000

CMD ["python","web_app.py"]