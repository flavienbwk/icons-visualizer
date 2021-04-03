# Icons Visualizer

<p align="center">
    <a href="https://travis-ci.org/flavienbwk/icons-visualizer" target="_blank">
        <img src="https://travis-ci.org/flavienbwk/icons-visualizer.svg?branch=master"/>
    </a>
    <a href="https://opensource.org/licenses/MIT" target="_blank">
        <img src="https://img.shields.io/badge/License-MIT-yellow.svg">
    </a>
</p>

A quick and simple UI and API to search and display icons. Can be used in an offline environment thanks to Docker.

![Interface example](./interface.png)

Written in Python (Flask RESTPlus / Swagger) and ReactJS.

## Get started

First, import the icons you want in the `icons/` directory.

<center>
:information_source: **The names of your files** are very important : the search engine is based on filenames to find keywords as you type the icon you're looking for in the UI searchbar.
</center>

### Build for dev

```bash
docker-compose up -d
```

You can access the UI at `localhost:8080`

### Build for prod

```bash
docker-compose -f prod.docker-compose.yml up --build -d
```

You can access the UI at `localhost:8080`

### Deploy to K8S

I pretend you have here your K8S instance configured to be accessed by your `kubectl` CLI.

I've used [Scaleway Kapsule](https://scaleway.com/kapsule) to perform my tests. This is an easy way to have a Kubernetes cluster ready in some seconds.

1. Building production images

    By default, images are tagged `flavienb/icons-visualizer-{api,web,nginx}:latest`. Edit it in `prod.docker-compose.yml` before building.

    ```bash
    docker-compose -f prod.docker-compose.yml buid
    ```

    Finally, `docker push` the 3 images.

2. Add a new `icons-visualizer` namespace

    ```bash
    kubectl create namespace icons-visualizer
    ```

3. Considerations on persistant volume for icons

    You have 4 options to see your icons on Kubernetes :

    - Create a `PersistentVolume` with `spec.local` pointing to a path on a node and import your icons inside (requires an SSH access to this node)
    - Use a remote NFS server (not supported yet by Icons Visualizer)
    - Copy all of your icons in your Docker image
    - Use a S3 server such as MinIO and import your pictures via a web interface

    For this example, I'll go with MinIO so you have a light image to deploy.

4. Configure your Ingress app endpoint

    - **Define** the app endpoint in [k8s/nginx.yaml, line 51](./k8s/nginx.yaml#L51)
    - **Define** the MinIO endpoint in [k8s/minio.yaml, line 76](./k8s/minio.yaml#76)

    Deploy with :

    ```bash
    kubectl apply -f k8s --namespace icons-visualizer
    ```

You can now access the UI on your Kubernetes instance

Don't forget to import your icons through MinIO !
