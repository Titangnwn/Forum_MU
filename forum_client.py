import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, simpledialog
import socket
import threading
import json
from datetime import datetime
import psutil

class ForumClient:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🏆 Manchester United Fans Forum - Client")
        self.root.geometry("900x700")
        self.root.configure(bg="#1a1a1a")  # Dark gray background for modern look
        
        # Modern styling
        self.style = ttk.Style()
        self.style.theme_use('clam')  # Use clam theme for modern look
        self.style.configure('TLabelFrame', background='#1a1a1a', foreground='white', borderwidth=2, relief='solid')
        self.style.configure('TButton', background='#DA020E', foreground='white', font=('Segoe UI', 9, 'bold'), borderwidth=0, focusthickness=0)
        self.style.map('TButton', background=[('active', '#B00000')])  # Darker red on hover
        self.style.configure('Treeview', background='#333333', foreground='white', fieldbackground='#333333', borderwidth=0)
        self.style.configure('Treeview.Heading', background='#DA020E', foreground='white', font=('Segoe UI', 9, 'bold'))
        
        self.client = None
        self.connected = False
        self.username = ""
        self.club = "Manchester United"
        self.news = []
        
        self.setup_ui()
        self.update_system_info()
    
    def setup_ui(self):
        # Header with gradient effect
        header_frame = tk.Frame(self.root, bg="#DA020E", height=70)
        header_frame.pack(fill=tk.X, pady=(0,10))
        header_frame.pack_propagate(False)
        
        # Inner frame for gradient simulation
        inner_header = tk.Frame(header_frame, bg="#B00000")
        inner_header.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
        
        header_label = tk.Label(inner_header, text="🏆 MANCHESTER UNITED FAN FORUM 🏆", 
                               font=("Segoe UI", 18, "bold"), fg="white", bg="#B00000")
        header_label.pack(expand=True)
        
        # Connection frame with modern styling
        conn_frame = tk.LabelFrame(self.root, text="🔗 Connection Panel", bg="#1a1a1a", fg="white", 
                                  font=("Segoe UI", 10, "bold"), borderwidth=2, relief='solid')
        conn_frame.pack(fill=tk.X, padx=15, pady=5)
        
        # Server info
        server_frame = tk.Frame(conn_frame)
        server_frame.pack(fill=tk.X, padx=5, pady=2)
        
        tk.Label(server_frame, text="Server:").pack(side=tk.LEFT)
        self.server_entry = tk.Entry(server_frame, width=15)
        self.server_entry.pack(side=tk.LEFT, padx=5)
        self.server_entry.insert(0, "127.0.0.1")
        
        tk.Label(server_frame, text="Your Name:").pack(side=tk.LEFT, padx=(10,0))
        self.username_entry = tk.Entry(server_frame, width=20)
        self.username_entry.pack(side=tk.LEFT, padx=5)
        
        tk.Label(server_frame, text="🔴 Manchester United Fan Forum", font=("Segoe UI", 10, "bold"), fg="#DA020E", bg="#1a1a1a").pack(side=tk.LEFT, padx=10)
        
        self.connect_btn = ttk.Button(server_frame, text="🔗 Connect", command=self.toggle_connection, style='TButton')
        self.connect_btn.pack(side=tk.LEFT, padx=10)
        
        self.status_label = tk.Label(server_frame, text="❌ Disconnected", fg="#FF6B6B", bg="#1a1a1a", font=("Segoe UI", 9, "bold"))
        self.status_label.pack(side=tk.LEFT, padx=5)
        
        # Main content with modern panels
        main_frame = tk.Frame(self.root, bg="#1a1a1a")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=5)
        
        # Left panel - News with modern styling
        left_frame = tk.LabelFrame(main_frame, text="📰 Manchester United News Feed", bg="#1a1a1a", fg="white", 
                                  font=("Segoe UI", 10, "bold"), borderwidth=2, relief='solid')
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0,8))
        
        # News refresh with modern button
        filter_frame = tk.Frame(left_frame, bg="#1a1a1a")
        filter_frame.pack(fill=tk.X, padx=8, pady=5)
        
        tk.Label(filter_frame, text="Latest MU News:", font=("Segoe UI", 9, "bold"), fg="#DA020E", bg="#1a1a1a").pack(side=tk.LEFT)
        ttk.Button(filter_frame, text="🔄 Refresh", command=self.request_news, style='TButton').pack(side=tk.RIGHT, padx=5)
        
        # News list with modern Treeview
        self.news_tree = ttk.Treeview(left_frame, columns=("Title", "Time"), show="headings", height=14, style='Treeview')
        self.news_tree.heading("Title", text="📄 Title")
        self.news_tree.heading("Time", text="🕒 Time")
        
        self.news_tree.column("Title", width=350)
        self.news_tree.column("Time", width=130)
        
        news_scroll = ttk.Scrollbar(left_frame, orient=tk.VERTICAL, command=self.news_tree.yview)
        self.news_tree.configure(yscrollcommand=news_scroll.set)
        
        self.news_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=8, pady=5)
        news_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.news_tree.bind("<Double-1>", self.show_news_detail)
        
        # Right panel - Chat with modern styling
        right_frame = tk.LabelFrame(main_frame, text="💬 Red Devils Discussion Hub", bg="#1a1a1a", fg="white", 
                                   font=("Segoe UI", 10, "bold"), borderwidth=2, relief='solid')
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(8,0))
        
        # Online users with modern label
        users_frame = tk.Frame(right_frame, bg="#1a1a1a")
        users_frame.pack(fill=tk.X, padx=8, pady=5)
        
        tk.Label(users_frame, text="👥 Online Fans:", font=("Segoe UI", 9, "bold"), fg="#1E90FF", bg="#1a1a1a").pack(side=tk.LEFT)
        self.users_label = tk.Label(users_frame, text="", font=("Segoe UI", 8), fg="white", bg="#1a1a1a")
        self.users_label.pack(side=tk.LEFT, padx=5)
        
        # Chat messages with modern styling
        self.chat_area = scrolledtext.ScrolledText(right_frame, height=15, width=45, state=tk.DISABLED, 
                                                  bg="#2a2a2a", fg="white", insertbackground="white", 
                                                  font=("Segoe UI", 9), borderwidth=1, relief='flat')
        self.chat_area.pack(fill=tk.BOTH, expand=True, padx=8, pady=5)
        
        # Configure text tags for different clubs
        self.setup_chat_tags()
        
        # Message input with modern styling
        input_frame = tk.Frame(right_frame, bg="#1a1a1a")
        input_frame.pack(fill=tk.X, padx=8, pady=5)
        
        self.message_entry = tk.Entry(input_frame, bg="#404040", fg="white", insertbackground="white", 
                                     font=("Segoe UI", 9), borderwidth=1, relief='flat')
        self.message_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0,8))
        self.message_entry.bind("<Return>", lambda e: self.send_message())
        
        self.send_btn = ttk.Button(input_frame, text="📤 Send", command=self.send_message, state=tk.DISABLED, style='TButton')
        self.send_btn.pack(side=tk.RIGHT)
        
        # System info
        self.sys_label = tk.Label(self.root, text="", font=("Arial", 8))
        self.sys_label.pack(pady=2)
    
    def setup_chat_tags(self):
        """Setup color tags for Manchester United theme"""
        self.chat_area.tag_config("user", foreground="#DA020E", font=("Arial", 9, "bold"))
        self.chat_area.tag_config("system", foreground="gray", font=("Arial", 8, "italic"))
        self.chat_area.tag_config("timestamp", foreground="gray", font=("Arial", 8))
    
    def toggle_connection(self):
        if self.connected:
            self.disconnect()
        else:
            self.connect()
    
    def connect(self):
        username = self.username_entry.get().strip()
        server_ip = self.server_entry.get().strip()
        
        if not username:
            messagebox.showwarning("Warning", "Please enter your name")
            return
        
        try:
            self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client.settimeout(5)
            self.client.connect((server_ip, 5556))
            self.client.settimeout(None)
            
            self.username = username
            self.connected = True
            
            # Update UI
            self.connect_btn.config(text="Disconnect")
            self.status_label.config(text=f"Connected as {username} 🔴", fg="green")
            self.send_btn.config(state=tk.NORMAL)
            
            # Start receiving thread
            thread = threading.Thread(target=self.receive_messages, daemon=True)
            thread.start()
            
            self.add_chat_message("🔴 Connected to Manchester United Forum!", "system")
            
            # Request initial news after a short delay
            self.root.after(1000, self.request_news)
            
        except Exception as e:
            messagebox.showerror("Error", f"Connection failed: {e}")
    
    def disconnect(self):
        if self.client:
            try:
                self.client.close()
            except:
                pass
        
        self.connected = False
        self.connect_btn.config(text="Connect")
        self.status_label.config(text="Disconnected", fg="red")
        self.send_btn.config(state=tk.DISABLED)
        self.add_chat_message("Disconnected from forum", "system")
    
    def receive_messages(self):
        buffer = ""
        while self.connected:
            try:
                data = self.client.recv(1024).decode()
                if not data:
                    break
                
                buffer += data
                while "\n" in buffer:
                    line, buffer = buffer.split("\n", 1)
                    if line.strip():
                        try:
                            message = json.loads(line.strip())
                            self.handle_message(message)
                        except json.JSONDecodeError:
                            continue
            
            except Exception as e:
                if self.connected:
                    self.add_chat_message(f"Connection error: {e}", "system")
                break
        
        if self.connected:
            self.disconnect()
    
    def handle_message(self, message):
        msg_type = message.get("type")
        
        if msg_type == "request_info":
            # Send user info to server
            user_info = {
                "username": self.username
            }
            self.client.sendall(json.dumps(user_info).encode() + b"\n")
        
        elif msg_type == "news_list" or msg_type == "news_update":
            self.news = message.get("news", [])
            print(f"DEBUG: Received {len(self.news)} news items from server")
            for i, news in enumerate(self.news):
                print(f"DEBUG: News {i+1}: {news.get('title', 'No title')}")
            
            # Update in main thread
            self.root.after(0, self.update_news_display)
            
            news_count = len(self.news)
            if news_count > 0:
                self.add_chat_message(f"📰 Loaded {news_count} Manchester United news", "system")
            else:
                self.add_chat_message("📭 No news available", "system")
        
        elif msg_type == "chat":
            username = message["username"]
            text = message["message"]
            time = message["time"]
            self.add_chat_message(f"[{time}] {username}: {text}", "user")
        
        elif msg_type == "user_joined":
            username = message["username"]
            self.add_chat_message(f"🔴 {username} joined the Red Devils forum", "system")
        
        elif msg_type == "user_left":
            username = message["username"]
            self.add_chat_message(f"⚪ {username} left the forum", "system")
    
    def send_message(self):
        if not self.connected:
            return
        
        text = self.message_entry.get().strip()
        if not text:
            return
        
        message = {
            "type": "chat",
            "message": text
        }
        
        try:
            self.client.sendall(json.dumps(message).encode() + b"\n")
            self.message_entry.delete(0, tk.END)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to send message: {e}")
    
    def add_chat_message(self, text, tag=""):
        self.chat_area.config(state=tk.NORMAL)
        self.chat_area.insert(tk.END, text + "\n", tag)
        self.chat_area.config(state=tk.DISABLED)
        self.chat_area.see(tk.END)
    
    def update_news_display(self):
        try:
            print(f"DEBUG: Updating news display with {len(self.news)} items")
            
            # Clear existing items
            for item in self.news_tree.get_children():
                self.news_tree.delete(item)
                
            # Add all Manchester United news
            for i, news in enumerate(self.news):
                title = news.get("title", "No Title")
                time = news.get("time", "No Time")
                print(f"DEBUG: Adding news {i+1}: {title}")
                self.news_tree.insert("", tk.END, values=(title, time))
                
            # Force refresh
            self.news_tree.update()
            
            print(f"DEBUG: News tree now has {len(self.news_tree.get_children())} items")
            
        except Exception as e:
            print(f"ERROR in update_news_display: {e}")
            self.add_chat_message(f"❌ Error displaying news: {e}", "system")
    

    
    def request_news(self):
        if self.connected:
            try:
                request = {"type": "request_news"}
                self.client.sendall(json.dumps(request).encode() + b"\n")
                print("DEBUG: Sent news request to server")
                self.add_chat_message("🔄 Requesting Manchester United news...", "system")
            except Exception as e:
                print(f"ERROR requesting news: {e}")
                self.add_chat_message(f"❌ Failed to request news: {e}", "system")
        else:
            messagebox.showwarning("Warning", "Not connected to server")
    
    def show_news_detail(self, event):
        selected = self.news_tree.selection()
        if not selected:
            return
        
        item = self.news_tree.item(selected[0])
        title = item["values"][0]
        
        # Find news by title
        news_item = next((n for n in self.news if n["title"] == title), None)
        if news_item:
            NewsDetailDialog(self.root, news_item)
    
    def update_system_info(self):
        cpu = psutil.cpu_percent()
        memory = psutil.virtual_memory().percent
        
        # Network info
        try:
            network = psutil.net_io_counters()
            net_sent = network.bytes_sent // 1024  # KB
            net_recv = network.bytes_recv // 1024  # KB
            
            # Disk usage
            disk = psutil.disk_usage('/')
            disk_percent = (disk.used / disk.total) * 100
            
            self.sys_label.config(text=f"💻 CPU: {cpu}% | 🧠 RAM: {memory:.1f}% | 💾 Disk: {disk_percent:.1f}% | 🌐 Net: ↑{net_sent}KB ↓{net_recv}KB")
        except:
            self.sys_label.config(text=f"💻 CPU: {cpu}% | 🧠 RAM: {memory:.1f}%")
        
        self.root.after(2000, self.update_system_info)
    
    def run(self):
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()
    
    def on_closing(self):
        if self.connected:
            self.disconnect()
        self.root.destroy()

