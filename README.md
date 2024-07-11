# Arabic-Sentiment-Analysis

## Overview

This repository contains solutions for two challenges:

- **Challenge 1**: Python code for a sentiment analysis approach and a report explaining the approach.
- **Challenge 2**: Code for Dockerizing and serving the sentiment analysis model as an API, along with a report explaining the test cases.

## File Organization

## Challenge 1: Sentiment Analysis Approach

The `challenge1` folder contains the following files:
- `Challenge 1 Code.ipynb`: Python code implementing the sentiment analysis approach.
- `Challenge 1 Report.pdf`: A report explaining the sentiment analysis approach used.

## Challenge 2: Dockerize and Serve the Sentiment Analysis Model

The `challenge2` folder contains the following files:
- `app.py`: Flask API code for model inference.
- `Dockerfile`: Docker configuration file.
- `requirements.txt`: List of Python dependencies.
- `templates`: contain the index.html file.
- `Challenge 2 Report.pdf`: A report explaining the test cases for the API.

### Download the Model

Before running the Docker container, you need to download the model files from the following link and place them in the `challenge2/Model` directory:

[Download Model](https://drive.google.com/drive/folders/1a-j7f03NToYpLXPyUaDD3yE4OCMynR97?usp=sharing)


## Steps to Run the API and Docker Image

### Prerequisites

- Docker installed on your system
- Postman installed

### Running the Docker Container

1. **Clone the repository:**

```sh
git clone <repository-url>
```
2. **Download the model and place it in the challenge2/Model directory:**

3. **Build the Docker image:**
```sh
cd <repository-directory>/challenge2
docker build -t sentiment-analysis-api .
```
3. **Run the Docker container:**
```sh
docker run -p 5000:5000 sentiment-analysis-api
```
4. **Testing:**
a. ***Testing using Interface***: run the given local link example:
```sh
http://127.0.0.1:5000
```
b. ***Testing using Postman***: To test the API, you can use Postman or any other API testing tool. Follow these steps:

1. **Open Postman and create a new request.**

2. **Set the request type to POST and enter the URL**:
```sh
http://localhost:5000/predict
```
3. **Set the headers**:
```sh
Key: Content-Type
Value: application/json
```
4. **Set the body to raw and select JSON format**:
```sh
{
  "text": "الف مبروك، ويستاهلون وعقبالي بإذن الله 😭🤲🤍🌙"
}
```
5. **Send the request and check the response**:
The response will contain the original text and the predicted sentiment label.
```sh
{
  "text": "الف مبروك، ويستاهلون وعقبالي بإذن الله 😭🤲🤍🌙",
  "predicted_label": "positive"
}
```
