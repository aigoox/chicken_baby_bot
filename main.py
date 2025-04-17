from telegram import Update
from telegram.constants import ParseMode
from telegram.error import BadRequest, Forbidden
from telegram.ext import Application, CommandHandler, CallbackContext
from flask import Flask, request
import os

# Token của bot
TOKEN = "8118725511:AAFZUcyx8l1nEGQh9wxE-JnKx21zHE9u_ls"

# Khởi tạo bot Telegram
app = Application.builder().token(TOKEN).build()

# Cấu hình các ID nhóm
idDataGroupKietLac = [
    6343138254, #Dev. Huỳnh Thông
    974755392,  #Chị Tuyền
    6843187206  # Văn Anh
]

idDataGroupSTSK = [
    6343138254, #Dev. Huỳnh Thông
    915221350,  #Anh Thuận
    6472715042, #Tuấn lỏ
]

idDataGroupSTSKB2B = [
    6343138254, #Dev. Huỳnh Thông
    622900588,  #Anh Phong
    278142933, #Chị Giang
]

idDataGroupNewProjectB2B = [
    6343138254, #Dev. Huỳnh Thông
    622900588,  #Anh Phong
    1334692945, #Thi
]

IDGroupNewGroupB2B = "-4775629953"
IDGroupKietLac = "-1002403939929"
IDGroupSTSK = "-4598566938"
IDGroupSTSKB2B = "-4542368071"

# Cấu hình command get_info để trả về thông tin người dùng
async def getInfo(update: Update, context: CallbackContext):
    idUser = update.effective_user.id
    idGroup = update.effective_chat.id
    name = update.effective_user.full_name
    await update.effective_message.reply_text(f"ID User: `{idUser}`\n"
                                              f"ID Group: `{idGroup}`\n"
                                              f"Name: {name}", parse_mode=ParseMode.MARKDOWN)

# Xử lý tin nhắn trong nhóm và tag tất cả thành viên
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
                name = f"{user.first_name} {user.last_name}" if user.last_name else user.first_name
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

# Thêm các handler cho các command
app.add_handler(CommandHandler("all", handleGroupMessage))
app.add_handler(CommandHandler("get_info", getInfo))

# Khởi tạo Flask app để xử lý webhook
flask_app = Flask(__name__)

# Cấu hình route cho webhook của bot Telegram
@flask_app.route('/' + TOKEN, methods=['POST'])
def webhook():
    json_str = request.get_data().decode('UTF-8')
    update = Update.de_json(json_str, app.bot)
    app.process_update(update)
    return 'OK'

# Cấu hình một route mặc định để kiểm tra bot đang chạy
@flask_app.route('/')
def index():
    return 'Bot is running!'

# Thiết lập webhook cho bot Telegram
def set_webhook():
    url = os.getenv("WEBHOOK_URL") + '/' + TOKEN
    app.bot.set_webhook(url)

if __name__ == '__main__':
    set_webhook()
    flask_app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 10000)))
