FROM python:3

ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

#CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
CMD [ "sh", "-c", "if [ -n \"$PORT\" ]; then python manage.py runserver 0.0.0.0:$PORT; else python manage.py runserver 0.0.0.0:8000; fi" ]
