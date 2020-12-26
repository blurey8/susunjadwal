# Susun Jadwal Backend

- [Susun Jadwal Backend](#susun-jadwal-backend)
  - [Requirements](#requirements)
  - [Configuration](#configuration)
    - [Development](#development)
    - [Development with Docker](#development-with-docker)
    - [Production](#production)
  - [API Documentation](#api-documentation)
    - [Definition](#definition)
      - [Parameter](#parameter)
      - [Permission](#permission)
    - [API Endpoint](#api-endpoint)
      - [Authorization](#authorization)
      - [Get Courses](#get-courses)
      - [Save User Schedule](#save-user-schedule)
      - [Get User Schedule Detail](#get-user-schedule-detail)
      - [Delete User Schedule](#delete-user-schedule)
      - [Rename User Schedule](#rename-user-schedule)
  - [License](#license)

## Requirements

1. `python` and `pip`
2. `docker`

## Configuration

### Development

1. Create virtual environment using `python3 -m venv env`
2. Activate virtualenv `source ./env/bin/activate`
3. Install requirements `pip install -r requirements.txt`
4. Add your credential to scrap schedule from SIAK in `scraper/credentials.json` with the following structure:

```
{
    "<kd_org>": {
        "username": "<username>",
        "password": "<password>"
    }
}
```

You can also see `scraper/credentials.template.json` for example and `sso/additional-info.json` for list of `kd_org`.

5. Start database using `bash start_db.sh`
6. Go to mongo console by running `docker exec -it ristek-mongo mongo -u <admin_username>`
7. Create database by running `use <db_name>`. By default, Flask use database named `test` so it becomes `use test`
8. Create user for database:

```
db.createUser(
    {
        user: "<db_user>",
        pwd: "<db_pwd>",
        roles:[
            {
                role: "readWrite",
                db: "<db_name>"
            }
        ]
    }
);
```

You can quit mongo console now by using Ctrl + D.

9. Create config file, `instance/config.cfg`. You can see `instance/config.template.cfg` for example and edit db name, username, and password to match the one you created before
10. Finally, run Flask by using `FLASK_ENV="development" flask run`

### Development with Docker

1. Do step #4 from [Development](#development).
2. Do step #9 from [Development](#development) but change the following settings accordingly:

   - `MONGODB_DB` : `test`
   - `MONGODB_HOST` : `db`
   - `MONGODB_USERNAME` : `mongo_user`
   - `MONGODB_PASSWORD` : `mongo_password`
3. Start the containers with `docker-compose up -d --build`
4. Go to Mongo console by running `docker-compose exec db mongo -u mongo_user`
5. Do steps #7 and #8 from [Development](#development).
6. To stop the containers, run `docker-compose down`

For subsequent uses, you can just do steps #3 and #6 above.

### Production

> We actually have a slightly different setup in the real Ristek server. For future maintainers, you may want to contact past contributors.

1. Do everything in development step **except** step no 10, running Flask. Don't forget to modify `instance/config.cfg`, `start_db.sh`, and `scraper/credentials.json` if you want to
2. Run gunicorn using `bash start.sh`
3. Set your Nginx (or other reverse proxy of your choice) to reverse proxy to `sunjad.sock`. For example, to reverse proxy `/susunjadwal/api` you can set

```
location ^~ /susunjadwal/api {
    proxy_set_header Host $http_host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
    proxy_pass http://unix:/path/to/susunjadwal/backend/sunjad.sock;
}
```

4. Run the schedule scrapper cron job using `crontab -e` and add the line to run `cron.sh`. For example, to run it every 10 minutes add `*/10 * * * * bash /path/to/susunjadwal/backend/cron.sh`

## API Documentation

### Definition

#### Parameter

This is the URL parameter needed in this API endpoint.

| Parameter          | Description                          |
| ------------------ | ------------------------------------ |
| `major_id`         | Major UUID, not major code from SIAK |
| `user_schedule_id` | User schedule UUID                   |
| `user_id`          | User UUID, not related to SSO UI     |

#### Permission

This is the permission types of this project's endpoint.

| Permission              | Description                                      |
| ----------------------- | ------------------------------------------------ |
| *null*                  | Does not require any authentication              |
| `@require_jwt_token`    | Require valid JWT token on authorization header  |
| `@require_same_user_id` | Only the resource owner can access this endpoint |

### API Endpoint

#### Authorization

Return major id, token and user id by send authentication ticket and front end URL.

- **Request**

`POST /auth/`

Ticket can be retrieved by let user login from SSO UI. Ticket will be returned on the redirected URL param or body HTML.

Service URL is the URL that passed as URL parameter when redirect user to SSO UI login page. Service URL should be the URL of frontend that called SSO UI endpoint.

```json
{
    "ticket": "ST-472-kAnV6Npexxxxxxxxxxxx-sso.ui.ac.id",
    "service_url": "https://www.front-end-url.com/"
    // For local development, it might be "http://localhost:3000/"
}
```

- **Response**

Token needed for Token Authentication.

Status: 200

```json
{
    "major_id": "5fca7580cdbbxxxxxxxxxxxx",
    "token": "eyJ0eXAiOiJK-very-long-token-NDD07OVxi1yw",
    "user_id": "5fca7583cdbbxxxxxxxxxxxx"
}
```

#### Get Courses

Return list of available courses of selected major on current term.

- **Request**

`@require_jwt_token`
`GET /majors/<major_id>/courses`

- **Response**

Status: 200

```json
{
    "courses": [
        {
            "classes": [
                {
                    "lecturer": [
                        "Lecturer Name 1",
                        ...
                    ],
                    "name": "Class Name",
                    "schedule_items": [
                        {
                            "day": "Senin",
                            "end": "09.40",
                            "room": "A6.09 (Ged Baru)",
                            "start": "08.00"
                        },
                        {...},
                    ]
                }
                {...},
            ]
            "credit": 3,
            "name": "Course Name",
            "term": 6
        },
        {...},
    ],
    "is_detail": true,
    "name": "2019-2"
}
```

#### Save User Schedule

Create a user schedule and return UUI of the user schedule.

- **Request**

`@require_jwt_token`
`@require_same_user_id`
`POST /majors/<major_id>/courses`

```json
{
    "schedule_items": [
        {
            "day": "Senin",
            "end": "09.40",
            "name": "Class/Activity Name",
            "room": "A6.09 (Ged Baru)",
            "start": "08.00"
        },
        {...}
    ]
}
```

- **Response**

Status: 201

```json
{
    "id": "5fdbb1a6bbc4xxxxxxxxxxxx"
}
```

#### Get User Schedule Detail

Return a saved user schedule detail.

- **Request**

`@require_jwt_token`
`@require_same_user_id`
`GET /user_schedules/<user_schedule_id>`

- **Response**

Status: 200

```json
{
    "user_schedules": [
        {
            "created_at": "Fri, 18 Dec 2020 01:54:07 GMT",
            "id": "5fdba94fea3dxxxxxxxxxxxx",
            "name": "Schedule Name",
            "schedule_items": [
                {
                    "day": "Senin",
                    "end": "09.40",
                    "name": "Class/Activity Name",
                    "room": "A6.09 (Ged Baru)",
                    "start": "08.00"
                },
                {...}
            ]
        },
        {...}
    ]
}
```

#### Delete User Schedule

Delete user schedule and return nothing.

- **Request**

`@require_jwt_token`
`@require_same_user_id`
`POST /users/<user_id>/user_schedules/<user_schedule_id>`

- **Response**

Status: 204

#### Rename User Schedule

Rename user schedule and return UUID of renamed user schedule.

- **Request**

`@require_jwt_token`
`@require_same_user_id`
`POST /users/<user_id>/user_schedules/<user_schedule_id>/change_name`

- **Response**

Status: 200

```json

{
    "id": "5fdbb1a6bbc4xxxxxxxxxxxx"
}
```

## License

See LICENSE.md. This software actually goes a long way back, thank you so much to everyone involved.
