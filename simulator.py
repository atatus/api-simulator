import argparse
import grequests
import json
import os
import re
from faker import Faker
import time
from urllib.parse import urlparse, urlunparse

# Initialize the Faker generator
fake = Faker()

# Function to validate the file argument
def validate_file(arg):
    if not os.path.exists(arg):
        raise argparse.ArgumentTypeError(f"The file {arg} does not exist!")
    try:
        with open(arg, 'r') as f:
            json.load(f)
    except json.JSONDecodeError:
        raise argparse.ArgumentTypeError(f"The file {arg} is not in the correct JSON format!")
    return arg

# Function to generate fake data based on existing values
def generate_fake_data(request):
    fake_body = {}
    fake_params = {}

    # Generate fake data for body
    if 'body' in request and request['body']:
        for key, value in request['body'].items():
            if isinstance(value, str):
                fake_body[key] = fake.name() if 'name' in key else fake.address()
            elif isinstance(value, int):
                fake_body[key] = fake.random_int(min=1, max=100)
            elif isinstance(value, float):
                fake_body[key] = fake.random_number(digits=2, fix_len=True)
            # Add more conditions here if needed for other value types

    # Generate fake data for query parameters
    if 'params' in request and request['params']:
        for key, value in request['params'].items():
            if isinstance(value, str):
                fake_params[key] = fake.name() if 'name' in key else fake.address()
            elif isinstance(value, int):
                fake_params[key] = fake.random_int(min=1, max=100)
            elif isinstance(value, float):
                fake_params[key] = fake.random_number(digits=2, fix_len=True)
            # Add more conditions here if needed for other value types

    return fake_body, fake_params

# Function to replace placeholders in the URL path with fake data
def replace_placeholders_in_url(url):
    parsed_url = urlparse(url)
    path = parsed_url.path
    # Replace placeholders like :userId, :orderId, and :id with fake data
    # Use a regular expression to ensure that only placeholders in the path are replaced
    path = re.sub(r':(\w+)', lambda match: str(fake.random_int(min=1, max=100)), path)
    # Reconstruct the URL with the modified path
    return urlunparse(parsed_url._replace(path=path))

# Function to send requests and handle responses based on Content-Type
def send_requests(urls, requests_per_minute, duration_minutes, global_domain, concurrency):
    start_time = time.time()
    end_time = start_time + duration_minutes * 60
    requests_interval = 60 / requests_per_minute

    while time.time() < end_time:
        # Prepare requests
        reqs = []
        for request in urls:
            method = request['method'].upper()
            url = request['url']

            if not method or not url:
                print(f"Skipping request: method or URL is missing.")
                continue

            # Check if URL starts with https or if global domain is specified
            if not url.startswith('https://') and not global_domain:
                print("Error: URL does not contain https and no global domain is specified.")
                continue

            # Prepend global domain if URL does not include a domain
            if not url.startswith('http'):
                url = f"{global_domain}{url}"
            url = replace_placeholders_in_url(url)
            headers = request.get('headers', {})
            body = request.get('body', '')
            params = request.get('params', {})

            # Generate fake data for this request
            fake_body, fake_params = generate_fake_data(request)

            # Use the generated fake data if available, otherwise use the original data
            body = json.dumps(fake_body) if fake_body else json.dumps(body)
            params = fake_params if fake_params else params

            # Determine the Content-Type based on the body type
            if body:
                try:
                    json.loads(body)
                    headers['Content-Type'] = 'application/json'
                except json.JSONDecodeError:
                    headers['Content-Type'] = 'text/plain'

            if method == 'POST':
                req = grequests.post(url, headers=headers, data=body, params=params)
            elif method == 'GET':
                req = grequests.get(url, headers=headers, params=params)
            elif method == 'PUT':
                req = grequests.put(url, headers=headers, data=body, params=params)
            elif method == 'DELETE':
                req = grequests.delete(url, headers=headers, data=body, params=params)
            elif method == 'OPTIONS':
                req = grequests.options(url, headers=headers, params=params)
            elif method == 'HEAD':
                req = grequests.head(url, headers=headers, params=params)
            else:
                print(f"Unsupported method: {method}")
                continue

            reqs.append(req)

        # Send requests concurrently
        responses = grequests.map(reqs, size=concurrency)

        # Handle responses
        for response in responses:
            if response is not None:
                # Handle response based on Content-Type
                content_type = ''
                if 'headers' in response:
                    headers = response['headers']
                    if headers is not None:
                        content_type = headers.get('Content-Type', '')

                if 'application/json' in content_type:
                    data = response.json()
                elif 'text/html' in content_type:
                    data = response.text
                else:
                    data = response.content

                print(f"Response for {response.url}: {response.status_code}")
                # print(data)
            # else:
            #     # print(f"Empty Response!")

        # Sleep to maintain the specified rate of requests
        time.sleep(requests_interval)

# Argument parsing
parser = argparse.ArgumentParser(description='Send requests with fake data.')
parser.add_argument('--file', type=validate_file, help='File containing URLs in JSON format.')
parser.add_argument('--requests_per_minute', type=int, default=60, help='Number of requests per minute.')
parser.add_argument('--duration_minutes', type=int, default=2, help='Duration in minutes.')
parser.add_argument('--global_domain', type=str, default='', help='Global domain to prepend to URLs without a domain.')
parser.add_argument('--concurrency', type=int, default=1, help='Number of concurrent requests.')
args = parser.parse_args()

# Load URLs from the file
with open(args.file, 'r') as f:
    urls = json.load(f)

# Call the function with your list of URLs, number of requests per minute, duration in minutes, global domain, and concurrency
send_requests(urls, args.requests_per_minute, args.duration_minutes, args.global_domain, args.concurrency)
