import socketserver
import threading

from telegram import Update
from telegram.constants import ParseMode
from telegram.error import BadRequest, Forbidden
from telegram.ext import Application, CommandHandler, CallbackContext
from werkzeug import http

TOKEN = "8118725511:AAFZUcyx8l1nEGQh9wxE-JnKx21zHE9u_ls"

app = Application.builder().token(TOKEN).build()

idDataGroupKietLac = [
    6343138254,  # Dev. Huỳnh Thông
    974755392,   # Chị Tuyền
    6843187206   # Văn Anh
]

idDataGroupSTSK = [
    6343138254,  # Dev. Huỳnh Thông
    915221350,   # Anh Thuận
    6472715042,  # Tuấn lỏ
]

idDataGroupSTSKB2B = [
    6343138254,  # Dev. Huỳnh Thông
    622900588,   # Anh Phong
    278142933,   # Chị Giang
]

idDataGroupNewProjectB2B = [
    6343138254,  # Dev. Huỳnh Thông
    622900588,   # Anh Phong
    1334692945,  # Thi
]

IDGroupNewGroupB2B = "-4775629953"
IDGroupKietLac = "-1002403939929"
IDGroupSTSK = "-4598566938"
IDGroupSTSKB2B = "-4542368071"

async def getInfo(update: Update, context: CallbackContext):
    idUser = update.effective_user.id
    idGroup = update.effective_chat.id
    name = update.effective_user.full_name
    await update.effective_message.reply_text(f"ID User: `{idUser}`\n"
                                              f"ID Group: `{idGroup}`\n"
                                              f"Name: {name}", parse_mode=ParseMode.MARKDOWN)

async def handleGroupMessage(update: Update, context: CallbackContext):
    print("Bắt đầu tag all")
    myID = update.effective_user.id
    group = []
    content = ""
    if str(update.effective_chat.id) == IDGroupSTSK:
        group = idDataGroupSTSK
    if str(update.effective_chat.id) == IDGroupKietLac:
        group = idDataGroupKietLac
    if str(update.effective_chat.id) == IDGroupSTSKB2B:
        group = idDataGroupSTSKB2B
    if str(update.effective_chat.id) == IDGroupNewGroupB2B:
        group = idDataGroupNewProjectB2B
    i = 0
    for member_id in group:
        try:
            user = await context.bot.get_chat(member_id)
            if user.id != myID:
                name = f"{user.first_name} {user.last_name}"
                if i > 0:
                    content += " , "
                content += f"[{name}](tg://user?id={user.id}) "
                i += 1
        except (BadRequest, Forbidden) as ex:
            print(f'Error BadRequest, Forbidden: {ex}')
        except Exception as e:
            print(f'Error: {e}')

    if content != "":
        content = f"Tag all: {content}"
        await update.message.reply_text(content, parse_mode=ParseMode.MARKDOWN)

# Add command handlers
app.add_handler(CommandHandler("all", handleGroupMessage))
app.add_handler(CommandHandler("get_info", getInfo))

# Use long polling instead of webhook
print("===============Khởi động Bot Thành công===============")
# Bắt đầu bot

def initialize_bot_telegram():
    print("===============initialize_bot_telegram===============")
    app.run_polling()

def run_server_fake():
    # Define the port to run the server on
    PORT = 8000

    # Set up the server to serve files from the current directory
    Handler = http.server.SimpleHTTPRequestHandler

    # Create the server
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"Serving at http://localhost:{PORT}")
        # Start the server and keep it running until interrupted
        httpd.serve_forever()


if __name__ == 'main':
    bot_threading = threading.Thread(target=initialize_bot_telegram)
    run_server_threading = threading.Thread(target=run_server_fake)

    bot_threading.start()
    run_server_threading.start()

    bot_threading.join()
    run_server_threading.join()