from telegram import Update
from telegram.constants import ParseMode
from telegram.error import BadRequest, Forbidden
from telegram.ext import Application, CommandHandler, CallbackContext

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

# Start polling for updates
app.run_polling()
