# lemmy-image-purge

A simple utility that aims to purge the content of a community from a lemmy instnace, specifically covering purging data from pictrs and the lemmy database.

## Usage

### Run via Docker

Subtitute the values below with ones for your own instance

```shell
docker run -it --rm \
    --network="lemmy" \
    -e DATABASE_URL="postgresql://postgres@localhost:5432/lemmy" \
    -e PICTRS_URL="http://pictrs/" \
    -e PICTRS_API_KEY="aaaabbbbccccc1111222333" \
    ghcr.io/devops-pizza/lemmy-image-purge:latest \
    purge --community "https://lemmy.world/c/lemmyshitpost" --domain "devops.pizza" --days 7
```

### Run via pipx

```shell
pipx install lemmy-image-purge
export DATABASE_URL="postgresql://postgres@localhost:5432/lemmy"
export PICTRS_URL="http://pictrs/"
export PICTRS_API_KEY="aaaabbbbccccc1111222333"
lemmy-image-purge purge --community "https://lemmy.world/c/lemmyshitpost" --domain "devops.pizza" --days 7
```

### Run via Kubernetes

```shell
cat <EOF > job.yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: lemmy-image-purge
  namespace: lemmy
spec:
  template:
    spec:
      containers:
      - name: app
        image: ghcr.io/devops-pizza/lemmy-image-purge:latest
        env:
        - name: DATABASE_URL
          value: postgresql://postgres@localhost:5432/lemmy
        - name: PICTRS_URL
          value: http://pictrs/
        - name: PICTRS_API_KEY
          value: aaaabbbbccccc1111222333
        args: ["purge", "--community", "https://lemmy.world/c/lemmyshitpost", "--domain", "devops.pizza", "--days", "7"]
      restartPolicy: Never
  backoffLimit: 0
EOF
```
