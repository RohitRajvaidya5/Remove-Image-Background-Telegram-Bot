from telegram import Update
from telegram.ext import (
    Application,
    MessageHandler,
    CommandHandler,
    ContextTypes,
    filters
)
from dotenv import load_dotenv
from rembg import remove, new_session
from PIL import Image
from io import BytesIO
import numpy as np
import os
import logging


load_dotenv()

TOKEN = os.getenv("TELEGRAM_TOKEN")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

os.makedirs("downloads", exist_ok=True)
os.makedirs("outputs", exist_ok=True)

session = new_session("isnet-general-use")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.effective_message
    if message is None:
        return

    await message.reply_text(
        """
📸 Send any photo and I'll remove its background.

Supported:
✅ Portrait photos
✅ Product photos
✅ Animals
✅ Objects

Output:
🖼️ Transparent PNG
"""
    )

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.effective_message
    if message is None:
        return

    await message.reply_text(
        """
👋 Welcome to AI Background Remover Bot

How to use:

1️⃣ Send any photo to this chat
2️⃣ The AI will automatically remove the background
3️⃣ You'll receive a transparent PNG image

✨ Best results:
• Use clear, high-quality images
• Ensure the subject is visible
• Portraits and product photos work best

📸 Just send a photo to get started!
"""
    )

async def remove_background(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    try:
        msg = update.effective_message
        if msg is None:
            return

        await msg.reply_text(
            "Processing image..."
        )

        if not msg.photo:
            await msg.reply_text(
                "Please send a valid image."
            )
            return

        photo = msg.photo[-1]

        input_path = (
            f"downloads/{photo.file_unique_id}.jpg"
        )

        output_path = (
            f"outputs/{photo.file_unique_id}.png"
        )

        try:
            input_file = await photo.get_file()
            await input_file.download_to_drive(input_path)

        except Exception as e:
            logging.exception("Image download failed")

            await msg.reply_text(
                "Failed to download image."
            )
            return

        try:
            input_image = Image.open(input_path)

        except Exception:
            await msg.reply_text(
                "Invalid image file."
            )
            return

        try:
            raw = remove(
                input_image,
                session=session,
                alpha_matting=True,
                alpha_matting_foreground_threshold=240,
                alpha_matting_background_threshold=10,
                alpha_matting_erode_size=10
            )

        except Exception as e:
            logging.exception("Background removal failed")

            await msg.reply_text(
                "Failed to remove background."
            )
            return

        if isinstance(raw, (bytes, bytearray, memoryview)):
            output_image = Image.open(
                BytesIO(bytes(raw))
            ).convert("RGBA")

        elif isinstance(raw, np.ndarray):
            output_image = Image.fromarray(raw).convert("RGBA")

        elif isinstance(raw, Image.Image):
            output_image = raw.convert("RGBA")

        else:
            try:
                output_image = Image.open(
                    BytesIO(bytes(raw))
                ).convert("RGBA")

            except Exception:
                raise TypeError(
                    f"Unsupported output type: {type(raw)}"
                )

        output_image.save(output_path)

        with open(output_path, "rb") as file:
            await msg.reply_document(
                document=file,
                filename="background_removed.png"
            )

        logging.info(
            f"Successfully processed {photo.file_unique_id}"
        )

    except Exception:
        logging.exception("Unexpected error")

        # attempt to notify the user if possible
        err_msg = update.effective_message
        if err_msg is not None:
            await err_msg.reply_text(
                "An unexpected error occurred. Please try again."
            )

    finally:
        if os.path.exists(input_path):
            os.remove(input_path)

        if os.path.exists(output_path):
            os.remove(output_path)


if TOKEN is None:
    raise RuntimeError("TELEGRAM_TOKEN environment variable is not set")

app = Application.builder().token(TOKEN).build()

app.add_handler(
    CommandHandler("start", start)
)

app.add_handler(
    CommandHandler("help", help_command)
)

app.add_handler(
    MessageHandler(
        filters.PHOTO,
        remove_background
    )
)



print("Bot running...")
app.run_polling()
