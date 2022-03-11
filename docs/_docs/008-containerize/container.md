
[Dockerizing Django with Postgres, Gunicorn, and Nginx](https://testdriven.io/blog/dockerizing-django-with-postgres-gunicorn-and-nginx/)


## create docker config


## create docker pull secret in kubernetes

```shell
kubectl create secret generic demo-cred \
--from-file=.dockerconfigjson=$HOME/.docker/config.json \
--type=kubernetes.io/dockerconfigjson

kubectl create secret docker-registry docker-cred --docker-server=https://index.docker.io/v1/ --docker-username=ginigangadharan --docker-password=<your-pword> --docker-email=net.gini@gmail.com
```

### See credential

```shell
$ kubectl get secret docker-cred -o yaml

## see the values
$ kubectl get secret docker-cred --output="jsonpath={.data.\.dockerconfigjson}" | base64 --decode
```