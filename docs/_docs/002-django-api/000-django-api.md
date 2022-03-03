
https://github.com/codingforentrepreneurs/Django-Rest-Framework-Tutorial


## Object-Relational Mapper (ORM)

[An introduction to the Django ORM](https://opensource.com/article/17/11/django-orm)
[Build a REST API in 30 minutes with Django REST Framework](https://medium.com/swlh/build-your-first-rest-api-with-django-rest-framework-e394e39a482c)

- [Rest API Guide](https://www.bezkoder.com/django-rest-api/#1_Technology)

## Serialization

Serialization is the process of converting a Model to JSON. Using a serializer, we can specify what fields should be present in the JSON representation of the model.

## Sample curl request

```shell
root@Ubuntu-20-CP:~# curl -X POST http://192.168.56.1:8000/app/api/nodes/managednodes/ -H "Content-Type: application/json" -d '{"instance_name": "node66","instance_name_connection": "node66.lab.local","instance_credential": "test55"}'
```

## Appendix