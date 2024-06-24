# ClimatePing

![ClimatePing Logo](./static/logo.png)

## Descripción

**ClimatePing** is a simple Flask application to check current weather conditions and daily forecasts for the city of La Plata. 
The app uses the Open-Meteo weather forecast API to obtain updated weather data.

## Technologies Used

- *Flask*
- *Open Meteo API*
- *Docker*
- *GitHub Actions*: (To be implemented as a future improvement) for CI/CD
- *AWS EC2*: (To be implemented as a future improvement) to deploy the application.

## Installation and Usage

### Locally

1. **Clone the repository:**:

```sh
git clone https://github.com/your-username/climateping.git
cd climateping
```
2. **Create and activate a python virtual environment**:
```sh
python -m venv venv
source venv/bin/activate  # En Windows usa `venv\Scripts\activate`
```

3. **Install all dependencies**:
```sh
pip install -r requirements.txt
```

4. **Run the app**:
```sh
python app.py
La aplicación estará disponible en http://127.0.0.1:5000.
```

### With Docker

1. **Build the Docker image**:
```sh
docker build -t climateping .
```
2. **Run the container**:
```sh
docker run -d -p 5000:5000 climateping
```


Either way now you can acces the application on your browser at http://127.0.0.1:5000.
