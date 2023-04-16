# sqlalchemy2_base
learning and building a base for other projects to use SQLAlchemy 2.0 +



## FastAPI Endpoints


### Health Endpoints

1. `/api/health/metrics`: This endpoint handles GET requests and returns system metrics in a Prometheus-compatible format.

2. `/api/health/status`: This endpoint handles GET requests and returns the status of the system, uptime, and current datetime.

3. `/api/health/system-info`: This endpoint handles GET requests and returns information about the system's CPU usage.

4. `/api/health/processes`: This endpoint handles GET requests and returns a list of running processes filtered by python processes.

5. `/api/health/configuration`: This endpoint handles GET requests and returns configuration settings for the API.

6. `/api/health/heapdump`: This endpoint handles GET requests and returns a heap dump from the running application.
