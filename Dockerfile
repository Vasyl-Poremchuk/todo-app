# Define the base image
FROM python:3.10.5-slim-bullseye

# Set the value of the environment values
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory in the container
WORKDIR /app

# Copy the requirements & Install the dependencies
COPY ./requirements.txt /app
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Copy the `todo` app code into the container
COPY . /app

# Expose the port on which the `todo` app will run
EXPOSE 8000

# Set the entrypoint command to start the `todo`
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
