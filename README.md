# Botola Project

This project contains the `dash_app` and `transfermarkt_api` services, designed to run together using Docker Compose. The `dash_app` serves a dashboard application, while the `transfermarkt_api` provides the backend API services.

## Table of Contents
- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Running the Project](#running-the-project)
- [Accessing the Services](#accessing-the-services)
- [Configuration](#configuration)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

## Overview

The project is designed to run two services:
1. **dash_app**: A frontend dashboard application.
2. **transfermarkt_api**: A backend API service.

Both services run in separate Docker containers, connected through a Docker network. This setup ensures isolation, scalability, and ease of development.

## Prerequisites

Make sure you have the following installed:
- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

## Installation

1. **Clone this repository**:
   ```bash
   git clone <your-repo-url>
   cd <your-repo-directory>
