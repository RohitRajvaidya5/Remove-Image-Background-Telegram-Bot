# AI Background Remover Telegram Bot

AI-powered Telegram bot that removes backgrounds from images and returns a transparent PNG using **Python**, **python-telegram-bot**, and **rembg (BiRefNet)**.

## Features

* Remove backgrounds from photos automatically
* Supports portraits and general objects
* Returns high-quality transparent PNG images
* Fast and easy to use through Telegram
* Built with Python and AI image segmentation models
* Ready for deployment on Render, Railway, or VPS

---

## Demo

1. Open the Telegram bot.
2. Send a photo.
3. The bot processes the image using AI.
4. Receive a transparent PNG with the background removed.

---

## Tech Stack

* Python
* python-telegram-bot
* rembg
* BiRefNet
* Pillow
* NumPy
* ONNX Runtime

---

## Project Structure

```text
background-remover-bot/
│
├── bot.py
├── requirements.txt
├── .gitignore
├── downloads/
├── outputs/
└── README.md
```

---

## Installation

### Clone Repository

```bash
git clone https://github.com/your-username/background-remover-bot.git

cd background-remover-bot
```

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Virtual Environment

Windows:

```bash
venv\Scripts\activate
```

Linux / macOS:

```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Environment Variables

Create a `.env` file:

```env
BOT_TOKEN=YOUR_TELEGRAM_BOT_TOKEN
```

---

## Running Locally

```bash
python bot.py
```

Expected output:

```text
Loading AI model...
Bot running...
```

---

## Telegram Bot Setup

1. Open Telegram.
2. Search for BotFather.
3. Create a new bot using:

```text
/newbot
```

4. Copy the generated bot token.
5. Add the token to your `.env` file.

---

## Deployment

### Render

1. Push project to GitHub.
2. Create a new Web Service on Render.
3. Connect your repository.
4. Configure:

Build Command:

```bash
pip install -r requirements.txt
```

Start Command:

```bash
python bot.py
```

5. Add environment variable:

```text
BOT_TOKEN=YOUR_TOKEN
```

6. Deploy.

---

## Supported Models

Below is a list of available models and what they are best for:

| Model | Best For |
|---|---|
| u2net | Original rembg model, good general-purpose background removal |
| u2netp | Smaller and faster version of U²-Net, lower accuracy |
| u2net_human_seg | Human portraits only |
| u2net_cloth_seg | Clothing segmentation |
| silueta | Lightweight model, fast but less accurate |
| isnet-general-use | Improved general-purpose model (currently used) |
| isnet-anime | Anime and cartoon characters |
| sam | Meta Segment Anything Model (more flexible but heavier) |

Note: I'm currently using `isnet-general-use` to reduce memory usage inside Docker containers; the larger models may not fit due to memory constraints.

### BiRefNet (Recommended)

```python
session = new_session("birefnet-general")
```

Best overall quality for portraits and objects.

### Human Segmentation

```python
session = new_session("u2net_human_seg")
```

Optimized for people and profile pictures.

### Default Model

```python
session = new_session("u2net")
```

Faster but lower quality.

---

## Error Handling

The bot includes handling for:

* Invalid images
* Download failures
* Background removal failures
* File processing errors
* Unexpected runtime exceptions

---

## Future Improvements

* Batch image processing
* Multiple AI model selection
* Watermark support
* Usage analytics
* Docker deployment
* FastAPI backend integration
* User request history
* Image compression options

---

## License

This project is licensed under the MIT License.

---

## Author

Rohit Rajvaidya

Backend Developer | Python | Django | FastAPI | SQL | Automation

Built as a portfolio project to demonstrate AI integration, image processing, Telegram bot development, and deployment skills.
