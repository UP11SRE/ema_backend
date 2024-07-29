# Ema Backend

This project is the backend application for the Google Drive File Picker and reader, built with Django. It provides a RESTful API for interacting with Google Drive files and managing user authentication.

## Features

### User Authentication

- Users can register for an account.
- Users can log in with their existing credentials.
- Token-based authentication for secure access.

### File Management

- Upload files from Google Drive.
- Retrieve all uploaded files.
- Download files from Google Drive.

## Technologies

- Backend: Django, Django REST Framework
- Database: SQLite (or any other database of your choice)
- Authentication: Token-based authentication

## Getting Started

### Prerequisites

- Python 3.x
- Django
- Django REST Framework

### Installation

1. Clone this repository.
   bash
   git clone <repository-url>
   cd ema-backend

2. Install dependencies:
   bash
   pip install -r requirements.txt

3. Set up environment variables:
   - Create a `.env` file in the project root and add your Google Drive API credentials.

### Running the Development Server

1. Run database migrations:
   bash
   python manage.py migrate

2. Start the development server:
   bash
   python manage.py runserver

3. The API will be available at `http://localhost:8000/`.

### Docker Deployment

- A Dockerfile is included for easy deployment. To run the project using Docker:

  1. Build the Docker image:

     ```
     bash
     docker build -t ema-backend .

     ```

  2. Run the Docker container:
     ```
     bash
     docker run -p 8000:8000 ema-backend
     ```

## API Endpoints

### User Registration

- **Endpoint**: `/api/auth/registration/`
- **Method**: `POST`
- **Request Body**:
  json
  {
  "username": "exampleuser",
  "email" : "email"
  "password1": "examplepassword",
  "password2": "examplepassword",
  }

- **Response**:
  json
  {
  "message": "User registered successfully."
  }

### User Login

- **Endpoint**: `/api/auth/login/`
- **Method**: `POST`
- **Request Body**:
  json
  {
  "username": "exampleuser",
  "password": "examplepassword"
  }

- **Response**:
  json
  {
  "key": "token"
  }

### Get All Files from your Google drive

- **Endpoint**: `/api/files/list`
- **Method**: `GET`
- **Headers**:
  - `Authorization: Token your_token`
- **Response**:
  json
  [
  {
  "id": 1,
  "name": "File 1",
  "size": "1024",
  "google_drive_id": "1JNzcaAaptY3X7ItpQQ6-FpLI_bc2PwpncOAoJs4KF_c"
  },
  ...
  ]

  ### Upload File

- **Endpoint**: `/api/files/upload/`
- **Method**: `POST`
- **Headers**:
  - `Authorization: Token your_jwt_token`
- **Request Body**:
  {
  "files": [
  {
  "name": "File 1",
  "size": "1024",
  "google_drive_id": "1JNzcaAaptY3X7ItpQQ6-FpLI_bc2PwpncOAoJs4KF_c"
  },
  {
  "name": "File 2",
  "size": "2048",
  "google_drive_id": "1JNzcaAaptY3X7ItpQQ6-FpLI_bc2PwpncOAoJs4KF_d"
  }
  ]
  }

- **Response**:
  json
  {
  "message": "File uploaded successfully.",
  "file_id": 1
  }

### Get All Files which you have uploaded

- **Endpoint**: `/api/files/getall`
- **Method**: `GET`
- **Headers**:
  - `Authorization: Token your_token`
- **Response**:
  json
  [
  {
  "id": 1,
  "name": "File 1",
  "size": "1024",
  "google_drive_id": "1JNzcaAaptY3X7ItpQQ6-FpLI_bc2PwpncOAoJs4KF_c"
  },
  ...
  ]

### Read Files which you have uploaded to our database

- **Endpoint**: `/api/files/read/<file_id>/`
- **Method**: `GET`
- **Headers**:
  - `Authorization: Token your token`
- **Response**: The file will be downloaded.
  # but this is working from the frontend only.

## Frontend Integration

- Frontend Github Repo : https://github.com/UP11SRE/ema-frontend.git

- This backend is designed to work with a frontend application that allows users to interact with their Google Drive files. You can access the frontend at `http://localhost:5173/`.

## Contributing

Pull requests and contributions are welcome! Please follow standard coding practices and create issues for any bugs or feature requests.

## License

This project is licensed under the MIT License. See the LICENSE file for details.
