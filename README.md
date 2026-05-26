# CRM Multi-tenant SaaS API
 
Асинхронный CRM сервис с поддержкой мультиарендности. Каждая организация работает изолированно — пользователи видят только данные своей организации.
 
## Стек технологий
 
- FastAPI — асинхронный веб-фреймворк
- PostgreSQL — основная база данных
- SQLAlchemy — ORM для работы с БД
- Alembic — миграции базы данных
- Redis — кеширование данных
- JWT — авторизация через токены
- Nginx — reverse proxy
- Docker / Docker Compose — контейнеризация
- Pydantic — валидация данных
- pytest — тестирование с тестовой БД
## Функциональность
 
- Создание организаций (тенантов)
- Регистрация и авторизация пользователей через JWT
- Управление контактами (клиентами) организации
- Управление сделками привязанными к контактам
- Полная изоляция данных между организациями
- Кеширование через Redis с автоматической инвалидацией
- Пагинация для всех списковых эндпоинтов
## Структура проекта
 
```
crm/
├── app/
│   ├── main.py
│   ├── config.py
│   ├── database.py
│   ├── redis_client.py
│   ├── models/
│   │   ├── base.py
│   │   ├── organization.py
│   │   ├── user.py
│   │   ├── contact.py
│   │   └── deal.py
│   ├── repositories/
│   │   ├── organization.py
│   │   ├── user.py
│   │   ├── contact.py
│   │   └── deal.py
│   ├── services/
│   │   └── auth.py
│   ├── routers/
│   │   ├── auth.py
│   │   ├── organization.py
│   │   ├── contact.py
│   │   └── deal.py
│   └── schemas/
│       ├── auth.py
│       ├── organization.py
│       ├── contact.py
│       └── deal.py
├── migrations/
├── nginx/
│   └── nginx.conf
├── tests/
│   ├── conftest.py
│   ├── test_auth.py
│   ├── test_organization.py
│   ├── test_contact.py
│   └── test_deal.py
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── .env
```
 
## Архитектура
 
```
Интернет -> Nginx:80 -> FastAPI:8000 -> PostgreSQL
                                     -> Redis
```
 
## Multi-tenant изоляция
 
Каждый запрос проверяет что пользователь работает только с данными своей организации:
 
```python
if user.organization_id != contact.organization_id:
    raise HTTPException(status_code=403, detail="Not allowed")
```
 
Пользователь не может получить доступ к контактам или сделкам другой организации даже зная их ID.
 
## Запуск проекта
 
### 1. Клонировать репозиторий
 
```bash
git clone https://github.com/eternal-silence00/CRM.git
cd CRM
```
 
### 2. Создать `.env` файл
 
```properties
DATABASE_URL=postgresql+asyncpg://postgres:password@db:5432/multi_tenant_SaaS
REDIS_URL=redis://redis:6379
BASE_URL=http://localhost:8000
POSTGRES_USER=postgres
POSTGRES_PASSWORD=password
POSTGRES_DB=multi_tenant_SaaS
SECRET_KEY=your_secret_key
ALGORITHM=HS256
```
 
### 3. Запустить через Docker
 
```bash
docker-compose up --build
```
 
### 4. Применить миграции
 
```bash
docker-compose exec app alembic upgrade head
```
 
### 5. Открыть документацию
 
```
http://localhost/docs
```
 
## API Endpoints
 
### Авторизация
 
| Метод | Путь | Описание |
|-------|------|----------|
| POST | /organization | Создать организацию |
| POST | /auth/register | Регистрация пользователя |
| POST | /auth/login | Вход и получение JWT |
| GET | /organization/{id}/workers | Сотрудники организации |
 
### Контакты (требуют JWT)
 
| Метод | Путь | Описание |
|-------|------|----------|
| POST | /contact | Создать контакт |
| GET | /contact/organization/{id} | Все контакты организации |
| GET | /contact/{id} | Получить контакт по ID |
 
### Сделки (требуют JWT)
 
| Метод | Путь | Описание |
|-------|------|----------|
| POST | /deal | Создать сделку |
| GET | /deal/organization/{id} | Все сделки организации |
| GET | /deal/{id} | Получить сделку по ID |
| PATCH | /deal/{id} | Обновить сделку |
| DELETE | /deal/{id} | Удалить сделку |
 
## Запуск тестов
 
```bash
docker-compose exec app pytest tests/ -v
```
 
Тесты используют отдельную БД `multi_tenant_saas_test` и не затрагивают основные данные.
 
## Архитектурные решения
 
**Multi-tenant через общие таблицы** — все организации хранятся в одной БД. Изоляция обеспечивается через `organization_id` в каждой таблице и проверку прав в каждом эндпоинте.
 
**Cache-Aside паттерн** — контакты и сделки кешируются в Redis. Кеш инвалидируется при создании, изменении и удалении записей.
 
**Repository паттерн** — слой репозитория отделяет бизнес-логику от работы с БД.
 
**Nginx reverse proxy** — принимает все входящие запросы на порту 80 и перенаправляет на FastAPI.