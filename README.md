# Library Microservices System

This project represents a microservices-based system for library management.

## Project purpose

The system allows users to browse books, search the catalog, and borrow or reserve books through a web application.

## Main components

- uporabniki – microservice for user registration, authentication and user management
- knjige – microservice for book catalog, search and availability
- izposoja – microservice for borrowing, reservations and returning books
- web-ui – web application used as the user interface

## Architecture

The system is based on a microservices architecture.

Each microservice is responsible for a specific business domain:

- uporabniki manages user accounts and authentication
- knjige manages the book catalog and availability
- izposoja manages book borrowing and reservations

The web-ui component provides the user interface and communicates with the microservices through REST APIs.

Each microservice is designed as an independent component that can be developed and deployed separately.

## Project structure
library-microservices-system
│
├── docs
│   └── README.md
│
├── uporabniki
│   └── README.md
│
├── knjige
│   └── README.md
│
├── izposoja
│   └── README.md
│
└── web-ui
└── README.md

Each folder represents a separate component of the system. The microservices are organized according to business domains to follow the principles of Clean Architecture and microservices design.
