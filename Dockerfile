FROM python:3.12-alpine

WORKDIR /app

RUN apk update && apk upgrade && \
    apk add --no-cache ffmpeg libpq-dev gcc musl-dev bash

COPY requirements.txt . 
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN python manage.py collectstatic --noinput

# Setup script to wait postgres to be fully available
COPY ./scripts/wait-for-it.sh /usr/local/bin/wait-for-it.sh
RUN chmod +x /usr/local/bin/wait-for-it.sh

COPY ./scripts/entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh

# # Set the entrypoint
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]

# Command to run Django using the development server (but Nginx is handling requests)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
