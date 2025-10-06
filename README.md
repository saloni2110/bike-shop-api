# Bike Shop API

A simple and robust RESTful API for managing a collection of bicycles, built with Python, Flask, and MongoDB. This project is fully deployed and live on Render.

## Live API Endpoint

The live API is hosted on Render at: `[PASTE YOUR RENDER URL HERE](https://bike-shop-api-ptly.onrender.com]`

---

## Features

- **Full CRUD Functionality:** Create, Read, Update, and Delete bikes.
- **RESTful Architecture:** Follows standard REST principles for predictable URLs and HTTP methods.
- **MongoDB Atlas Integration:** Uses a cloud-hosted NoSQL database for flexible and scalable data storage.
- **Production Ready:** Deployed with a Gunicorn production server.

---

## API Endpoints

### Bikes Collection

#### `GET /api/v1/bikes`
- **Description:** Retrieves a list of all bikes in the database.
- **Success Response:** `200 OK` with an array of bike objects.

#### `POST /api/v1/bikes`
- **Description:** Adds a new bike to the database.
- **Request Body (JSON):**
  ```json
  {
    "make": "BrandName",
    "model": "ModelName",
    "type": "Road/Mountain/etc.",
    "price": 1500
  }
