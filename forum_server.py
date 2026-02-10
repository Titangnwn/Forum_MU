import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, simpledialog
import socket
import threading
import json
from datetime import datetime
import psutil

class ForumServer:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🏆 Manchester United Forum - Server")
        self.root.geometry("950x750")
        self.root.configure(bg="#1a1a1a")  # Modern dark gray background
        
        # Modern styling
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure('TLabelFrame', background='#1a1a1a', foreground='white', borderwidth=2, relief='solid')
        self.style.configure('TButton', background='#DA020E', foreground='white', font=('Segoe UI', 9, 'bold'), borderwidth=0, focusthickness=0)
        self.style.map('TButton', background=[('active', '#B00000')])
        self.style.configure('Treeview', background='#333333', foreground='white', fieldbackground='#333333', borderwidth=0)
        self.style.configure('Treeview.Heading', background='#DA020E', foreground='white', font=('Segoe UI', 9, 'bold'))
        
        self.server = None
        self.running = False
        self.clients = {}  # {socket: {"username": str}}
        self.news = []  # List berita
        self.messages = []  # List pesan diskusi
        
        self.setup_ui()
        self.update_news_display()  # Start with empty news list
        
    def setup_ui(self):
        # Header with gradient effect
        header_frame = tk.Frame(self.root, bg="#DA020E", height=70)
        header_frame.pack(fill=tk.X, pady=(0,10))
        header_frame.pack_propagate(False)
        
        inner_header = tk.Frame(header_frame, bg="#B00000")
        inner_header.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
        
        header_label = tk.Label(inner_header, text="🏆 MANCHESTER UNITED FORUM SERVER 🏆", 
                               font=("Segoe UI", 18, "bold"), fg="white", bg="#B00000")
        header_label.pack(expand=True)
        
        # Server control with modern styling
        control_frame = tk.Frame(self.root, bg="#1a1a1a")
        control_frame.pack(pady=5)
        
        self.start_btn = ttk.Button(control_frame, text="🚀 Start Server", command=self.toggle_server, style='TButton')
        self.start_btn.pack(side=tk.LEFT, padx=5)
        
        self.status_label = tk.Label(control_frame, text="❌ Status: Stopped", fg="#FF6B6B", bg="#1a1a1a", font=("Segoe UI", 9, "bold"))
        self.status_label.pack(side=tk.LEFT, padx=10)
        
        # News management with modern styling
        news_frame = tk.LabelFrame(self.root, text="📰 News Management Dashboard", bg="#1a1a1a", fg="white", 
                                  font=("Segoe UI", 10, "bold"), borderwidth=2, relief='solid')
        news_frame.pack(padx=15, pady=5, fill=tk.BOTH, expand=True)
        
        # News input form
        input_frame = tk.Frame(news_frame)
        input_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Title input with modern styling
        tk.Label(input_frame, text="📰 News Title:", fg="white", bg="#1a1a1a", font=("Segoe UI", 9)).pack(anchor=tk.W)
        self.title_entry = tk.Entry(input_frame, width=70, bg="#404040", fg="white", insertbackground="white", 
                                   font=("Segoe UI", 9), borderwidth=1, relief='flat')
        self.title_entry.pack(fill=tk.X, pady=2)
        
        # Content input with modern styling
        tk.Label(input_frame, text="📝 News Content:", fg="white", bg="#1a1a1a", font=("Segoe UI", 9)).pack(anchor=tk.W)
        self.content_text = scrolledtext.ScrolledText(input_frame, height=5, width=70, bg="#404040", fg="white", 
                                                     insertbackground="white", font=("Segoe UI", 9), 
                                                     borderwidth=1, relief='flat')
        self.content_text.pack(fill=tk.X, pady=2)
        
        # Buttons with modern styling
        btn_frame = tk.Frame(input_frame, bg="#1a1a1a")
        btn_frame.pack(fill=tk.X, pady=8)
        
        ttk.Button(btn_frame, text="📰 Add News", command=self.add_news, style='TButton').pack(side=tk.LEFT, padx=3)
        ttk.Button(btn_frame, text="✏️ Edit Selected", command=self.edit_news).pack(side=tk.LEFT, padx=3)
        ttk.Button(btn_frame, text="🗑️ Delete Selected", command=self.delete_news).pack(side=tk.LEFT, padx=3)
        ttk.Button(btn_frame, text="📡 Broadcast All", command=self.broadcast_news, style='TButton').pack(side=tk.LEFT, padx=3)
        tk.Button(btn_frame, text="🔄 Clear Form", command=self.clear_form).pack(side=tk.LEFT, padx=2)
        
        # News list
        self.news_tree = ttk.Treeview(news_frame, columns=("ID", "Title", "Time"), show="headings", height=8)
        self.news_tree.heading("ID", text="ID")
        self.news_tree.heading("Title", text="Title")
        self.news_tree.heading("Time", text="Time")
        
        self.news_tree.column("ID", width=50)
        self.news_tree.column("Title", width=400)
        self.news_tree.column("Time", width=150)
        
        scrollbar_news = ttk.Scrollbar(news_frame, orient=tk.VERTICAL, command=self.news_tree.yview)
        self.news_tree.configure(yscrollcommand=scrollbar_news.set)
        
        self.news_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        scrollbar_news.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Logs and clients with modern layout
        bottom_frame = tk.Frame(self.root, bg="#1a1a1a")
        bottom_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=5)
        
        # Server logs with modern styling
        logs_frame = tk.LabelFrame(bottom_frame, text="📋 Server Activity Logs", bg="#1a1a1a", fg="white", 
                                  font=("Segoe UI", 10, "bold"), borderwidth=2, relief='solid')
        logs_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0,8))
        
        self.logs = scrolledtext.ScrolledText(logs_frame, height=12, width=55, bg="#2a2a2a", fg="white", 
                                             insertbackground="white", font=("Segoe UI", 9), 
                                             borderwidth=1, relief='flat')
        self.logs.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)
        
        # Connected clients with modern styling
        clients_frame = tk.LabelFrame(bottom_frame, text="👥 Connected Fans", bg="#1a1a1a", fg="white", 
                                     font=("Segoe UI", 10, "bold"), borderwidth=2, relief='solid')
        clients_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=(8,0))
        
        self.clients_tree = ttk.Treeview(clients_frame, columns=("Username",), show="headings", height=12, style='Treeview')
        self.clients_tree.heading("Username", text="👤 Username")
        self.clients_tree.column("Username", width=160)
        self.clients_tree.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)
        
        # System info with modern styling
        self.sys_label = tk.Label(self.root, text="", font=("Segoe UI", 8), fg="white", bg="#1a1a1a")
        self.sys_label.pack(pady=5)
        
        self.update_system_info()
    

    
    def toggle_server(self):
        if self.running:
            self.stop_server()
        else:
            self.start_server()
    
    def start_server(self):
        try:
            self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server.bind(("0.0.0.0", 5556))
            self.server.listen(10)
            
            self.running = True
            self.start_btn.config(text="Stop Server")
            self.status_label.config(text="Status: Running", fg="green")
            self.add_log("[SERVER] Forum server started on port 5556")
            
            thread = threading.Thread(target=self.accept_clients, daemon=True)
            thread.start()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to start server: {e}")
    
    def stop_server(self):
        self.running = False
        if self.server:
            self.server.close()
        
        for client in list(self.clients.keys()):
            client.close()
        self.clients.clear()
        
        self.start_btn.config(text="Start Server")
        self.status_label.config(text="Status: Stopped", fg="red")
        self.add_log("[SERVER] Forum server stopped")
        self.update_clients_display()
    
    def accept_clients(self):
        while self.running:
            try:
                conn, addr = self.server.accept()
                thread = threading.Thread(target=self.handle_client, args=(conn, addr), daemon=True)
                thread.start()
            except:
                break
    
    def handle_client(self, conn, addr):
        try:
            # Request username and club
            conn.sendall(json.dumps({"type": "request_info"}).encode() + b"\n")
            
            data = conn.recv(1024).decode().strip()
            client_info = json.loads(data)
            
            username = client_info["username"]
            
            self.clients[conn] = {"username": username}
            self.add_log(f"[CONNECTED] {username} from {addr}")
            self.update_clients_display()
            
            # Send initial data
            self.send_news_to_client(conn)
            self.send_messages_to_client(conn)
            
            # Log what was sent
            self.add_log(f"[SENT] {len(self.news)} news items to {username}")
            
            # Broadcast new user joined
            self.broadcast_message({
                "type": "user_joined",
                "username": username,
                "time": datetime.now().strftime("%H:%M:%S")
            }, exclude=conn)
            
            while self.running:
                data = conn.recv(1024).decode().strip()
                if not data:
                    break
                
                try:
                    message = json.loads(data)
                    self.handle_message(conn, message)
                except json.JSONDecodeError:
                    continue
        
        except Exception as e:
            self.add_log(f"[ERROR] {addr}: {e}")
        
        finally:
            if conn in self.clients:
                user_info = self.clients[conn]
                self.add_log(f"[DISCONNECTED] {user_info['username']}")
                
                # Broadcast user left
                self.broadcast_message({
                    "type": "user_left",
                    "username": user_info['username'],
                    "time": datetime.now().strftime("%H:%M:%S")
                }, exclude=conn)
                
                del self.clients[conn]
                self.update_clients_display()
            
            conn.close()
    
    def handle_message(self, conn, message):
        if message["type"] == "chat":
            user_info = self.clients[conn]
            chat_msg = {
                "type": "chat",
                "username": user_info["username"],
                "message": message["message"],
                "time": datetime.now().strftime("%H:%M:%S")
            }
            
            self.messages.append(chat_msg)
            self.broadcast_message(chat_msg)
            self.add_log(f"[CHAT] {user_info['username']}: {message['message']}")
        
        elif message["type"] == "request_news":
            # Client meminta berita terbaru
            self.send_news_to_client(conn)
            user_info = self.clients[conn]
            self.add_log(f"[REQUEST] {user_info['username']} requested news update")
    
    def broadcast_message(self, message, exclude=None):
        data = json.dumps(message).encode() + b"\n"
        disconnected = []
        
        for client in self.clients:
            if client != exclude:
                try:
                    client.sendall(data)
                except:
                    disconnected.append(client)
        
        for client in disconnected:
            if client in self.clients:
                del self.clients[client]
        
        if disconnected:
            self.update_clients_display()
    
    def send_news_to_client(self, conn):
        try:
            news_data = {"type": "news_list", "news": self.news}
            conn.sendall(json.dumps(news_data).encode() + b"\n")
            self.add_log(f"[SEND NEWS] Sent {len(self.news)} news items to client")
        except Exception as e:
            self.add_log(f"[ERROR] Failed to send news: {e}")
    
    def send_messages_to_client(self, conn):
        try:
            for msg in self.messages[-20:]:  # Send last 20 messages
                conn.sendall(json.dumps(msg).encode() + b"\n")
        except:
            pass
    
    def add_news(self):
        title = self.title_entry.get().strip()
        content = self.content_text.get(1.0, tk.END).strip()
        
        if not title or not content:
            messagebox.showwarning("Warning", "Please enter both title and content")
            return
        
        news_id = max([n["id"] for n in self.news], default=0) + 1
        new_news = {
            "id": news_id,
            "title": title,
            "content": content,
            "club": "Manchester United",
            "time": datetime.now().strftime("%Y-%m-%d %H:%M")
        }
        
        self.news.append(new_news)
        self.update_news_display()
        self.clear_form()
        self.add_log(f"[NEWS] Added: {title}")
        
        # Auto broadcast new news to all clients
        news_data = {"type": "news_update", "news": self.news}
        self.broadcast_message(news_data)
        self.add_log(f"[AUTO BROADCAST] New news sent to all clients")
    
    def edit_news(self):
        selected = self.news_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Select news to edit")
            return
        
        item = self.news_tree.item(selected[0])
        news_id = int(item["values"][0])
        
        news_item = next((n for n in self.news if n["id"] == news_id), None)
        if news_item:
            # Fill form with selected news
            self.title_entry.delete(0, tk.END)
            self.title_entry.insert(0, news_item["title"])
            
            self.content_text.delete(1.0, tk.END)
            self.content_text.insert(1.0, news_item["content"])
            
            # Remove old news and let user add updated version
            self.news.remove(news_item)
            self.update_news_display()
            self.add_log(f"[NEWS] Loaded for editing: {news_item['title']}")
    
    def delete_news(self):
        selected = self.news_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Select news to delete")
            return
        
        if messagebox.askyesno("Confirm", "Delete selected news?"):
            item = self.news_tree.item(selected[0])
            news_id = int(item["values"][0])
            
            self.news = [n for n in self.news if n["id"] != news_id]
            self.update_news_display()
            self.add_log(f"[NEWS] Deleted news ID: {news_id}")
    
    def broadcast_news(self):
        if not self.news:
            messagebox.showinfo("Info", "No news to broadcast")
            return
            
        news_data = {"type": "news_update", "news": self.news}
        self.broadcast_message(news_data)
        self.add_log(f"[MANUAL BROADCAST] {len(self.news)} news items sent to {len(self.clients)} clients")
    
    def update_news_display(self):
        for item in self.news_tree.get_children():
            self.news_tree.delete(item)
        
        for news in self.news:
            self.news_tree.insert("", tk.END, values=(news["id"], news["title"], news["time"]))
    
    def update_clients_display(self):
        for item in self.clients_tree.get_children():
            self.clients_tree.delete(item)
        
        for client_info in self.clients.values():
            self.clients_tree.insert("", tk.END, values=(client_info["username"],))
    
    def add_log(self, message):
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.logs.insert(tk.END, f"[{timestamp}] {message}\n")
        self.logs.see(tk.END)
    
    def update_system_info(self):
        cpu = psutil.cpu_percent()
        memory = psutil.virtual_memory().percent
        clients_count = len(self.clients)
        self.sys_label.config(text=f"CPU: {cpu}% | RAM: {memory}% | Clients: {clients_count}")
        self.root.after(2000, self.update_system_info)
    
    def run(self):
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()
    
    def on_closing(self):
        if self.running:
            self.stop_server()
        self.root.destroy()

    def clear_form(self):
        """Clear the news input form"""
        self.title_entry.delete(0, tk.END)
        self.content_text.delete(1.0, tk.END)
        self.add_log("[FORM] Input form cleared")

if __name__ == "__main__":
    app = ForumServer()
    app.run()