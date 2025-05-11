## Create Virtual Environment

```bash
python3.10 -m venv .venv
```

## Activate Virtual Enviroment

```bash
.venv/Scripts/activate
```

OR in Mac/Linux

```bash
source .venv/bin/activate
```

## Install Requirements

```bash
pip install -r requirements.txt
```

## Run Command

```bash
uvicorn app.main:app --reload
```

OR run the following to specify port number and to allow all host:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

```