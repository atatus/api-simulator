# API Simulator

Simulate API requests based on sample api data.

### 1. Basic Usage

To run the script with the default values for all arguments, you can simply call the script without any additional arguments.
This will use the default values specified in the script for `requests_per_minute`, `duration_minutes`, `global_domain`, and `concurrency`.

This sample JSON file `payload-sample.json` demonstrates how to structure requests for different HTTP methods, including GET and POST, with placeholders in the URL path that will be replaced with fake data by the script. The `headers` and `body` fields are optional and can be used to customize the request headers and body content.


```bash
python simulator.py --file payload-sample.json
```

### 1. Changing the Requests Per Minute

To change the number of requests per minute, use the `--requests_per_minute` argument.

```bash
python simulator.py --file payload-sample.json --requests_per_minute 30
```

### 2. Changing the Duration in Minutes

To change the duration for which the script will send requests, use the `--duration_minutes` argument.

```bash
python simulator.py --file payload-sample.json --duration_minutes 10
```

### 3. Specifying a Global Domain

To specify a global domain that will be prepended to URLs without a domain, use the `--global_domain` argument.

```bash
python simulator.py --file payload-sample.json --global_domain https://api.example.com
```

### 4. Changing the Concurrency Level

To change the number of concurrent requests, use the `--concurrency` argument.

```bash
python simulator.py --file payload-sample.json --concurrency 20
```

### 5. Combining Multiple Arguments

You can combine multiple arguments to customize the script's behavior according to your needs.

```bash
python simulator.py --file payload-sample.json --requests_per_minute 30 --duration_minutes 10 --global_domain https://api.example.com --concurrency 20
```