class NewsDetailDialog:
    def __init__(self, parent, news_data):
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("📰 News Detail - Manchester United")
        self.dialog.geometry("600x500")
        self.dialog.configure(bg="#1a1a1a")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Title with modern styling
        title_frame = tk.Frame(self.dialog, bg="#DA020E", height=50)
        title_frame.pack(fill=tk.X, pady=(0,10))
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(title_frame, text=news_data["title"], font=("Segoe UI", 16, "bold"), 
                              fg="white", bg="#DA020E", wraplength=550)
        title_label.pack(expand=True)
        
        # Info with modern layout
        info_frame = tk.Frame(self.dialog, bg="#1a1a1a")
        info_frame.pack(fill=tk.X, padx=15, pady=5)
        
        tk.Label(info_frame, text=f"🏆 Club: {news_data['club']}", font=("Segoe UI", 10, "bold"), 
                fg="#DA020E", bg="#1a1a1a").pack(side=tk.LEFT)
        tk.Label(info_frame, text=f"🕒 Time: {news_data['time']}", font=("Segoe UI", 10), 
                fg="#1E90FF", bg="#1a1a1a").pack(side=tk.RIGHT)
        
        # Content with modern text area
        content_frame = tk.LabelFrame(self.dialog, text="📝 Content", bg="#1a1a1a", fg="white", 
                                     font=("Segoe UI", 10, "bold"), borderwidth=2, relief='solid')
        content_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)
        
        content_text = scrolledtext.ScrolledText(content_frame, wrap=tk.WORD, state=tk.DISABLED, 
                                                bg="#2a2a2a", fg="white", insertbackground="white", 
                                                font=("Segoe UI", 10), borderwidth=1, relief='flat')
        content_text.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)
        
        content_text.config(state=tk.NORMAL)
        content_text.insert(tk.END, news_data["content"])
        content_text.config(state=tk.DISABLED)
        
        # Close button with modern styling
        ttk.Button(self.dialog, text="❌ Close", command=self.dialog.destroy, style='TButton').pack(pady=15)

if __name__ == "__main__":
    app = ForumClient()
    app.run()