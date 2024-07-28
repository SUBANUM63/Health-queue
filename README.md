# Health Queue Web-Based Project

## Overview
Health Queue is a web-based application designed to streamline the patient queue management system in healthcare facilities. The project aims to improve the patient experience and operational efficiency by providing a user-friendly interface for managing appointments and tracking patient flow.

## Features
- **User-Friendly Interface**: Intuitive design for ease of use by both patients and healthcare staff.
- **Real-Time Queue Management**: Monitor and manage patient queues in real time.
- **Appointment Scheduling**: Patients can book, reschedule, or cancel appointments online.
- **Notifications**: Automated SMS or email notifications to remind patients of their appointments.
- **Patient Tracking**: Track patient status from check-in to check-out.
- **Reporting**: Generate reports on patient flow, wait times, and other key metrics.

## Technologies Used
- **Frontend**: HTML, CSS, JavaScript, React.js
- **Backend**: Python, Flask
- **Database**: MySQL
- **Other Tools**: Docker, Git, Redis

## Installation
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/SUBANUM63/health-queue.git
   cd health-queue
   ```
2. **Set Up Virtual Environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   source  ./set_env.sh
  . ```
3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
4. **Set Up Database**:
   - Ensure MySQL is installed and running.
   - Create a database and update the database URL in the configuration file.
   - Run the Application:
   - you can initialize the data base by running:
   ```bash
   python3 init_db.py
   ``` 
5. **Run the Application**:
   ```bash
   python3 run.py
   ```
# Usage
- **Admin Panel**: Access the admin panel to manage the system settings, view reports, and handle patient queues.
- **Patient Interface**: Patients can log in to book appointments, check their queue status, and receive notifications.

# Contributing
- ## Fork the repository.
- ## Create a new branch (git checkout -b feature-branch).
- ## Make your changes.
- ## Commit your changes (git commit -m 'Add some feature').
- ## Push to the branch (git push origin feature-branch).
- ## Open a pull request.

# License
- This project is licensed under the MIT License - see the LICENSE file for details.

# Contact
- For any questions or suggestions, please contact zeinuka641@gmail.com.


- Feel free to download, use, and contribute to the Health Queue project to help improve the healthcare system's efficiency and patient experience

