# Cirs-License-Registration-Issuer
Барилгын тусгай зөвшөөрөл блокчэйнд бүртгэх

Ухаалаг гэрээг доорх холбоосоор харах боломжтой.

[https://github.com/teo-mn/Cirs-License-Registration-Sc](https://github.com/teo-mn/Cirs-License-Registration-Sc)

### Start django app

```
gunicorn --workers 1 --threads 3 --worker-connections 10 -b :1010 license_registration_issuer.wsgi
```

### Start message queue consumer

```
celery -A license_registration_issuer worker --beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler --pool=solo --concurrency=1
```
### Орчины мэдээлэл

#### Блокчэйнтэй холбоотой

| Түлхүүр үг    | Тайлбар |
| -------- | ------- |
| NODE_URL  | Блокчэйний node-ий URL    |
| NODE_URL_WS | WS ажиллаж буй node-ий URL     |
| CHAIN_ID    | блокчэйний ID /teo: 1104, teo_test: 3305 /    |
| LICENSE_REGISTRATION_ADDRESS    | Лиценз бүртгэх ухаалаг гэрээний хаяг    |
| REQUIREMENT_REGISTRATION_ADDRESS    | Заалт бүртгэх ухаалаг гэрээний хаяг    |
| KV_ADDRESS    | ИТА бүртгэх ухаалаг гэрээний хаяг    |
| ISSUER_ADDRESS    | Лиценз олгогчийн блокчэйний хаяг    |
| ISSUER_PK    | Лиценз олгогчийн блокчэйний хаягийн нууц түлхүүр    |

#### Message Queue тэй холбоотой

| Түлхүүр үг    | Тайлбар |
| -------- | ------- |
| CELERY_BROKER_URL  | Message Queue URL /жишээ (rabbit MQ): amqp://guest:guest@localhost:5672/    |
| CELERY_TASK_DEFAULT_EXCHANGE |   Message Queue Exchange   |
| CELERY_TASK_DEFAULT_ROUTING_KEY    | Message Queue Routing Key   |
| CELERY_TASK_DEFAULT_QUEUE    | Message Queue queue name   |
