# React-Kit Project

## Overview

This repository contains a full-stack application with a backend (Python) and a frontend (React with TypeScript). The project is designed to provide a robust and scalable architecture for modern web applications.

## Core Features

### Backend
- User authentication and authorization (including Google OAuth).
- OTP-based verification.
- Database models for user management, OTP, and reset tokens.
- Middleware for request handling and authentication.
- Utility functions for email, SMS, JWT, and hashing.
- Code formatting script (`format.py`) for maintaining consistent code style in the `/app` directory.

### Frontend
- Responsive and modern UI built with React 19 and Tailwind CSS v4.
- TypeScript for type safety and better developer experience.
- Automatic API type generation using `npm run api`.
- Integration with backend APIs for user authentication and data management.
- Component library integration with `shadcn/ui` for reusable and accessible UI components.
- Strict linting and formatting using ESLint and Prettier.

## Prerequisites

- Node.js (v16 or later)
- Python (v3.10 or later)
- npm or yarn
- pip (Python package manager)

## Setup Instructions

### Backend

1. Navigate to the `backend` directory:
   ```bash
   cd backend
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   ```

3. Activate the virtual environment:
   - On Windows:
     ```bash
     .\venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

5. Run the backend server:
   ```bash
   python app/main.py
   ```

6. Format the backend code:
   ```bash
   python format.py
   ```

### Frontend

1. Navigate to the `frontend` directory:
   ```bash
   cd frontend
   ```

2. Install Node.js dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm run dev
   ```

4. Generate API types:
   ```bash
   npm run api
   ```

## Project Structure

```
react-kit/
├── backend/
│   ├── app/
│   ├── database/
│   ├── middlewares/
│   ├── models/
│   ├── routes/
│   ├── schemas/
│   ├── services/
│   └── utils/
├── frontend/
│   ├── public/
│   └── src/
└── README.md
```

## Commands Explained

### Backend
- `python -m venv venv`: Creates a virtual environment.
- `.\venv\Scripts\activate` or `source venv/bin/activate`: Activates the virtual environment.
- `pip install -r requirements.txt`: Installs all required Python packages.
- `uvicorn app.main:app --reload --port 8000`: Starts the backend server.
- `python format.py`: Formats all code in the `/app` directory.

### Frontend
- `npm install`: Installs all required Node.js packages.
- `npm run dev`: Starts the frontend development server.
- `npm run api`: Generates TypeScript types for API interactions.

## Contributing

1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. Submit a pull request with a detailed description of your changes.

## License

This project is licensed under the MIT License. See the LICENSE file for details.