# Digital Library — Backend API

🔗 **Frontend App (Live)**: [https://digital-library-f.vercel.app/](https://digital-library-f.vercel.app/)

Welcome to the **Digital Library Backend API!** This project serves as the robust foundation for managing user authentication, storing user-specific book collections, and providing access to a curated catalog of books. Built with FastAPI and PostgreSQL, it ensures efficient and secure data handling, powering the interactive frontend application.

---

## 🚀 Technologies Used

- ⚙️ Python: The core language for the backend logic.

- ✨ FastAPI: A modern, fast (high-performance) web framework for building APIs with Python 3.7+ based on standard Python type hints.

- 🐘 PostgreSQL: A powerful, open-source relational database system for storing all application data.

- 💚 SQLAlchemy (Async): An ORM (Object Relational Mapper) used for interacting with the PostgreSQL database asynchronously.

- 🔐 JWT (JSON Web Tokens): For secure user authentication and authorization.

- 🛡️ OAuth2 with Bearer Tokens: Implemented for API security, ensuring that only authenticated users can access protected resources.

- ☁️ Render: The cloud platform used for deploying the backend API.

- 📦 Poetry: For dependency management and project setup.
---

## 📦 API Endpoints

### 🔐 Authentication (/auth)
- POST /auth/register — Register a new user
- Body: { "username": "user", "password": "pass" }

- POST /auth/login — Log in and receive a token
- Body: { "username": "user", "password": "pass" }

### 📚 Books (/books)
Provides access to the public book catalog. These endpoints do not require authentication.

- GET /books  
- Description: Retrieves a list of all available books in the digital library.

### 📖 User Library (/library)
Manages the user's personal collection of books. These endpoints require authentication via a JWT Bearer Token.

- POST /library

Description: Adds a book to the authenticated user's library.

Query Parameters:

book_id: string (The ID of the book to add)

Headers: Authorization: Bearer <your_token>

Responses:

200 OK: Book successfully added to the user's library. Returns updated user details.

401 Unauthorized: Authentication required.

404 Not Found: Book not found or user not found.

- GET /library

Description: Retrieves all books currently in the authenticated user's library.

Headers: Authorization: Bearer <your_token>

Responses:

200 OK: Returns an array of book objects in the user's library.

401 Unauthorized: Authentication required.

- DELETE /library/{book_id}

Description: Removes a specific book from the authenticated user's library.

Path Parameters:

book_id: string (The ID of the book to remove)

Headers: Authorization: Bearer <your_token>

Responses:

200 OK: Book successfully removed. Returns updated user details.

401 Unauthorized: Authentication required.

404 Not Found: Book not found in the user's library.

### 💡 Key Features

- User Authentication: Secure user registration and login using JWTs.

- Personalized Libraries: Users can maintain their own collections of books.

- Public Book Catalog: Browse a comprehensive list of all available books.

- Database Management: Efficient asynchronous interaction with PostgreSQL using SQLAlchemy.

- Scalable Architecture: Built with FastAPI for high performance and easy extensibility.

- CORS Enabled: Configured to allow cross-origin requests for seamless frontend integration.

- Production-Ready Deployment: Configured for deployment on Render, including SSL handling for secure connections.
- 
----

## 📬 Contact

Created by **Facundo Robert** – [GitHub](https://github.com/RobertFacundo)  

Feel free to reach out for collaboration or feedback!!

----