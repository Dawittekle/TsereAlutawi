# 🚀 ጸረ አሉታዊ Bot

![image](https://github.com/user-attachments/assets/92c75162-2f89-49c7-866f-2d37564f8caa)


A powerful *Telegram bot* that detects and removes hate speech in group chats using *NLP*. It warns users, notifies admins, and removes repeat offenders automatically. You can try the bot here: [@tserealutawi\_bot]\(https\://t.me/tserealutawi\_bot)

## ✨ Features

- ✅ **Auto-Delete Hate Speech** – Instantly removes offensive messages.
- ✅ **User Warning System** – Issues up to 5 warnings before removal.
- ✅ **Auto-Kick Offenders** – Users with 5 warnings are removed.
- ✅ **Admin Notifications** – Alerts admins about violations.
- ✅ **Admin Management** – Add or remove admins easily.

## 🛠️ Installation

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/your-username/hate-speech-monitor-bot.git
cd hate-speech-monitor-bot
```

### 2️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 3️⃣ Set Up Environment Variables

Create a `.env` file and add your **Telegram Bot Token**:

```env
BOT_TOKEN=your-telegram-bot-token
```

### 4️⃣ Run the Bot

```bash
python bot.py
```

## 📌 Commands

**User Commands:**

- `/help` – Show available commands.
- `/id` – Get your Telegram user ID.

**Admin Commands:**

- `/addadmin <user_id>` – Add an admin.
- `/removeadmin <user_id>` – Remove an admin.
- `/listadmins` – List all admins.
- `/unban <user_id>` – Unban a user and reset warnings.

## 🤖 How It Works

1. The bot **monitors messages** in your group.
2. If a message contains **hate speech**, it is **deleted**.
3. The user receives a **warning** (privately).
4. After **5 warnings**, the user is **removed** from the group.
5. **Admins receive alerts** about violations.

## ⚠️ Notes

- Ensure the bot has **admin permissions** in your Telegram group.
- Admins can manage the bot using the provided commands.

## 🤝 Contribute

If you want to contribute to add multiple language, contact me!

---

🔥 Developed with ❤️ to keep communities safe!

