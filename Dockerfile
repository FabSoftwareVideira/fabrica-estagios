FROM python:3.9-slim AS base

WORKDIR /app

ARG APP_VERSION=0.1.0
ARG APP_ENV=development

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV APP_VERSION=${APP_VERSION}
ENV APP_ENV=${APP_ENV}

LABEL org.opencontainers.image.title="fabrica-estagios"
LABEL org.opencontainers.image.version="${APP_VERSION}"
LABEL net.brdrive.fsw-ifc-estagios.environment="${APP_ENV}"

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

FROM base AS dev

COPY . .

CMD ["flask", "run", "--host=0.0.0.0", "--port=5000", "--debug"]

FROM base AS prod

COPY . .

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app", "--workers", "3", "--threads", "2", "--timeout", "120"]



# # Use an official Python runtime as a parent image
# FROM python:3.9-slim

# # Set the working directory to /app
# WORKDIR /app

# # Copy the requirements file to the container
# COPY requirements.txt .

# # Install dependencies globally in the container environment
# RUN pip install --no-cache-dir -r requirements.txt

# # Copy the rest of the application code to the container
# COPY . .

# # Expose the port the app runs on
# EXPOSE 5000

# # Define the default command (this will be overridden by docker-compose)
# CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app", "--workers", "3", "--threads", "2", "--timeout", "120"]
