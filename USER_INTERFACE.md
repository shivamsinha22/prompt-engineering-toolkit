# User Interface

This version uses only Python's built-in libraries.

## Run

```bash
python app.py
```

Then open:

http://127.0.0.1:8000

No Flask installation and no `pip install` are required.

## API

- `GET /` - web interface
- `GET /strategies` - available prompt strategies
- `POST /generate` - generates a prompt from user input
