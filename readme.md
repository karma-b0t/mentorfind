
## Local Run Prerequisites
- create `.env` file in the root directory from .env_example

- install `ngrok` tool
* create account
* authorize

- install `pgadmin` tool.

## Local Run with Docker
- run ngrok:
`ngrok http 80`

- use ngrock URL in .env `WENHOOK_URL`

- test DB is up. Connect to `postgresql+psycopg://postgres:123@db:5432/mentors` via `pgadmin`

- run `set commands` once:
1. run `pip install -r requirements.txt`
2. run `py set_commands.py`

- run:
```
docker compose up --build
```

- stop and remove volumes:
```
docker compose down
```