# Profile Counter

A self-hosted profile counter created as a replacement for the now-defunct `https://profile-counter.glitch.me/:yourkey:/count.svg` service.

## 🚀 Features

- Self-hosted and lightweight
- Real-time profile visit counting
- Embeddable SVG badge for websites

## 🔍 Demo

![Profile Counter Repo :: Visitor's Count](https://server.jagaldol.com/profile-counter/jagaldol-profile-counter/count.svg)

the counter for this repo

## 🛠️ Usage

This project is self-hosted using Docker Compose. The backend is powered by a FastAPI server connected to a Redis store.

### 1. Prerequisites

- Docker
- Docker Compose

### 2. Start the Service

Clone the repository and run the following command:

```bash
docker-compose up -d
```

This will launch:

- `app.py`: the FastAPI application server
- `Redis`: the data store for tracking visit counts

### 3. Access the Counter

Once running, you can embed the counter using:

```html
<img src="http://localhost:3001/profile-counter/:your-key:/count.svg" />
```

Replace `:your-key:` with your own identifier.

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](./LICENSE) file for details.
