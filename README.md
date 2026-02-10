# 🏆 Manchester United Fan Forum

Aplikasi forum diskusi berbasis client-server untuk fans Manchester United dengan fitur real-time chat dan news broadcasting.

![Python](https://img.shields.io/badge/Python-3.x-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Network](https://img.shields.io/badge/Network-TCP%2FIP-red)

## 📋 Deskripsi

Manchester United Fan Forum adalah aplikasi desktop yang memungkinkan fans untuk:
- 💬 Chat real-time dengan fans lain
- 📰 Membaca berita terkini Manchester United
- 🔄 Menerima update otomatis dari server
- 👥 Melihat siapa yang sedang online

## ✨ Fitur

### Server
- News management (add, edit, delete)
- Auto broadcasting ke semua client
- Multi-client connection handling
- Activity logging
- System monitoring (CPU, RAM)

### Client
- Real-time chat room
- News feed dengan detail view
- Connection management
- Modern UI dengan tema Manchester United
- System monitoring

## 🛠️ Teknologi

- **Python 3.x**
- **Socket Programming** (TCP/IP)
- **Tkinter** (GUI)
- **Threading** (Concurrent connections)
- **JSON** (Data protocol)
- **psutil** (System monitoring)

## 📦 Instalasi

1. Clone repository:
```bash
git clone https://github.com/[username]/manchester-united-forum.git
cd manchester-united-forum
```

2. Install dependencies:
```bash
pip install psutil
```

## 🚀 Cara Menggunakan

### Menjalankan Server

```bash
python forum_server.py
```

1. Klik tombol **"Start Server"**
2. Server akan berjalan di port **5556**
3. Tambahkan berita melalui form News Management
4. Monitor aktivitas di Activity Logs

### Menjalankan Client

```bash
python forum_client.py
```

1. Masukkan **Server IP** (default: 127.0.0.1 untuk localhost)
2. Masukkan **Username** Anda
3. Klik **"Connect"**
4. Mulai chat dan baca berita!

## 📸 Screenshots

### Server Interface
![Server](screenshots/server.png)

### Client Interface
![Client](screenshots/client.png)

## 🔧 Konfigurasi

- **Port**: 5556 (dapat diubah di source code)
- **Max Connections**: 10 concurrent clients
- **Buffer Size**: 1024 bytes
- **Protocol**: JSON over TCP/IP

## 📁 Struktur File

```
manchester-united-forum/
├── forum_server.py          # Server application
├── forum_client.py          # Client application
├── flowchart client.png     # Client flowchart
├── flowchartserver.png      # Server flowchart
├── README.md                # Documentation
├── WORKFLOW_DETAIL.txt      # Detailed workflow
├── DOKUMEN_DESAIN.txt       # Design document
└── requirements.txt         # Dependencies
```

## 🌐 Network Protocol

### Message Types
- `request_info` - Server request user info
- `news_list` - Server send news list
- `news_update` - Server broadcast news update
- `chat` - Chat message
- `user_joined` - User join notification
- `user_left` - User leave notification

### Message Format
```json
{
  "type": "chat",
  "username": "John",
  "message": "Glory Glory Man United!",
  "time": "14:30:25"
}
```

## 🧪 Testing

Tested with:
- ✅ 10+ concurrent clients
- ✅ Multiple news broadcasts
- ✅ Long-running sessions (2+ hours)
- ✅ Disconnect/reconnect scenarios
- ✅ Server restart scenarios

## 📝 Requirements

```
Python >= 3.6
psutil >= 5.8.0
tkinter (included in Python)
```

## 🤝 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

M Farizal T G
- NPM: 714240043
- 
- 

## 🙏 Acknowledgments

- Tugas Besar Network Programming 2025
- Dosen Pengampu: M. Yusril Helmi Setyawan, S.Kom., M.Kom.,SFPC.
- Manchester United Football Club


---

⭐ **Glory Glory Man United!** ⭐
