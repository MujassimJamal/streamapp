# Steps to Run the Application in the Development Environment
### Prerequisites
1. Docker version 26 or higher.
2. Docker Compose version v2.27 or higher.
3. Git version 2 or higher.
4. Stable internet connection

### Steps
1. Clone the repository to your desired location:
   - `git clone https://github.com/MujassimJamal/streamapp.git`
2. Navigate to the project directory:
   - `cd streamapp`
3. Build the image and start the services:
   - `docker compose up --build`
(Wait for all services to be up and running. You should see the final message: "Watching for file changes with StatReloader.")
4. Open a browser and visit:
   - http://localhost/stream
