from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from controllers import auth_controller, library_controller, book_controller
from database import create_db_tables

import models.user
import models.book

@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db_tables()
    print("Database tables created (if they didn't exist).")
    yield

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_controller.router)
app.include_router(library_controller.router)
app.include_router(book_controller.router)

@app.get('/')
async def read_root(): # <-- La función debe ser 'async def' si devuelve una respuesta no trivial
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Digital Library Backend</title>
        <style>
            body {
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif, "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol";
                display: flex;
                justify-content: center;
                align-items: center;
                min-height: 100vh;
                background-color: #f4f4f4;
                margin: 0;
            }
            .container {
                background: white;
                border-radius: 10px;
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
                padding: 30px;
                max-width: 600px;
                width: 90%; /* Responsive width */
                text-align: center;
                box-sizing: border-box; /* Include padding in width */
            }
            p {
                font-size: 18px;
                color: #333;
                margin-bottom: 20px;
                font-weight: bold;
            }
            .warning {
                color: #e74c3c; /* Red color for warning */
            }
            .info {
                font-size: 16px;
                color: #555;
            }
            a {
                font-size: 18px;
                color: #3498db;
                text-decoration: none;
                font-weight: bold;
                padding: 10px 20px;
                background-color: #ecf0f1;
                border-radius: 5px;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                transition: all 0.3s ease;
                display: inline-block; /* Allows padding and margin */
            }
            a:hover {
                background-color: #dbe4e6;
                transform: translateY(-2px);
                box-shadow: 0 6px 10px rgba(0, 0, 0, 0.15);
            }
        </style>
    </head>
    <body>
        <div class="container">
            <p style="font-size: 20px; color: #333; margin-bottom: 20px; font-weight: bold;">
                ⚠️ <strong class="warning">This backend is hosted for FREE on Render</strong> and may take a few seconds to respond due to cold start.
            </p>
            <p style="font-size: 18px; color: #555; margin-bottom: 20px; font-weight: bold;">
                Now that we know the backend is up and running, feel free to visit the website:
            </p>
            <a href="https://digital-library-f.vercel.app/" target="_blank">
                👉 Go to the website
            </a>
            <p style="font-size: 16px; color: #777; margin-top: 20px;">
                Thank you for your patience and understanding!
            </p>
        </div>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content, status_code=200)