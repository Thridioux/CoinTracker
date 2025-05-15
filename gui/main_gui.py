import tkinter as tk
from tkinter import ttk, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
import numpy as np
from datetime import datetime, timezone
import pytz
from price_fetcher import PriceFetcher
from db import DatabaseManager
from utils.utils import Utils

class ThemeManager:
    def __init__(self):
        # Sadece light tema kullan
        self.colors = {
            "bg": "#ffffff",
            "fg": "#000000",
            "accent": "#1a73e8",
            "graph_bg": "#ffffff",
            "button_bg": "#f0f0f0",
            "hover_bg": "#e0e0e0",
            "selected_bg": "#1a73e8",
            "selected_fg": "#ffffff",
            "border": "#e0e0e0"
        }
    
    def get_colors(self):
        return self.colors

class CoinTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("CoinTracker")
        self.root.geometry("800x900")
        
        # Initialize theme manager
        self.theme_manager = ThemeManager()
        self.setup_styles()
        
        # Initialize default token and fetcher
        self.fetcher = PriceFetcher("BTC")
        self.db = DatabaseManager()

        # Initialize variables with defaults
        self.selected_token = tk.StringVar(value="Bitcoin")
        self.time_range = tk.StringVar(value="24h")
        self.price_var = tk.StringVar()
        
        # Initialize graph-related attributes
        self.canvas = None
        self.fig = None
        self.ax = None
        
        # Auto-refresh control
        self.auto_refresh = True
        self.refresh_interval = 60000  # 60 seconds in milliseconds
        
        # Create main container frame
        self.main_container = ttk.Frame(root)
        self.main_container.pack(fill=tk.BOTH, expand=True)
        
        # Show initial screen
        self.show_welcome_screen()
        
        # Klavye kısayolları kaldırıldı

    def setup_styles(self):
        colors = self.theme_manager.get_colors()
        style = ttk.Style()
        style.theme_use('default')
        
        # Configure common styles
        style.configure("TFrame", background=colors["bg"])
        style.configure("TLabel", 
                       background=colors["bg"], 
                       foreground=colors["fg"])
        style.configure("TButton",
                       background=colors["button_bg"],
                       foreground=colors["fg"],
                       padding=(10, 5))
        
        # Configure custom button style
        style.configure("Accent.TButton",
                       background=colors["accent"],
                       foreground=colors["selected_fg"])
        
        # Configure custom frame style
        style.configure("Card.TFrame",
                       background=colors["bg"],
                       borderwidth=1,
                       relief="solid")

        # Reapplying hover effects with increased contrast
        style.map('TimeRange.TButton',
                 background=[('active', colors["hover_bg"]),
                            ('pressed', colors["accent"])],
                 foreground=[('active', colors["fg"]),
                            ('pressed', 'white')])

        style.map('TimeRange.Selected.TButton',
                 background=[('active', colors["accent"]),
                            ('pressed', colors["accent"]),
                            ('!active', colors["accent"]),
                            ('!pressed', colors["accent"])],
                 foreground=[('active', 'white'),
                            ('pressed', 'white'),
                            ('!active', 'white'),
                            ('!pressed', 'white')])

        # Update root background
        self.root.configure(bg=colors["bg"])

    def schedule_refresh(self):
        """Schedule the next auto-refresh"""
        if self.auto_refresh:
            self.update_dashboard()
            # Schedule next refresh
            self.root.after(self.refresh_interval, self.schedule_refresh)

    def toggle_auto_refresh(self):
        """Toggle auto-refresh on/off"""
        self.auto_refresh = not self.auto_refresh
        if self.auto_refresh:
            self.auto_refresh_btn.configure(text="Auto Refresh: ON")
            self.schedule_refresh()
        else:
            self.auto_refresh_btn.configure(text="Auto Refresh: OFF")

    def clear_main_container(self):
        # Destroy all widgets in main container
        for widget in self.main_container.winfo_children():
            widget.destroy()
            
    def show_welcome_screen(self):
        self.clear_main_container()
        
        # Ana container'ı ortala
        welcome_frame = ttk.Frame(self.main_container)
        welcome_frame.pack(expand=True)
        
        # Logo çerçevesi (canvas ile özel logo çizimi)
        self.logo_canvas = tk.Canvas(welcome_frame, width=120, height=120, 
                              highlightthickness=0, bg=self.theme_manager.get_colors()["bg"])
        self.logo_canvas.pack(pady=20)
        
        # Logo elementlerini oluştur ama görünmez yap
        self.circle = self.logo_canvas.create_oval(60, 60, 60, 60, 
                                                 fill=self.theme_manager.get_colors()["accent"],
                                                 width=0)
        self.bitcoin_symbol = self.logo_canvas.create_text(60, 60, text='₿',
                                                          fill='white', font=('Arial', 1, 'bold'))
        
        # Animasyonu başlat
        self.animate_logo()

    def animate_logo(self, step=0):
        """Logo giriş animasyonu"""
        if step <= 30:  # 30 adımda tamamlansın
            # Daire animasyonu
            size = step * 2  # Her adımda büyüsün
            self.logo_canvas.coords(self.circle, 
                                  60 - size, 60 - size,
                                  60 + size, 60 + size)
            
            # Bitcoin sembolü animasyonu
            font_size = int(step * 2)  # Her adımda büyüsün
            self.logo_canvas.itemconfig(self.bitcoin_symbol,
                                      font=('Arial', font_size, 'bold'))
            
            # Bir sonraki adım için zamanlayıcı
            self.root.after(20, lambda: self.animate_logo(step + 1))
        elif step == 31:  # Animasyon bittikten sonra diğer elementleri göster
            self.show_welcome_content()

    def show_welcome_content(self):
        """Karşılama ekranının diğer elementlerini göster"""
        welcome_frame = self.logo_canvas.master
        
        # Uygulama başlığı (soldan sağa açılma animasyonu)
        title_frame = ttk.Frame(welcome_frame)
        title_frame.pack(pady=10)
        
        title_label = ttk.Label(title_frame, text="", 
                               font=('Arial', 24, 'bold'),
                               foreground=self.theme_manager.get_colors()["fg"])
        title_label.pack()
        
        def animate_title(text="", index=0):
            if index <= len("CoinTracker"):
                title_label.config(text=text + "|")
                self.root.after(100, lambda: animate_title("CoinTracker"[:index+1], index+1))
            else:
                title_label.config(text="CoinTracker")
                show_subtitle()
        
        def show_subtitle():
            subtitle_label = ttk.Label(welcome_frame,
                                     text="Kripto para piyasasını takip etmenin en kolay yolu",
                                     font=('Arial', 12),
                                     foreground=self.theme_manager.get_colors()["fg"])
            subtitle_label.pack(pady=5)
            
            # Stil ayarları
            style = ttk.Style()
            style.configure('Start.TButton', 
                           padding=15, 
                           font=('Arial', 12, 'bold'))
            
            # Başla butonu
            start_button = ttk.Button(welcome_frame,
                                    text="Başla",
                                    style='Start.TButton',
                                    command=self.show_main_dashboard)
            start_button.pack(pady=30)
            
            # Sürüm bilgisi
            version_label = ttk.Label(welcome_frame,
                                    text="v1.0.0",
                                    font=('Arial', 8),
                                    foreground=self.theme_manager.get_colors()["fg"])
            version_label.pack(pady=10)
        
        # Başlık animasyonunu başlat
        animate_title()

    def show_main_dashboard(self):
        self.clear_main_container()
        
        # Varsayılan token'ı ayarla (eğer seçilmemişse)
        if not self.selected_token.get():
            self.selected_token.set(Utils.TOKEN_LIST[0]["name"])
        
        # Header frame (token selection and current price)
        self.header_frame = ttk.Frame(self.main_container)
        self.header_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Metrics frame (price, change, volume)
        self.metrics_frame = ttk.Frame(self.main_container)
        self.metrics_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Time range frame
        self.timerange_frame = ttk.Frame(self.main_container)
        self.timerange_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Graph frame
        self.graph_frame = ttk.Frame(self.main_container)
        self.graph_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Alerts frame
        self.alerts_frame = ttk.LabelFrame(self.main_container, text="Price Alerts")
        self.alerts_frame.pack(fill=tk.X, padx=10, pady=5)
        self.create_alerts_widgets()
        
        # Create header content
        self.create_header_widgets()
        
        # Create time range buttons
        self.create_timerange_widgets()
        
        # Create metrics widgets
        self.create_metrics_widgets()
        
        # Initial dashboard update
        self.update_dashboard()
        
        # Start auto-refresh after dashboard is created
        self.schedule_refresh()

    def create_alerts_widgets(self):
        """Create widgets for price alerts"""
        # Price threshold entry
        threshold_frame = ttk.Frame(self.alerts_frame)
        threshold_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(threshold_frame, text="Alert Price:").pack(side=tk.LEFT, padx=5)
        self.alert_price = ttk.Entry(threshold_frame, width=15)
        self.alert_price.pack(side=tk.LEFT, padx=5)
        
        # Alert condition (above/below)
        self.alert_condition = tk.StringVar(value="above")
        ttk.Radiobutton(threshold_frame, text="Above", variable=self.alert_condition, 
                       value="above").pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(threshold_frame, text="Below", variable=self.alert_condition, 
                       value="below").pack(side=tk.LEFT, padx=5)
        
        # Set alert button
        ttk.Button(threshold_frame, text="Set Alert", 
                  command=self.set_price_alert).pack(side=tk.LEFT, padx=5)
        
        # Active alerts listbox
        self.alerts_listbox = tk.Listbox(self.alerts_frame, height=3)
        self.alerts_listbox.pack(fill=tk.X, padx=5, pady=5)
        
        # Remove alert button
        ttk.Button(self.alerts_frame, text="Remove Selected Alert", 
                  command=self.remove_price_alert).pack(pady=5)
        
        # Initialize alerts list
        if not hasattr(self, 'price_alerts'):
            self.price_alerts = []
            
    def set_price_alert(self):
        """Set a new price alert"""
        try:
            price = float(self.alert_price.get())
            condition = self.alert_condition.get()
            token = self.selected_token.get()
            
            alert = {
                'token': token,
                'price': price,
                'condition': condition
            }
            
            self.price_alerts.append(alert)
            self.alerts_listbox.insert(tk.END, 
                f"{token}: {condition} ${price:,.2f}")
            self.alert_price.delete(0, tk.END)
            
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid price")
            
    def remove_price_alert(self):
        """Remove selected price alert"""
        try:
            selection = self.alerts_listbox.curselection()
            if selection:
                index = selection[0]
                self.alerts_listbox.delete(index)
                self.price_alerts.pop(index)
        except Exception as e:
            messagebox.showerror("Error", f"Could not remove alert: {str(e)}")
            
    def check_price_alerts(self, current_price):
        """Check if any price alerts have been triggered"""
        for alert in self.price_alerts[:]:  # Copy list to allow modification while iterating
            if alert['condition'] == 'above' and current_price > alert['price']:
                self.trigger_alert(alert, current_price)
            elif alert['condition'] == 'below' and current_price < alert['price']:
                self.trigger_alert(alert, current_price)
                
    def trigger_alert(self, alert, current_price):
        """Show alert notification and remove the triggered alert"""
        message = f"Price Alert: {alert['token']} is now ${current_price:,.2f}, " \
                 f"{alert['condition']} your target of ${alert['price']:,.2f}"
        messagebox.showinfo("Price Alert", message)
        
        # Remove triggered alert
        index = self.price_alerts.index(alert)
        self.price_alerts.remove(alert)
        self.alerts_listbox.delete(index)

    def create_header_widgets(self):
        # Token selection on the left
        token_frame = ttk.Frame(self.header_frame)
        token_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        ttk.Label(token_frame, text="Token:", font=("Arial", 12)).pack(side=tk.LEFT, padx=5)
        token_dropdown = ttk.Combobox(
            token_frame,
            textvariable=self.selected_token,
            values=[token["name"] for token in Utils.TOKEN_LIST],
            font=("Arial", 12),
            width=15
        )
        token_dropdown.pack(side=tk.LEFT, padx=5)

        # Auto-refresh toggle button
        self.auto_refresh_btn = ttk.Button(
            self.header_frame,
            text="Auto Refresh: ON",
            command=self.toggle_auto_refresh
        )
        self.auto_refresh_btn.pack(side=tk.RIGHT, padx=5)
        
        # Manual refresh button
        refresh_btn = ttk.Button(
            self.header_frame,
            text="↻",
            command=self.update_dashboard,
            style='Refresh.TButton'
        )
        refresh_btn.pack(side=tk.RIGHT, padx=5)

    def create_timerange_widgets(self):
        """Zaman aralığı seçim butonlarını oluşturur ve stillerini ayarlar."""
        # Time range options (uzun ve anlaşılır etiketlerle)
        time_ranges = [
            ("1 Saat", "1h"),
            ("24 Saat", "24h"),
            ("1 Ay", "1m"),
            ("3 Ay", "3m"),
            ("6 Ay", "6m"),
            ("1 Yıl", "1y")
        ]

        # Buton çerçevesi için arka plan ve kenar düzenlemeleri
        frame_style = ttk.Style()
        frame_style.configure("ButtonFrame.TFrame", 
                            background=self.theme_manager.get_colors()["bg"])
        
        colors = self.theme_manager.get_colors()
                            
        # Normal butonlar için stil tanımları
        style = ttk.Style()
        style.configure('TimeRange.TButton', 
                       padding=(5, 3),
                       font=('Arial', 9, 'bold'),
                       background=colors["button_bg"],
                       foreground=colors["fg"],
                       borderwidth=1,
                       relief="raised")

        # Ensure hover effect is visible by increasing contrast
        style.map('TimeRange.TButton',
                 background=[('active', colors["hover_bg"]),
                            ('pressed', colors["accent"])],
                 foreground=[('active', colors["fg"]),
                            ('pressed', 'white')])

        # Ensure selected button hover effect is applied
        style.map('TimeRange.Selected.TButton',
                 background=[('active', colors["accent"]),
                            ('pressed', colors["accent"]),
                            ('!active', colors["accent"]),
                            ('!pressed', colors["accent"])],
                 foreground=[('active', 'white'),
                            ('pressed', 'white'),
                            ('!active', 'white'),
                            ('!pressed', 'white')])

        # Define selected button style
        style.configure('TimeRange.Selected.TButton',
                       padding=(5, 3),
                       font=('Arial', 9, 'bold'),
                       background=colors["accent"],
                       foreground='white',
                       borderwidth=1,
                       relief="raised")

        # Ensure hover effect for selected buttons
        style.map('TimeRange.Selected.TButton',
                 background=[('active', colors["accent"]),
                            ('pressed', colors["accent"]),
                            ('!active', colors["accent"]),
                            ('!pressed', colors["accent"])],
                 foreground=[('active', 'white'),
                            ('pressed', 'white'),
                            ('!active', 'white'),
                            ('!pressed', 'white')])

        # Merkez hizalama için container - aralarda biraz boşluk bırakalım
        container = ttk.Frame(self.timerange_frame, style="ButtonFrame.TFrame")
        container.pack(expand=True, padx=5, pady=8)
        
        # Düğmeleri merkezi bir şekilde yerleştirmek için buton çerçevesi
        button_frame = ttk.Frame(container, style="ButtonFrame.TFrame")
        button_frame.pack(expand=True)
        
        self.timerange_buttons = {}

        # Apply styles explicitly to buttons to ensure they are used
        for text, value in time_ranges:
            is_selected = value == self.time_range.get()
            btn = ttk.Button(
                button_frame,
                text=text,
                command=lambda v=value: self.update_time_range(v),
                style='TimeRange.Selected.TButton' if is_selected else 'TimeRange.TButton',
                width=8  # Ensure sufficient button width
            )
            btn.pack(side=tk.LEFT, padx=3, pady=3)  # Add spacing between buttons
            self.timerange_buttons[value] = btn
            
            if value == "24h":
                self.time_range.set("24h")

    def update_time_range(self, value):
        """Zaman aralığı seçimini günceller ve ilgili butonları vurgular."""
        self.time_range.set(value)
        time_range_texts = {
            "1h": "1 Saat",
            "24h": "24 Saat",
            "1m": "1 Ay",
            "3m": "3 Ay",
            "6m": "6 Ay",
            "1y": "1 Yıl"
        }
        for val, btn in self.timerange_buttons.items():
            button_text = time_range_texts.get(val, val)
            if val == value:
                btn.configure(
                    style='TimeRange.Selected.TButton',
                    width=8,
                    text=button_text
                )
                btn.state(['!disabled'])  # Seçili butonun aktif ve görünür kalmasını sağla
            else:
                btn.configure(
                    style='TimeRange.TButton',
                    width=8,
                    text=button_text
                )
                btn.state(['!disabled'])
        self.update_dashboard()

    def create_metrics_widgets(self):
        """Fiyat, değişim, hacim ve aralık etiketlerini oluşturur."""
        # Current price and 24h change
        price_frame = ttk.LabelFrame(self.metrics_frame, text="Fiyat Bilgisi")
        price_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.price_label = ttk.Label(
            price_frame,
            text="Yükleniyor...",
            font=("Arial", 24, "bold")
        )
        self.price_label.pack(pady=5)
        
        self.change_label = ttk.Label(
            price_frame,
            text="24s Değişim: --",
            font=("Arial", 12)
        )
        self.change_label.pack(pady=5)
        
        # High/Low values
        range_frame = ttk.LabelFrame(self.metrics_frame, text="Günlük Aralık")
        range_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.high_low_label = ttk.Label(
            range_frame,
            text="En Yüksek: --\nEn Düşük: --",
            font=("Arial", 12)
        )
        self.high_low_label.pack(pady=5)
        
        # Volume information
        volume_frame = ttk.LabelFrame(self.metrics_frame, text="Hacim")
        volume_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.volume_label = ttk.Label(
            volume_frame,
            text="24s Hacim: --\n24s İşlem Sayısı: --",
            font=("Arial", 12)
        )
        self.volume_label.pack(pady=5)

    def fetch_dashboard_data(self):
        """Seçili token ve zaman aralığı için fiyat ve geçmiş verileri getirir."""
        token_name = self.selected_token.get()
        token_symbol = next((t["symbol"] for t in Utils.TOKEN_LIST if t["name"] == token_name), "BTC")
        time_range = self.time_range.get()
        self.fetcher.token_symbol = token_symbol
        current_price = self.fetcher.fetch_current_price()
        historical_data = self.fetcher.fetch_historical_data(time_range)
        return token_symbol, current_price, historical_data

    def update_dashboard_labels(self, current_price, historical_data):
        """Fiyat, değişim, hacim ve aralık etiketlerini günceller."""
        if current_price is not None:
            self.price_label.config(text=f"${current_price:,.2f}")
        prices = historical_data.get("prices", []) if historical_data else []
        if prices:
            latest_price = prices[-1]
            first_price = prices[0]
            highest_price = max(prices)
            lowest_price = min(prices)
            price_change = ((latest_price - first_price) / first_price) * 100
            color = "green" if price_change > 0 else "red"
            self.change_label.config(
                text=f"Değişim: {price_change:+.2f}%",
                foreground=color
            )
            self.high_low_label.config(
                text=f"En Yüksek: ${highest_price:,.2f}\nEn Düşük: ${lowest_price:,.2f}"
            )
        volumes = historical_data.get("volumes", []) if historical_data else []
        total_volume = sum(volumes) if volumes else 0
        self.volume_label.config(
            text=f"Toplam Hacim: ${total_volume:,.2f}"
        )

    def update_dashboard(self):
        try:
            token_symbol, current_price, historical_data = self.fetch_dashboard_data()
            if current_price is None or not historical_data:
                messagebox.showerror("Hata", "Fiyat veya geçmiş veri alınamadı")
                return
            self.update_dashboard_labels(current_price, historical_data)
            self.check_price_alerts(current_price)
            self.db.insert_price(token_symbol, current_price)
            self.update_graph(historical_data)
        except Exception as e:
            messagebox.showerror("Hata", f"Veri işlenirken hata oluştu: {str(e)}")
            return

    def update_graph(self, historical_data):
        """Verilen geçmiş veriyle grafiği günceller."""
        try:
            # Clear previous graph if exists
            if self.canvas:
                self.canvas.get_tk_widget().destroy()
            if self.fig:
                plt.close(self.fig)

            # Create figure
            self.fig = plt.figure(figsize=(12, 6))
            self.ax = self.fig.add_subplot(111)

            # Get price data
            prices = historical_data.get("prices", [])
            timestamps = historical_data.get("timestamps", [])
            if not prices or not timestamps:
                print("No price data available")
                return

            # Plot price data
            self.ax.plot(timestamps, prices, label='Price', color='blue')
            self.ax.set_ylabel('Price (USD)', color='blue')

            # Format x-axis with dates
            self.ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M' if self.time_range.get() in ["1h", "24h"] else '%Y-%m-%d'))
            plt.xticks(rotation=45)
            plt.grid(True)

            # Display the plot
            self.canvas = FigureCanvasTkAgg(self.fig, master=self.graph_frame)
            self.canvas.draw()
            self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        except Exception as e:
            messagebox.showerror("Hata", f"Grafik oluşturulurken hata oluştu: {str(e)}")
            return

    def get_notification_bg(self, type_):
        """Bildirim tipi için arka plan rengini döndürür."""
        colors = self.theme_manager.get_colors()
        return {
            "info": colors["accent"],
            "error": "#ff5252",
            "success": "#4caf50"
        }.get(type_, colors["accent"])

    def show_notification(self, message, type_="info"):
        """Köşede kısa süreli bildirim gösterir."""
        colors = self.theme_manager.get_colors()
        notification = tk.Toplevel(self.root)
        notification.overrideredirect(True)
        # Position notification at the bottom right
        x = self.root.winfo_x() + self.root.winfo_width() - 300
        y = self.root.winfo_y() + self.root.winfo_height() - 100
        notification.geometry(f"300x50+{x}+{y}")
        bg_color = self.get_notification_bg(type_)
        frame = ttk.Frame(notification, style="Card.TFrame")
        frame.pack(fill=tk.BOTH, expand=True)
        label = ttk.Label(frame, text=message, foreground=colors["selected_fg"],
                          background=bg_color, padding=(10, 5))
        label.pack(fill=tk.BOTH, expand=True)
        notification.after(3000, notification.destroy)

