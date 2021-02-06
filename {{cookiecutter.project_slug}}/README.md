### Start up for development
```
tilt up --stream
```

### Manually build docker image
```
docker build -f infra/backend.dockerfile -t local/{{cookiecutter.docker_image_service}}:0.0.1 .
```

### Install helm chart local dev
```
helm upgrade -i -f infra/chart/values-local.yaml rr infra/chart
```
