# Docker Deployment

## Custom Container Hub
Default hub points to docker.io, if you need to modify this, add to the build command the argument REGISTRY
like this ```docker build --build-arg REGISTRY=my-private-hub.com .```


## Build Docker Image with external pip index as Build Image
Note: This image acts as a build image only!
```bash
# Create a secret file containing your pip index URL, e.g. your own index
echo "https://pypi.org/simple/" > pip_index_url.txt

# Build the Docker image using BuildKit and mount the secret
DOCKER_BUILDKIT=1 docker build \
  --secret id=pip_index_url,src=pip_index_url.txt \
  --build-arg REGISTRY=docker.io \
  -t build_{{cookiecutter.project_build_id | replace('"','')}} -f deployment/Container.build .
```
## Build Docker Image based on Build Image 
This Container deployment/Container.run should be copied to deployment/Container in order to avoid future overwrites
```bash
# Make the Run Container your own
cp  deployment/Container.run  deployment/Container

# Build the Docker image using BuildKit and mount the secret
DOCKER_BUILDKIT=1 docker build \
  --build-arg REGISTRY=docker.io \
  -t {{cookiecutter.package_name}} -f deployment/Container .
```
## Run AI Environment
* Publish Port 9000 to local port 9000
* Automatically remove the container and its associated anonymous volumes when it exits
 
```bash
docker run --publish 9000:9000 --env-file .env --rm {{ cookiecutter.package_name}}
```
## Troubleshooting
### Ensure .env file format
.env files that will be provided to docker have to ommit quotes. Otherwise the quotes will be part of the assignment.


### Inspect the Image
```bash
docker run -it {{ cookiecutter.package_name}} sh
```

