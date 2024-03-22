# API Simulator

Simulate API requests based on sample api data.

### 1. Basic Usage

This sample JSON file `payload-sample.json` demonstrates how to structure requests for different HTTP methods, including GET and POST, with placeholders in the URL path that will be replaced with fake data by the script. The `headers` and `body` fields are optional and can be used to customize the request headers and body content.

* Create a Virtual Environment and Install python dependencies

```bash
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
```

* Run simulator with sample payloads.

```bash
python3 simulator.py --file payload-sample.json --global_domain https://api.example.com
```

**Arguments**

This script accepts several command-line arguments to customize its behavior. Here's a breakdown of each argument:

- `--file`: Specifies the file containing URLs in JSON format. This file should list the URLs to which requests will be sent. The default value is not set, meaning this argument is required.

- `--global_domain`: Defines the global domain to prepend to URLs that do not include a domain. This is useful for specifying a base URL for relative paths. The default value is not set. This argument is required if JSON file does not have full domain in the url field.

- `--requests_per_minute`: Sets the number of requests per minute. This controls the rate at which requests are sent. The default value is 60.

- `--duration_minutes`: Specifies the duration in minutes for which the script will send requests. The default value is 2 minutes.

- `--concurrency`: Determines the number of concurrent requests to be made. This can help in managing the load on the server and improving the efficiency of the script. The default value is 1.


### 1. Changing the Requests Per Minute

To change the number of requests per minute, use the `--requests_per_minute` argument.

```bash
python3 simulator.py --file payload-sample.json --requests_per_minute 20 --global_domain https://api.example.com
```

### 2. Changing the Duration in Minutes

To change the duration for which the script will send requests, use the `--duration_minutes` argument.

```bash
python3 simulator.py --file payload-sample.json --duration_minutes 10 --global_domain https://api.example.com
```

### 3. Specifying a Global Domain

To specify a global domain that will be prepended to URLs without a domain, use the `--global_domain` argument.

```bash
python3 simulator.py --file payload-sample.json --global_domain https://api.example.com
```

### 4. Changing the Concurrency Level

To change the number of concurrent requests, use the `--concurrency` argument.

```bash
python3 simulator.py --file payload-sample.json --concurrency 20 --global_domain https://api.example.com
```

### 5. Combining Multiple Arguments

You can combine multiple arguments to customize the script's behavior according to your needs.

```bash
python3 simulator.py --file payload-sample.json --requests_per_minute 30 --duration_minutes 10 --global_domain https://api.example.com --concurrency 20
```

