# Vectorizer

A Python application for vectorizing images.

## Setup and Running Without Docker

1. Create a virtual environment:
```bash
python -m venv venv
```

2. Activate the virtual environment:
- Windows:
```bash
.\venv\Scripts\activate
```
- Unix/MacOS:
```bash
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements-.txt
```

4. Configure environment variables:
- Copy `.env.example` to `.env`
- Update the values in `.env` with your configuration:
  - `PORT`: The port to run the server on (default: 5000)
  - `S3_BUCKET`: Your S3 bucket name for storing results
  - `PYTHON_ENV`: Environment (development/production)

5. Run the application:
```bash
python run.py
```

The server will start on http://localhost:5000

## API Endpoints

- `POST /`: Main endpoint for vectorizing images
- `GET /health`: Health check endpoint
- `GET /test-error`: Test error endpoint

## Example Request

```json
{
    "url": "https://example.com/image.jpg",
    "solver": 0,  // 0 for binary solver, 1 for color solver
    "color_count": 8,  // Optional, used with color solver
    "raw": false,  // Optional, return raw markup if true
    "crop_box": [0, 0, 100, 100]  // Optional, crop image before processing
}
```
