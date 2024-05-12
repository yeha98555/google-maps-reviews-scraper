# Google Maps Scraper

## Usage

### Use in local

1. Install Dependencies:
```sh
make install
```

2. Set Environment Variables:
```sh
export GOOGLE_APPLICATION_CREDENTIALS="path/to/crawler_gcp_keyfile.json"
export GCS_BUCKET_NAME="your-bucket-name"
export GCS_BLOB_NAME="your-blob-name"
```

3. Get the results by running:
```sh
make run
```
Remember to add your params in params.yaml file.

4. Clean repo:
```sh
make clean
```

5. Clean repo and results:
```sh
make clean_all
```

### Use in Docker Container

1. Build Docker Image
```sh
docker build -t gmaps-scraper .
```

2. Run Docker Container
```sh
docker run -it --rm \
  -v $(pwd)/crawler_gcp_keyfile.json:/app/crawler_gcp_keyfile.json \
  -e GCS_BUCKET_NAME="your-bucket-name" \
  -e GCS_BLOB_NAME="your-blob-name" \
  gmaps-scraper
```

### Use in Airflow

1. Set Docker Proxy in Airflow docker-compose

2. Add DockerOperator to your DAG
```py
run_scraper = DockerOperator(
    task_id="e_gmaps-scraper",
    image="gmaps-scraper",
    api_version="auto",
    auto_remove=True,
    environment={
        "GCS_BUCKET_NAME": "your-bucket-name",
        "GCS_BLOB_NAME": "your-blob-name",
    },
    command="make run",
    mounts=[
        Mount(
            source="<your-gcp-keyfile>",  # local path
            target="/app/crawler_gcp_keyfile.json",
            type="bind",
            read_only=True,
        ),
    ],
    mount_tmp_dir=False,
    docker_url="tcp://docker-proxy:2375",
    network_mode="bridge",
)
```
