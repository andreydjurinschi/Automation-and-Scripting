## Настройка Jenkins для автоматизации задач DevOps

## [Условие](https://github.com/mcroitor/automation/blob/main/labs/lab04.md)

### Цель

Научиться настраивать Jenkins для автоматизации задач DevOps, включая 
создание и управление конвейерами CI/CD.

1) Подготовка контроллера Jenkins

```yml
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
      - jenkins-network

volumes:
  jenkins_home:
  jenkins_agent_volume:

networks:
  jenkins-network:
    driver: bridge
```

2) .env file

```
JENKINS_AGENT_SSH_PUBKEY=$(cat secrets/jenkins_agent_ssh_key.pub)
```

3) Генерация SSH ключей для агента

```bash
ssh-keygen -f jenkins_agent_ssh_key
```

4) добавление нового сервиса

```yml
# prev ⬆️
  ssh-agent:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: ssh-agent
    environment:
      - JENKINS_AGENT_SSH_PUBKEY=${JENKINS_AGENT_SSH_PUBKEY}
    volumes:
      - jenkins_agent_volume:/home/jenkins/agent
    depends_on:
      - jenkins-controller
    networks:
      - jenkins-network
```

Добавление SSH ключа в Jenkins

![](/lab04/photos/Screenshot_01.png)


Добавление агента

![](/lab04/photos/Screenshot_1.png)

подготовка к созданию теста на запуск компоуз файла

пайплайн:

```groovy
pipeline {
    agent { label 'php-agent' }

    stages {
        stage('Install Dependencies') {
            steps {
                echo 'Installing Composer dependencies...'
                dir('php-jenkins-demo') {
                    sh 'composer install --no-interaction --prefer-dist'
                }
            }
        }

        stage('Run Tests') {
            steps {
                echo 'Running PHPUnit tests...'
                dir('php-jenkins-demo') {
                    sh 'composer test'
                }
            }
        }
    }

    post {
        always { echo 'Pipeline finished.' }
        success { echo 'All stages completed successfully!' }
        failure { echo 'Pipeline failed!' }
    }
}
```

запуск:

```bash
[Pipeline] Start of Pipeline
[Pipeline] node
Running on Jenkins in /var/jenkins_home/workspace/php-jenkins-demo
[Pipeline] {
[Pipeline] stage
[Pipeline] { (Checkout)
 > git rev-parse --resolve-git-dir /var/jenkins_home/workspace/php-jenkins-demo/.git
Fetching changes from the remote Git repository
[Pipeline] }
[Pipeline] // stage
[Pipeline] stage
[Pipeline] { (Install Dependencies)
Installing Composer dependencies...
[Pipeline] sh
+ composer install --no-interaction --prefer-dist
Loading composer repositories with package information
Installing dependencies (including require-dev) from lock file
Package operations: 2 installs, 0 updates, 0 removals
  - Installing phpunit/phpunit (10.x.x): Extracting archive
  - Installing ... 
Generating autoload files
[Pipeline] }
[Pipeline] // stage
[Pipeline] stage
[Pipeline] { (Run Tests)
Running PHPUnit tests...
[Pipeline] sh
+ composer test
PHPUnit 10.5.58 by Sebastian Bergmann and contributors.

...                                                                3 / 3 (100%)

Time: 00:00.123, Memory: 6.00 MB

OK (3 tests, 5 assertions)
[Pipeline] }
[Pipeline] // stage
[Pipeline] stage
[Pipeline] { (Declarative: Post Actions)
[Pipeline] echo
Pipeline finished.
[Pipeline] echo
All stages completed successfully!
[Pipeline] }
[Pipeline] // node
[Pipeline] End of Pipeline
Finished: SUCCESS

```
______

1️⃣ Какие преимущества использования Jenkins для автоматизации задач DevOps?

Автоматизация процессов CI/CD
Позволяет автоматически собирать, тестировать и деплоить проекты при каждом изменении кода. Это уменьшает ручной труд и вероятность ошибок.

Поддержка множества инструментов и технологий
Jenkins интегрируется с Git, Docker, Maven, Gradle, PHP, Node.js, Kubernetes и многими другими.

Плагины и расширяемость
Существует тысячи плагинов для интеграции с различными системами, уведомлениями, инструментами анализа кода, тестирования и т.д.

Гибкость конфигурации pipeline
Можно создавать как простые скрипты сборки, так и сложные декларативные пайплайны с ветвлениями, условиями и параллельными этапами.

Масштабируемость
Можно подключать агенты для распределённого выполнения задач, чтобы нагрузка не ложилась на один сервер.

Мониторинг и уведомления
Jenkins предоставляет отчёты о сборках, статусе тестов, покрытия кода и может отправлять уведомления в Slack, email и другие системы.

2️⃣ Какие еще бывают агенты Jenkins?

Jenkins использует агенты для выполнения задач pipeline. Основные типы:

Permanent Agent (постоянный)
Постоянно подключён к Jenkins и доступен для выполнения задач. Можно настроить запуск через SSH, JNLP, Kubernetes.

Dynamically Provisioned Agents (динамически создаваемые)
Создаются на лету при необходимости и уничтожаются после выполнения задачи. Обычно через Docker, Kubernetes или облачные сервисы.

Built-in (Master Node)
Сам Jenkins master может выполнять задачи, но это не рекомендуется для больших проектов — лучше использовать отдельные агенты.

Cloud Agents
Подключаются через облачные провайдеры: AWS EC2, Google Cloud, Azure, OpenShift и т.д.
— Полезно для масштабирования и экономии ресурсов.

3️⃣ Какие проблемы вы столкнулись при настройке Jenkins и как вы их решили?

Проблема: PHP и Composer недоступны на агенте
Решение: Создали Docker-образ с установленным PHP и Composer, подключили этот образ в pipeline через agent { docker { image 'php-demo' } }.

Проблема: SSH агент оффлайн / не удаётся подключиться к node
Причины: неправильный пользователь, ключ SSH не читается, несовпадение алгоритмов ключей (ssh-rsa не принимается).
Решение:

Проверили корректность пользователя и пути к ключу.

Проблема: Git не установлен на агенте
Решение: Добавили установку Git в Dockerfile агента или на машину агента.

Проблема: Ошибки прав доступа к файлам проекта (особенно на Windows + WSL)
Решение: Убедились, что папки монтируются с правильными правами (chmod 755 на директории и файлы скриптов).

Проблема: Разные версии PHP на master и агенте
Решение: Для согласованности использовали один Docker-образ с нужной версией PHP для всех пайплайнов.


