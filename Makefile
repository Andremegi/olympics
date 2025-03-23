docker_build_local:
				@docker build --tag=$IMAGE:dev .
docker_run_local:
				@docker run -it -e PORT=8000 -p 8000:8000 $IMAGE:dev
docker_build_container_deployment:
				@docker build \
  --platform linux/amd64 \
  -t $GCP_REGION-docker.pkg.dev/$GCP_PROJECT/$ARTIFACTSREPO/$IMAGE:prod \
  .

docker_auth_gcp:
				@gcloud auth configure-docker $GCP_REGION-docker.pkg.dev
