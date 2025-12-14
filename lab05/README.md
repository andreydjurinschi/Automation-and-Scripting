# IWNO05: Ansible Playbook for Server Configuration

## ШАГ 1 — Подготовка структуры проекта и запуск тестов

```bash
Mode                 LastWriteTime         Length Name
----                 -------------         ------ ----
d-----        11/26/2025  11:53 AM                php-app
-a----        11/26/2025  11:32 AM            255 phpunit.xml
-a----        11/26/2025  12:00 PM            158 README.md
```

```bash
Каталог: C:\Users\djuri\Automation-and-Scripting\lab05\php-app
Mode                 LastWriteTime         Length Name
----                 -------------         ------ ----
d-----        11/26/2025  11:31 AM                src
d-----        11/26/2025  11:31 AM                tests
d-----        11/26/2025  11:58 AM                vendor
-a----        11/26/2025  11:32 AM            263 composer.json
-a----        11/26/2025  11:53 AM          65666 composer.lock
```

## ШАГ 2 - подготовка Docker файлов

`ssh-agent:`

```docker
FROM php:8.1-cli
# устанавливаем необходимые пакеты
RUN apt-get update && apt-get install -y \
    git \
    openssh-client \
    unzip \
    && rm -rf /var/lib/apt/lists/*
# создаём папку для проекта
WORKDIR /php-app
```

`ansible-agent`

```docker
FROM ubuntu:22.04

# устанавливаем Ansible и SSH
RUN apt-get update && apt-get install -y \
    software-properties-common \
    ssh \
    python3 \
    python3-pip \
    git \
    && apt-add-repository --yes --update ppa:ansible/ansible \
    && apt-get install -y ansible \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /ansible
```

`test-server`

```docker
FROM ubuntu:22.04

# устанавливаем SSH и Apache + PHP
RUN apt-get update && apt-get install -y \
    openssh-server \
    apache2 \
    php \
    php-cli \
    php-mbstring \
    php-xml \
    unzip \
    && mkdir /var/run/sshd \
    && rm -rf /var/lib/apt/lists/*

# создаём ansible пользователя
RUN useradd -m -s /bin/bash ansible
RUN mkdir -p /home/ansible/.ssh && chown ansible:ansible /home/ansible/.ssh

EXPOSE 22 80

CMD ["/usr/sbin/sshd", "-D"]

```


## ШАГ 3 - НАСТРОЙКА compose файла

```yaml
services:

  jenkins-controller:
    image: jenkins/jenkins:lts
    container_name: jenkins-controller
    ports:
      - "8080:8080"
      - "50000:50000"
    volumes:
      - jenkins_home:/var/jenkins_home
    networks:
      - ci-network

  ssh-agent:
    build:
      context: .
      dockerfile: Dockerfile.ssh_agent
    container_name: ssh-agent
    networks:
      - ci-network
    volumes:
      - ./php-app:/php-app

  ansible-agent:
    build:
      context: .
      dockerfile: Dockerfile.ansible_agent
    container_name: ansible-agent
    networks:
      - ci-network
    volumes:
      - ./ansible:/ansible

  test-server:
    build:
      context: .
      dockerfile: Dockerfile.test_server
    container_name: test-server
    networks:
      - ci-network
    ports:
      - "2222:22"

networks:
  ci-network:

volumes:
  jenkins_home:
```

выше представлины 4 сервиса. Jenkins сервис `jenkins-controller` с указанием постоянного хранилища конфигурации и данных самого Jenkins. `ssh-agent` - сборка из локального `Dockerfile`, который монтирует локальную папку проекта, запускает сборку и тесты, которые требуют ssh-агента. `ansible-agent` - 
Сборка из Dockerfile.ansible_agent. Монтирует локальную папку ./ansible в контейнер (/ansible). Используется для запуска Ansible playbook'ов/инфраструктурных задач из CI.
`test-server` - необходим для удаленного доступа / тестирования

## ШАГ 5 - настройка структуры Ansible

`hosts.ini`

```txt
[test-server]
test-server ansible_host=test-server ansible_user=ansible ansible_ssh_private_key_file=./id_rsa
```

`[test-server]` - имя группы хостов в инвентаре Ansible

`test-server` — алиас/имя хоста.

`ansible_host=test-server` — адрес для подключения.

`ansible_user=ansible` — пользователь SSH, от имени которого происходит подключение.

`ansible_ssh_private_key_file=./id_rsa` — путь к приватному SSH-ключу

### playbook 

```yaml
- hosts: test-server
  become: yes
  tasks:
    - name: install apache
      apt: name=apache2 state=present update_cache=yes

    - name: install php
      apt: name=php state=present

    - name: enable vhost
      copy:
        src: vhost.conf
        dest: /etc/apache2/sites-available/000-default.conf
```

