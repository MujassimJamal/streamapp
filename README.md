# Steps to run the application in development environment
### Prerequisites
1. Docker version 26>=.
2. Docker Compose version v2.27>=.

### Steps
1. Clone the repository in your desktop location: `git clone https://github.com/MujassimJamal/streamapp.git`
2. Go to the project directory: `cd streamapp`
3. Build the image and run services: `docker compose up --build` (Wait for all services to be up and running, you should be able to see the final message: Watching for file changes with StatReloader)
4. Open any browser and visit: `http://localhost/stream`
