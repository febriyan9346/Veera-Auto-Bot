# Veera Auto Bot

Automated bot for claiming daily rewards on Veera Rewards platform.

## 🌐 Official Platform

Access the platform here: [https://hub.veerarewards.com/loyalty?referral_code=O9C51R3W](https://hub.veerarewards.com/loyalty?referral_code=O9C51R3W)

## ✨ Features

- Automatic daily task claiming
- Multi-account support
- Proxy support (optional)
- Auto-retry with countdown timer
- Colorful console logging
- Cross-platform compatibility (Windows, Linux, macOS)

## 📋 Prerequisites

- Python 3.7 or higher
- pip package manager

## 🚀 Installation

1. Clone this repository:
```bash
git clone https://github.com/febriyan9346/Veera-Auto-Bot.git
cd Veera-Auto-Bot
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

## 📝 Configuration

1. Create `accounts.txt` file and add your private keys (one per line):
```
your_private_key_1
your_private_key_2
your_private_key_3
```

2. (Optional) Create `proxy.txt` file if you want to use proxies (one per line):
```
http://user:pass@ip:port
http://user:pass@ip:port
```

**⚠️ Security Warning:** Never share your private keys with anyone! Keep your `accounts.txt` file secure and private.

## 🎮 Usage

Run the bot:
```bash
python bot.py
```

Choose your preferred mode:
- Option 1: Run with proxy
- Option 2: Run without proxy

The bot will:
- Login to each account
- Claim daily tasks
- Wait 24 hours before the next cycle
- Repeat automatically

## 📂 File Structure

```
Veera-Auto-Bot/
│
├── bot.py              # Main bot script
├── accounts.txt        # Your private keys (create this)
├── proxy.txt           # Your proxies (optional)
├── requirements.txt    # Python dependencies
└── README.md          # Documentation
```

## 🔧 Dependencies

- `curl-cffi` - HTTP client with browser impersonation
- `eth-account` - Ethereum account management
- `pytz` - Timezone handling
- `colorama` - Colored terminal output

## ⚙️ How It Works

1. **Authentication**: Signs in using your Ethereum wallet private key
2. **CSRF Protection**: Retrieves and uses CSRF tokens for secure requests
3. **Message Signing**: Creates and signs SIWE (Sign-In with Ethereum) messages
4. **Task Claiming**: Automatically claims available daily tasks
5. **Cycle Management**: Runs continuously with 24-hour intervals

## 🛡️ Security Tips

- Store private keys securely
- Use dedicated wallets for automation
- Enable 2FA on your GitHub account
- Add `accounts.txt` and `proxy.txt` to `.gitignore`
- Never commit sensitive information to the repository

## ⚠️ Disclaimer

This bot is for educational purposes only. Use at your own risk. The developers are not responsible for any losses or damages caused by using this bot. Always comply with the platform's terms of service.

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the [issues page](https://github.com/febriyan9346/Veera-Auto-Bot/issues).

## 👨‍💻 Developer

**FEBRIYAN**

## 📞 Support

If you encounter any issues or have questions, please open an issue on GitHub.

---

## 💰 Support Us with Cryptocurrency

You can make a contribution using any of the following blockchain networks:

| Network | Wallet Address |
|---------|---------------|
| **EVM** | `0x216e9b3a5428543c31e659eb8fea3b4bf770bdfd` |
| **TON** | `UQCEzXLDalfKKySAHuCtBZBARCYnMc0QsTYwN4qda3fE6tto` |
| **SOL** | `9XgbPg8fndBquuYXkGpNYKHHhymdmVhmF6nMkPxhXTki` |
| **SUI** | `0x8c3632ddd46c984571bf28f784f7c7aeca3b8371f146c4024f01add025f993bf` |

---

⭐ If you find this project useful, please consider giving it a star!
