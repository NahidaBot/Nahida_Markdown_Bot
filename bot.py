import logging
import marko
from utils.escaper import html_esc, html_tag_filter
from uuid import uuid4

from telegram import InlineQueryResultArticle, InputTextMessageContent, Update
from telegram.constants import ParseMode
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    InlineQueryHandler,
    MessageHandler,
    filters,
)

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.DEBUG
)
logger = logging.getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    await update.message.reply_text(
        "Send markdown in code quotes, and this bot will answer markdown message with syntax telegram supported. \nNon-Supported markdown syntax will fallback to plain text. \n\nYou can also use inline mode, up to 256 chars. \n\n Cause telegram limit, markdown text contains code quotes must send in ``` . "
    )


async def inline_query(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the inline query. This is run when you type: @botusername <query>"""
    query = update.inline_query.query

    if not query:  # empty query should not be handled
        return

    html = html_tag_filter(marko.convert(html_esc(query)))

    results = [
        InlineQueryResultArticle(
            id=str(uuid4()),
            title="Markdown",
            input_message_content=InputTextMessageContent(
                html,
                parse_mode=ParseMode.HTML,
            ),
        )
    ]

    await update.inline_query.answer(results)


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message."""

    html = html_tag_filter(marko.convert(html_esc(update.message.text)))

    await update.message.reply_text(html, parse_mode=ParseMode.HTML)


def main() -> None:
    """Run the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token("token").build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", start))

    # on non command i.e message - echo the message on Telegram
    application.add_handler(InlineQueryHandler(inline_query))

    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    main()
