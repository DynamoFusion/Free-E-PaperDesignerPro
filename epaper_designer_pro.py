#!/usr/bin/env python3
"""
E-Paper Designer Pro
The first visual drag-and-drop editor for Waveshare e-paper displays
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, colorchooser
from PIL import Image, ImageDraw, ImageFont, ImageTk, ImageOps
import json
import os

class DrawableObject:
    """Base class for draggable objects"""
    def __init__(self, obj_type):
        self.type = obj_type
        self.z_index = 0
    
    def contains_point(self, x, y):
        return False
    
    def move(self, dx, dy):
        pass
    
    def draw(self, draw, fonts):
        pass
    
    def get_position(self):
        return (0, 0)
    
    def to_dict(self):
        """Serialize to dict"""
        return {'type': self.type, 'z_index': self.z_index}
    
    @staticmethod
    def from_dict(data):
        """Deserialize from dict"""
        obj_type = data.get('type')
        if obj_type == 'Rectangle':
            return RectangleObject.from_dict(data)
        elif obj_type == 'Circle':
            return CircleObject.from_dict(data)
        elif obj_type == 'Text':
            return TextObject.from_dict(data)
        elif obj_type == 'Line':
            return LineObject.from_dict(data)
        elif obj_type == 'Icon':
            return IconObject.from_dict(data)
        return None


class RectangleObject(DrawableObject):
    def __init__(self, x, y, width, height, filled=False):
        super().__init__("Rectangle")
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.filled = filled
    
    def contains_point(self, x, y):
        return (self.x <= x <= self.x + self.width and 
                self.y <= y <= self.y + self.height)
    
    def move(self, dx, dy):
        self.x += dx
        self.y += dy
    
    def draw(self, draw, fonts):
        if self.filled:
            draw.rectangle([self.x, self.y, self.x+self.width, self.y+self.height], 
                          fill=0, outline=0)
        else:
            draw.rectangle([self.x, self.y, self.x+self.width, self.y+self.height], 
                          outline=0, width=2)
    
    def get_position(self):
        return (self.x, self.y)
    
    def to_dict(self):
        d = super().to_dict()
        d.update({'x': self.x, 'y': self.y, 'width': self.width, 
                  'height': self.height, 'filled': self.filled})
        return d
    
    @staticmethod
    def from_dict(data):
        obj = RectangleObject(data['x'], data['y'], data['width'], 
                             data['height'], data['filled'])
        obj.z_index = data.get('z_index', 0)
        return obj


class CircleObject(DrawableObject):
    def __init__(self, x, y, radius, filled=False):
        super().__init__("Circle")
        self.x = x
        self.y = y
        self.radius = radius
        self.filled = filled
    
    def contains_point(self, x, y):
        dx = x - self.x
        dy = y - self.y
        return (dx*dx + dy*dy) <= (self.radius * self.radius)
    
    def move(self, dx, dy):
        self.x += dx
        self.y += dy
    
    def draw(self, draw, fonts):
        if self.filled:
            draw.ellipse([self.x-self.radius, self.y-self.radius, 
                         self.x+self.radius, self.y+self.radius], 
                        fill=0, outline=0)
        else:
            draw.ellipse([self.x-self.radius, self.y-self.radius, 
                         self.x+self.radius, self.y+self.radius], 
                        outline=0, width=2)
    
    def get_position(self):
        return (self.x, self.y)
    
    def to_dict(self):
        d = super().to_dict()
        d.update({'x': self.x, 'y': self.y, 'radius': self.radius, 'filled': self.filled})
        return d
    
    @staticmethod
    def from_dict(data):
        obj = CircleObject(data['x'], data['y'], data['radius'], data['filled'])
        obj.z_index = data.get('z_index', 0)
        return obj


class TextObject(DrawableObject):
    def __init__(self, x, y, text, font_size="medium"):
        super().__init__("Text")
        self.x = x
        self.y = y
        self.text = text
        self.font_size = font_size
        self.width = len(text) * 8
        self.height = 12
    
    def contains_point(self, x, y):
        return (self.x <= x <= self.x + self.width and 
                self.y <= y <= self.y + self.height)
    
    def move(self, dx, dy):
        self.x += dx
        self.y += dy
    
    def draw(self, draw, fonts):
        font = fonts.get(self.font_size, fonts['medium'])
        draw.text((self.x, self.y), self.text, font=font, fill=0)
    
    def get_position(self):
        return (self.x, self.y)
    
    def to_dict(self):
        d = super().to_dict()
        d.update({'x': self.x, 'y': self.y, 'text': self.text, 'font_size': self.font_size})
        return d
    
    @staticmethod
    def from_dict(data):
        obj = TextObject(data['x'], data['y'], data['text'], data['font_size'])
        obj.z_index = data.get('z_index', 0)
        return obj


class LineObject(DrawableObject):
    def __init__(self, x1, y1, x2, y2, width=2):
        super().__init__("Line")
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.line_width = width
    
    def contains_point(self, x, y):
        px = self.x2 - self.x1
        py = self.y2 - self.y1
        norm = px*px + py*py
        
        if norm == 0:
            return False
        
        u = ((x - self.x1) * px + (y - self.y1) * py) / norm
        u = max(0, min(1, u))
        
        dx = self.x1 + u * px - x
        dy = self.y1 + u * py - y
        
        return (dx*dx + dy*dy) <= (self.line_width + 3)**2
    
    def move(self, dx, dy):
        self.x1 += dx
        self.y1 += dy
        self.x2 += dx
        self.y2 += dy
    
    def draw(self, draw, fonts):
        draw.line([self.x1, self.y1, self.x2, self.y2], 
                 fill=0, width=self.line_width)
    
    def get_position(self):
        return (self.x1, self.y1)
    
    def to_dict(self):
        d = super().to_dict()
        d.update({'x1': self.x1, 'y1': self.y1, 'x2': self.x2, 
                  'y2': self.y2, 'line_width': self.line_width})
        return d
    
    @staticmethod
    def from_dict(data):
        obj = LineObject(data['x1'], data['y1'], data['x2'], 
                        data['y2'], data['line_width'])
        obj.z_index = data.get('z_index', 0)
        return obj


class IconObject(DrawableObject):
    """Pre-made icons (WiFi, Bluetooth, Battery, etc.)"""
    
    ICONS = {
        'wifi': lambda d, x, y, s: [
            d.arc([x-s, y+s//2, x+s, y+s+s//2], 180, 360, fill=0, width=2),
            d.arc([x-s//2, y+s//2+s//4, x+s//2, y+s+s//4], 180, 360, fill=0, width=2),
            d.ellipse([x-2, y+s-2, x+2, y+s+2], fill=0),
        ],
        'bluetooth': lambda d, x, y, s: [
            d.polygon([(x, y), (x+s, y+s//2), (x, y+s), (x+s, y+s+s//2), (x, y+s)], outline=0, width=2),
            d.line([x, y, x, y+s], fill=0, width=2),
        ],
        'battery_full': lambda d, x, y, s: [
            d.rectangle([x, y+s//4, x+s, y+3*s//4], outline=0, width=2),
            d.rectangle([x+s, y+s//3, x+s+s//6, y+2*s//3], fill=0),
            d.rectangle([x+2, y+s//4+2, x+s-2, y+3*s//4-2], fill=0),
        ],
        'battery_half': lambda d, x, y, s: [
            d.rectangle([x, y+s//4, x+s, y+3*s//4], outline=0, width=2),
            d.rectangle([x+s, y+s//3, x+s+s//6, y+2*s//3], fill=0),
            d.rectangle([x+2, y+s//4+2, x+s//2, y+3*s//4-2], fill=0),
        ],
        'battery_low': lambda d, x, y, s: [
            d.rectangle([x, y+s//4, x+s, y+3*s//4], outline=0, width=2),
            d.rectangle([x+s, y+s//3, x+s+s//6, y+2*s//3], fill=0),
            d.rectangle([x+2, y+s//4+2, x+s//4, y+3*s//4-2], fill=0),
        ],
        'heart': lambda d, x, y, s: [
            d.polygon([
                (x, y+s//3), 
                (x-s//2, y), (x-s//3, y-s//4), (x, y),
                (x+s//3, y-s//4), (x+s//2, y),
                (x, y+s//3), (x, y+s)
            ], fill=0),
        ],
        'star': lambda d, x, y, s: [
            d.polygon([
                (x, y-s//2), (x+s//6, y), (x+s//2, y), (x+s//4, y+s//4),
                (x+s//3, y+s//2), (x, y+s//3), (x-s//3, y+s//2),
                (x-s//4, y+s//4), (x-s//2, y), (x-s//6, y)
            ], fill=0),
        ],
        'check': lambda d, x, y, s: [
            d.line([x-s//2, y, x, y+s//2], fill=0, width=3),
            d.line([x, y+s//2, x+s, y-s//2], fill=0, width=3),
        ],
        'x': lambda d, x, y, s: [
            d.line([x-s//2, y-s//2, x+s//2, y+s//2], fill=0, width=3),
            d.line([x-s//2, y+s//2, x+s//2, y-s//2], fill=0, width=3),
        ],
        'arrow_up': lambda d, x, y, s: [
            d.polygon([(x, y-s//2), (x+s//2, y+s//2), (x-s//2, y+s//2)], fill=0),
        ],
        'arrow_down': lambda d, x, y, s: [
            d.polygon([(x, y+s//2), (x+s//2, y-s//2), (x-s//2, y-s//2)], fill=0),
        ],
        'home': lambda d, x, y, s: [
            d.polygon([(x, y-s//2), (x+s//2, y), (x+s//2, y+s//2), 
                      (x-s//2, y+s//2), (x-s//2, y)], outline=0, width=2),
            d.rectangle([x-s//6, y+s//6, x+s//6, y+s//2], fill=0),
        ],
        'settings': lambda d, x, y, s: [
            d.ellipse([x-s//3, y-s//3, x+s//3, y+s//3], outline=0, width=2),
            d.rectangle([x-s//6, y-s//6, x+s//6, y+s//6], fill=0),
            *[d.line([x+int(s//2*__import__('math').cos(a)), 
                     y+int(s//2*__import__('math').sin(a)),
                     x+int(s//3*__import__('math').cos(a)), 
                     y+int(s//3*__import__('math').sin(a))], fill=0, width=2)
              for a in [0, 1.57, 3.14, 4.71]],
        ],
    }
    
    def __init__(self, x, y, icon_type, size=16):
        super().__init__("Icon")
        self.x = x
        self.y = y
        self.icon_type = icon_type
        self.size = size
    
    def contains_point(self, x, y):
        return (self.x - self.size <= x <= self.x + self.size and 
                self.y - self.size <= y <= self.y + self.size)
    
    def move(self, dx, dy):
        self.x += dx
        self.y += dy
    
    def draw(self, draw, fonts):
        if self.icon_type in self.ICONS:
            self.ICONS[self.icon_type](draw, self.x, self.y, self.size)
    
    def get_position(self):
        return (self.x, self.y)
    
    def to_dict(self):
        d = super().to_dict()
        d.update({'x': self.x, 'y': self.y, 'icon_type': self.icon_type, 'size': self.size})
        return d
    
    @staticmethod
    def from_dict(data):
        obj = IconObject(data['x'], data['y'], data['icon_type'], data['size'])
        obj.z_index = data.get('z_index', 0)
        return obj


class EpaperDesigner:
    def __init__(self, root):
        self.root = root
        self.root.title("E-Paper Designer Pro - The First Visual Editor for E-Paper!")
        
        # Display size presets
        self.display_presets = {
            'Waveshare 2.13" V4 (250×122)': (250, 122),
            'Waveshare 1.54" (200×200)': (200, 200),
            'Waveshare 2.9" (296×128)': (296, 128),
            'Waveshare 4.2" (400×300)': (400, 300),
            'Waveshare 7.5" (800×480)': (800, 480),
            'Custom...': None,
        }
        
        # Display dimensions
        self.width = 250
        self.height = 122
        self.scale = 3
        self.current_display = 'Waveshare 2.13" V4 (250×122)'
        
        # State
        self.objects = []
        self.selected_object = None
        self.drag_start = None
        self.grid_snap = False
        self.grid_size = 5
        self.show_rulers = False
        self.history = []  # Undo/redo
        self.history_index = -1
        self.current_file = None
        
        # Fonts
        self.fonts = {}
        self.load_fonts()
        
        # Create GUI
        self.create_menu()
        self.create_widgets()
        
        # Keyboard shortcuts
        self.root.bind('<Control-z>', lambda e: self.undo())
        self.root.bind('<Control-y>', lambda e: self.redo())
        self.root.bind('<Control-s>', lambda e: self.save_project())
        self.root.bind('<Control-o>', lambda e: self.load_project())
        self.root.bind('<Delete>', lambda e: self.delete_selected())
        self.root.bind('<Control-d>', lambda e: self.duplicate_selected())
        self.root.bind('<Up>', lambda e: self.nudge(0, -1))
        self.root.bind('<Down>', lambda e: self.nudge(0, 1))
        self.root.bind('<Left>', lambda e: self.nudge(-1, 0))
        self.root.bind('<Right>', lambda e: self.nudge(1, 0))
        
        self.redraw_all()
        self.save_history()
    
    def load_fonts(self):
        try:
            self.fonts['tiny'] = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 8)
            self.fonts['small'] = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 10)
            self.fonts['medium'] = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 12)
            self.fonts['large'] = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 16)
        except:
            # Fallback for Windows
            try:
                self.fonts['tiny'] = ImageFont.truetype("arial.ttf", 8)
                self.fonts['small'] = ImageFont.truetype("arial.ttf", 10)
                self.fonts['medium'] = ImageFont.truetype("arial.ttf", 12)
                self.fonts['large'] = ImageFont.truetype("arialbd.ttf", 16)
            except:
                self.fonts['tiny'] = ImageFont.load_default()
                self.fonts['small'] = ImageFont.load_default()
                self.fonts['medium'] = ImageFont.load_default()
                self.fonts['large'] = ImageFont.load_default()
    
    def create_menu(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New Project", command=self.new_project, accelerator="Ctrl+N")
        file_menu.add_command(label="Open Project...", command=self.load_project, accelerator="Ctrl+O")
        file_menu.add_command(label="Save Project", command=self.save_project, accelerator="Ctrl+S")
        file_menu.add_command(label="Save Project As...", command=self.save_project_as)
        file_menu.add_separator()
        file_menu.add_command(label="Export PNG...", command=self.save_image)
        file_menu.add_command(label="Export Python Code...", command=self.export_code)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        
        # Edit menu
        edit_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Edit", menu=edit_menu)
        edit_menu.add_command(label="Undo", command=self.undo, accelerator="Ctrl+Z")
        edit_menu.add_command(label="Redo", command=self.redo, accelerator="Ctrl+Y")
        edit_menu.add_separator()
        edit_menu.add_command(label="Duplicate", command=self.duplicate_selected, accelerator="Ctrl+D")
        edit_menu.add_command(label="Delete", command=self.delete_selected, accelerator="Del")
        edit_menu.add_separator()
        edit_menu.add_command(label="Select All", command=self.select_all)
        edit_menu.add_command(label="Clear All", command=self.clear_all)
        
        # View menu
        view_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="View", menu=view_menu)
        view_menu.add_checkbutton(label="Grid Snap", command=self.toggle_grid_snap)
        view_menu.add_checkbutton(label="Show Rulers", command=self.toggle_rulers)
        view_menu.add_separator()
        
        # Display size submenu
        display_menu = tk.Menu(view_menu, tearoff=0)
        view_menu.add_cascade(label="Display Size", menu=display_menu)
        for display_name in self.display_presets.keys():
            display_menu.add_command(label=display_name, 
                                    command=lambda d=display_name: self.change_display_size(d))
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="Keyboard Shortcuts", command=self.show_shortcuts)
        help_menu.add_separator()
        help_menu.add_command(label="☕ Support Development", command=self.show_support)
        help_menu.add_separator()
        help_menu.add_command(label="About", command=self.show_about)
    
    def create_widgets(self):
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Canvas frame with label
        canvas_frame = ttk.Frame(main_frame)
        canvas_frame.grid(row=0, column=0, rowspan=30, padx=10, pady=10)
        
        # Display info label above canvas
        display_info = ttk.Label(canvas_frame, 
                                text=f"📺 Waveshare 2.13\" e-Paper | {self.width}×{self.height}px | Scale: {self.scale}×",
                                font=('Arial', 10, 'bold'),
                                relief='solid',
                                padding=5)
        display_info.pack(pady=(0, 5))
        
        # Canvas
        self.canvas = tk.Canvas(canvas_frame, width=self.width*self.scale, 
                               height=self.height*self.scale, bg='white', bd=2, relief='solid')
        self.canvas.pack()
        
        # Dimensions label below canvas
        dims_label = ttk.Label(canvas_frame,
                              text=f"Actual Size: 2.13 inches | 23.71mm × 48.55mm",
                              font=('Arial', 8),
                              foreground='gray')
        dims_label.pack(pady=(5, 0))
        
        # Mouse events
        self.canvas.bind("<Button-1>", self.on_mouse_down)
        self.canvas.bind("<B1-Motion>", self.on_mouse_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_mouse_up)
        self.canvas.bind("<Button-3>", self.on_right_click)
        
        # Toolbar
        toolbar_frame = ttk.LabelFrame(main_frame, text="Tools", padding="10")
        toolbar_frame.grid(row=0, column=1, columnspan=2, sticky='ew', padx=5)
        
        # Basic shapes
        ttk.Button(toolbar_frame, text="📐 Rectangle", command=self.add_rectangle, width=15).grid(row=0, column=0, pady=2)
        ttk.Button(toolbar_frame, text="⭕ Circle", command=self.add_circle, width=15).grid(row=0, column=1, pady=2)
        ttk.Button(toolbar_frame, text="📝 Text", command=self.add_text, width=15).grid(row=1, column=0, pady=2)
        ttk.Button(toolbar_frame, text="➖ Line", command=self.add_line, width=15).grid(row=1, column=1, pady=2)
        
        # Icons panel
        icons_frame = ttk.LabelFrame(main_frame, text="Icons", padding="10")
        icons_frame.grid(row=1, column=1, columnspan=2, sticky='ew', padx=5, pady=5)
        
        icons_list = [
            ('📶 WiFi', 'wifi'),
            ('📡 Bluetooth', 'bluetooth'),
            ('🔋 Battery Full', 'battery_full'),
            ('🔋 Battery Half', 'battery_half'),
            ('🔋 Battery Low', 'battery_low'),
            ('❤️ Heart', 'heart'),
            ('⭐ Star', 'star'),
            ('✓ Check', 'check'),
            ('✗ X', 'x'),
            ('🏠 Home', 'home'),
            ('⚙️ Settings', 'settings'),
            ('⬆️ Arrow Up', 'arrow_up'),
            ('⬇️ Arrow Down', 'arrow_down'),
        ]
        
        for i, (label, icon_type) in enumerate(icons_list):
            row = i // 2
            col = i % 2
            ttk.Button(icons_frame, text=label, 
                      command=lambda it=icon_type: self.add_icon(it),
                      width=15).grid(row=row, column=col, pady=1, padx=2)
        
        # Layer controls
        layer_frame = ttk.LabelFrame(main_frame, text="Layers", padding="10")
        layer_frame.grid(row=2, column=1, columnspan=2, sticky='ew', padx=5, pady=5)
        
        ttk.Button(layer_frame, text="⬆️ Bring Forward", command=self.bring_forward, width=15).grid(row=0, column=0, pady=2)
        ttk.Button(layer_frame, text="⬇️ Send Backward", command=self.send_backward, width=15).grid(row=0, column=1, pady=2)
        
        # Alignment
        align_frame = ttk.LabelFrame(main_frame, text="Align", padding="10")
        align_frame.grid(row=3, column=1, columnspan=2, sticky='ew', padx=5, pady=5)
        
        ttk.Button(align_frame, text="⬅️ Left", command=lambda: self.align('left'), width=10).grid(row=0, column=0, pady=2)
        ttk.Button(align_frame, text="↕️ Center V", command=lambda: self.align('center_v'), width=10).grid(row=0, column=1, pady=2)
        ttk.Button(align_frame, text="➡️ Right", command=lambda: self.align('right'), width=10).grid(row=0, column=2, pady=2)
        ttk.Button(align_frame, text="⬆️ Top", command=lambda: self.align('top'), width=10).grid(row=1, column=0, pady=2)
        ttk.Button(align_frame, text="↔️ Center H", command=lambda: self.align('center_h'), width=10).grid(row=1, column=1, pady=2)
        ttk.Button(align_frame, text="⬇️ Bottom", command=lambda: self.align('bottom'), width=10).grid(row=1, column=2, pady=2)
        
        # Grid snap toggle
        self.grid_var = tk.BooleanVar()
        ttk.Checkbutton(align_frame, text="Grid Snap (5px)", variable=self.grid_var, 
                       command=self.toggle_grid_snap).grid(row=2, column=0, columnspan=3, pady=5)
        
        # Info/Stats panel
        stats_frame = ttk.LabelFrame(main_frame, text="Project Info", padding="10")
        stats_frame.grid(row=4, column=1, columnspan=2, sticky='ew', padx=5, pady=5)
        
        self.stats_label = ttk.Label(stats_frame, text=self._get_stats_text(), 
                                     font=('Courier', 8), justify='left')
        self.stats_label.pack()
        
        # Status
        self.info_label = ttk.Label(main_frame, text="Ready - Drag objects, right-click to delete", relief='sunken')
        self.info_label.grid(row=5, column=1, columnspan=2, sticky='ew', pady=10)
    
    def redraw_all(self):
        # Create image
        self.image = Image.new('1', (self.width, self.height), 255)
        self.draw = ImageDraw.Draw(self.image)
        
        # Draw grid if snap enabled
        if self.grid_snap:
            for x in range(0, self.width, self.grid_size):
                for y in range(0, self.height, self.grid_size):
                    if x % (self.grid_size * 4) == 0 and y % (self.grid_size * 4) == 0:
                        # Draw small dots at major grid intersections
                        self.draw.point((x, y), fill=128)
        
        # Sort by z-index and draw
        sorted_objects = sorted(self.objects, key=lambda obj: obj.z_index)
        for obj in sorted_objects:
            obj.draw(self.draw, self.fonts)
        
        # Update canvas
        scaled = self.image.resize((self.width*self.scale, self.height*self.scale), Image.NEAREST)
        self.photo = ImageTk.PhotoImage(scaled)
        self.canvas.delete("all")
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo)
        
        # Draw rulers if enabled
        if self.show_rulers:
            self._draw_rulers()
        
        # Draw selection box on canvas
        if self.selected_object:
            pos = self.selected_object.get_position()
            x, y = pos[0] * self.scale, pos[1] * self.scale
            # Draw selection box
            self.canvas.create_rectangle(x-5, y-5, x+5, y+5, outline='red', width=2)
            # Draw crosshair
            self.canvas.create_line(x-10, y, x+10, y, fill='red', width=1)
            self.canvas.create_line(x, y-10, x, y+10, fill='red', width=1)
            # Show coordinates
            self.canvas.create_text(x, y-15, text=f"({pos[0]}, {pos[1]})", 
                                   fill='red', font=('Arial', 8, 'bold'))
    
    def _draw_rulers(self):
        """Draw ruler overlays on canvas"""
        # Draw horizontal ruler (top)
        for x in range(0, self.width, 10):
            scaled_x = x * self.scale
            if x % 50 == 0:
                # Major tick
                self.canvas.create_line(scaled_x, 0, scaled_x, 15, fill='blue', width=2)
                self.canvas.create_text(scaled_x, 20, text=str(x), fill='blue', font=('Arial', 7))
            elif x % 10 == 0:
                # Minor tick
                self.canvas.create_line(scaled_x, 0, scaled_x, 8, fill='gray', width=1)
        
        # Draw vertical ruler (left)
        for y in range(0, self.height, 10):
            scaled_y = y * self.scale
            if y % 50 == 0:
                # Major tick
                self.canvas.create_line(0, scaled_y, 15, scaled_y, fill='blue', width=2)
                self.canvas.create_text(20, scaled_y, text=str(y), fill='blue', font=('Arial', 7))
            elif y % 10 == 0:
                # Minor tick
                self.canvas.create_line(0, scaled_y, 8, scaled_y, fill='gray', width=1)
        
        # Draw corner marker
        self.canvas.create_rectangle(0, 0, 25, 25, fill='lightgray', outline='blue', width=2)
        self.canvas.create_text(12, 12, text="0,0", fill='blue', font=('Arial', 6, 'bold'))
    
    def snap_to_grid(self, value):
        if self.grid_snap:
            return round(value / self.grid_size) * self.grid_size
        return value
    
    def _get_stats_text(self):
        """Generate stats text for info panel"""
        obj_counts = {}
        for obj in self.objects:
            obj_counts[obj.type] = obj_counts.get(obj.type, 0) + 1
        
        stats = f"Display: {self.width}×{self.height}px\n"
        stats += f"Objects: {len(self.objects)}\n"
        for obj_type, count in sorted(obj_counts.items()):
            stats += f"  {obj_type}: {count}\n"
        stats += f"Selected: {self.selected_object.type if self.selected_object else 'None'}"
        return stats
    
    def _update_stats(self):
        """Update stats display"""
        if hasattr(self, 'stats_label'):
            self.stats_label.config(text=self._get_stats_text())
    
    def toggle_grid_snap(self):
        self.grid_snap = self.grid_var.get()
        self.redraw_all()
    
    def toggle_rulers(self):
        self.show_rulers = not self.show_rulers
        self.redraw_all()
    
    def change_display_size(self, display_name):
        """Change the display size"""
        if display_name == 'Custom...':
            dialog = tk.Toplevel(self.root)
            dialog.title("Custom Display Size")
            dialog.geometry("300x150")
            
            ttk.Label(dialog, text="Width (px):").grid(row=0, column=0, padx=10, pady=10)
            width_entry = ttk.Entry(dialog, width=10)
            width_entry.insert(0, str(self.width))
            width_entry.grid(row=0, column=1, padx=10, pady=10)
            
            ttk.Label(dialog, text="Height (px):").grid(row=1, column=0, padx=10, pady=10)
            height_entry = ttk.Entry(dialog, width=10)
            height_entry.insert(0, str(self.height))
            height_entry.grid(row=1, column=1, padx=10, pady=10)
            
            def apply_custom():
                try:
                    new_width = int(width_entry.get())
                    new_height = int(height_entry.get())
                    if 50 <= new_width <= 1200 and 50 <= new_height <= 800:
                        self.width = new_width
                        self.height = new_height
                        self.current_display = f"Custom ({new_width}×{new_height})"
                        self._update_canvas_size()
                        dialog.destroy()
                    else:
                        messagebox.showerror("Error", "Size must be between 50-1200 (width) and 50-800 (height)")
                except ValueError:
                    messagebox.showerror("Error", "Please enter valid numbers")
            
            ttk.Button(dialog, text="Apply", command=apply_custom).grid(row=2, column=0, columnspan=2, pady=20)
        else:
            size = self.display_presets.get(display_name)
            if size:
                if messagebox.askyesno("Change Display Size", 
                                      f"Change to {display_name}?\n\nCurrent objects will be kept but may need repositioning."):
                    self.width, self.height = size
                    self.current_display = display_name
                    self._update_canvas_size()
    
    def _update_canvas_size(self):
        """Update canvas and UI after size change"""
        # Adjust scale if display is too large
        max_canvas_width = 900
        max_canvas_height = 600
        scale_x = max_canvas_width // self.width
        scale_y = max_canvas_height // self.height
        self.scale = max(1, min(scale_x, scale_y, 3))
        
        # Recreate canvas
        self.canvas.config(width=self.width*self.scale, height=self.height*self.scale)
        
        # Update display info label
        for widget in self.canvas.master.winfo_children():
            if isinstance(widget, ttk.Label) and "📺" in widget.cget("text"):
                widget.config(text=f"📺 {self.current_display} | {self.width}×{self.height}px | Scale: {self.scale}×")
                break
        
        self.redraw_all()
        self.info_label.config(text=f"Display size changed to {self.width}×{self.height}px")
    
    def on_mouse_down(self, event):
        x = event.x // self.scale
        y = event.y // self.scale
        
        for obj in reversed(sorted(self.objects, key=lambda o: o.z_index)):
            if obj.contains_point(x, y):
                self.selected_object = obj
                self.drag_start = (x, y)
                self.info_label.config(text=f"Selected {obj.type} - Arrow keys to nudge, Del to delete")
                self.redraw_all()
                return
        
        self.selected_object = None
        self.redraw_all()
    
    def on_mouse_drag(self, event):
        if self.selected_object and self.drag_start:
            x = event.x // self.scale
            y = event.y // self.scale
            
            dx = self.snap_to_grid(x - self.drag_start[0])
            dy = self.snap_to_grid(y - self.drag_start[1])
            
            if dx != 0 or dy != 0:
                self.selected_object.move(dx, dy)
                self.drag_start = (x, y)
                self.redraw_all()
    
    def on_mouse_up(self, event):
        if self.selected_object:
            self.save_history()
            pos = self.selected_object.get_position()
            self.info_label.config(text=f"{self.selected_object.type} at {pos}")
        self.drag_start = None
    
    def on_right_click(self, event):
        x = event.x // self.scale
        y = event.y // self.scale
        
        for obj in reversed(sorted(self.objects, key=lambda o: o.z_index)):
            if obj.contains_point(x, y):
                self.objects.remove(obj)
                self.selected_object = None
                self.save_history()
                self.redraw_all()
                self.info_label.config(text=f"Deleted {obj.type}")
                return
    
    def nudge(self, dx, dy):
        if self.selected_object:
            self.selected_object.move(dx, dy)
            self.save_history()
            self.redraw_all()
    
    def delete_selected(self):
        if self.selected_object:
            self.objects.remove(self.selected_object)
            self.selected_object = None
            self.save_history()
            self._update_stats()
            self.redraw_all()
    
    def duplicate_selected(self):
        if self.selected_object:
            # Create copy
            data = self.selected_object.to_dict()
            new_obj = DrawableObject.from_dict(data)
            new_obj.move(10, 10)  # Offset slightly
            new_obj.z_index = max([o.z_index for o in self.objects] + [0]) + 1
            self.objects.append(new_obj)
            self.selected_object = new_obj
            self.save_history()
            self.redraw_all()
            self.info_label.config(text=f"Duplicated {new_obj.type}")
    
    def bring_forward(self):
        if self.selected_object:
            self.selected_object.z_index += 1
            self.save_history()
            self.redraw_all()
    
    def send_backward(self):
        if self.selected_object:
            self.selected_object.z_index -= 1
            self.save_history()
            self.redraw_all()
    
    def align(self, direction):
        if not self.selected_object:
            return
        
        if direction == 'left':
            pos = self.selected_object.get_position()
            self.selected_object.move(-pos[0], 0)
        elif direction == 'right':
            pos = self.selected_object.get_position()
            self.selected_object.move(self.width - pos[0], 0)
        elif direction == 'top':
            pos = self.selected_object.get_position()
            self.selected_object.move(0, -pos[1])
        elif direction == 'bottom':
            pos = self.selected_object.get_position()
            self.selected_object.move(0, self.height - pos[1])
        elif direction == 'center_v':
            pos = self.selected_object.get_position()
            self.selected_object.move(self.width//2 - pos[0], 0)
        elif direction == 'center_h':
            pos = self.selected_object.get_position()
            self.selected_object.move(0, self.height//2 - pos[1])
        
        self.save_history()
        self.redraw_all()
    
    def select_all(self):
        # Future: multi-select
        pass
    
    def clear_all(self):
        if self.objects and messagebox.askyesno("Clear All", "Delete all objects?"):
            self.objects = []
            self.selected_object = None
            self.save_history()
            self.redraw_all()
    
    def save_history(self):
        """Save current state for undo/redo"""
        # Remove future history if we're in the middle
        if self.history_index < len(self.history) - 1:
            self.history = self.history[:self.history_index + 1]
        
        # Save state
        state = [obj.to_dict() for obj in self.objects]
        self.history.append(state)
        self.history_index += 1
        
        # Limit history size
        if len(self.history) > 50:
            self.history.pop(0)
            self.history_index -= 1
    
    def undo(self):
        if self.history_index > 0:
            self.history_index -= 1
            self.load_state(self.history[self.history_index])
            self.info_label.config(text="Undo")
    
    def redo(self):
        if self.history_index < len(self.history) - 1:
            self.history_index += 1
            self.load_state(self.history[self.history_index])
            self.info_label.config(text="Redo")
    
    def load_state(self, state):
        """Load objects from state"""
        self.objects = [DrawableObject.from_dict(obj_data) for obj_data in state]
        self.selected_object = None
        self.redraw_all()
    
    def new_project(self):
        if messagebox.askyesno("New Project", "Clear current project?"):
            self.objects = []
            self.selected_object = None
            self.current_file = None
            self.history = []
            self.history_index = -1
            self.save_history()
            self.redraw_all()
            self.root.title("E-Paper Designer Pro - Untitled")
    
    def save_project(self):
        if self.current_file:
            self._save_to_file(self.current_file)
        else:
            self.save_project_as()
    
    def save_project_as(self):
        filename = filedialog.asksaveasfilename(
            defaultextension=".epd",
            filetypes=[("E-Paper Design", "*.epd"), ("JSON", "*.json"), ("All files", "*.*")]
        )
        if filename:
            self._save_to_file(filename)
            self.current_file = filename
            self.root.title(f"E-Paper Designer Pro - {os.path.basename(filename)}")
    
    def _save_to_file(self, filename):
        data = {
            'version': '1.0',
            'width': self.width,
            'height': self.height,
            'objects': [obj.to_dict() for obj in self.objects]
        }
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        self.info_label.config(text=f"Saved: {filename}")
    
    def load_project(self):
        filename = filedialog.askopenfilename(
            filetypes=[("E-Paper Design", "*.epd"), ("JSON", "*.json"), ("All files", "*.*")]
        )
        if filename:
            with open(filename, 'r') as f:
                data = json.load(f)
            
            self.objects = [DrawableObject.from_dict(obj_data) for obj_data in data['objects']]
            self.current_file = filename
            self.selected_object = None
            self.save_history()
            self.redraw_all()
            self.root.title(f"E-Paper Designer Pro - {os.path.basename(filename)}")
            self.info_label.config(text=f"Loaded: {filename}")
    
    def add_rectangle(self):
        obj = RectangleObject(20, 20, 60, 40, False)
        obj.z_index = max([o.z_index for o in self.objects] + [0]) + 1
        self.objects.append(obj)
        self.selected_object = obj
        self.save_history()
        self.redraw_all()
    
    def add_circle(self):
        obj = CircleObject(125, 61, 25, False)
        obj.z_index = max([o.z_index for o in self.objects] + [0]) + 1
        self.objects.append(obj)
        self.selected_object = obj
        self.save_history()
        self.redraw_all()
    
    def add_text(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Add Text")
        dialog.geometry("300x180")
        
        ttk.Label(dialog, text="Text:").grid(row=0, column=0, sticky='e', padx=5, pady=5)
        text_entry = ttk.Entry(dialog, width=20)
        text_entry.insert(0, "Hello World")
        text_entry.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(dialog, text="Font:").grid(row=1, column=0, sticky='e', padx=5, pady=5)
        font_var = tk.StringVar(value="medium")
        ttk.Combobox(dialog, textvariable=font_var, 
                    values=['tiny', 'small', 'medium', 'large'], width=17).grid(row=1, column=1, padx=5, pady=5)
        
        def create():
            obj = TextObject(10, 10, text_entry.get(), font_var.get())
            obj.z_index = max([o.z_index for o in self.objects] + [0]) + 1
            self.objects.append(obj)
            self.selected_object = obj
            self.save_history()
            self.redraw_all()
            dialog.destroy()
        
        ttk.Button(dialog, text="Create", command=create).grid(row=2, column=0, columnspan=2, pady=20)
    
    def add_line(self):
        obj = LineObject(10, 10, 100, 100, 2)
        obj.z_index = max([o.z_index for o in self.objects] + [0]) + 1
        self.objects.append(obj)
        self.selected_object = obj
        self.save_history()
        self.redraw_all()
    
    def add_icon(self, icon_type):
        obj = IconObject(125, 61, icon_type, 16)
        obj.z_index = max([o.z_index for o in self.objects] + [0]) + 1
        self.objects.append(obj)
        self.selected_object = obj
        self.save_history()
        self._update_stats()
        self.redraw_all()
        self.info_label.config(text=f"Added {icon_type} icon - Drag to position")
    
    def save_image(self):
        filename = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"), ("All files", "*.*")]
        )
        if filename:
            self.image.save(filename)
            self.info_label.config(text=f"Exported PNG: {filename}")
    
    def export_code(self):
        # Convert to buffer
        mirrored = ImageOps.mirror(self.image)
        buf = [0xFF] * (16 * self.height)
        pixels = mirrored.load()
        
        for y in range(self.height):
            for x in range(self.width):
                byte_index = int(x / 8) + y * 16
                bit_index = 7 - (x % 8)
                if pixels[x, y] == 0:
                    if byte_index < len(buf):
                        buf[byte_index] &= ~(1 << bit_index)
        
        code = f'''#!/usr/bin/env python3
"""
Generated by E-Paper Designer Pro
The first visual editor for e-paper displays!
"""
from waveshare_epd import epd2in13_V4

epd = epd2in13_V4.EPD()
epd.init()

buffer = [
'''
        for i in range(0, len(buf), 16):
            line = "    " + ", ".join(f"0x{b:02X}" for b in buf[i:i+16])
            if i + 16 < len(buf):
                line += ","
            code += line + "\n"
        
        code += ''']

epd.display(buffer)
epd.sleep()
print("Display updated!")
'''
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".py",
            filetypes=[("Python files", "*.py"), ("All files", "*.*")]
        )
        if filename:
            with open(filename, 'w') as f:
                f.write(code)
            self.info_label.config(text=f"Exported code: {filename}")
    
    def show_shortcuts(self):
        shortcuts = """
Keyboard Shortcuts:

Ctrl+Z - Undo
Ctrl+Y - Redo
Ctrl+S - Save Project
Ctrl+O - Open Project
Ctrl+D - Duplicate Selected
Delete - Delete Selected

Arrow Keys - Nudge selected object (1px)
        
Mouse:
Left Click - Select/Drag object
Right Click - Delete object
"""
        messagebox.showinfo("Keyboard Shortcuts", shortcuts)
    
    def show_support(self):
        """Show support dialog with PayPal QR code"""
        dialog = tk.Toplevel(self.root)
        dialog.title("❤️ Support E-Paper Designer")
        dialog.geometry("450x550")
        dialog.resizable(False, False)
        
        # Title
        title = ttk.Label(dialog, text="☕ Buy Me a Coffee?", 
                         font=('Arial', 18, 'bold'))
        title.pack(pady=15)
        
        # Message
        message_text = """This tool is 100% FREE and always will be!

If E-Paper Designer saved you time or helped
your project, consider buying me a coffee! ☕

Every contribution helps keep development going
and new features coming!"""
        
        message = ttk.Label(dialog, text=message_text,
                           justify='center', font=('Arial', 10))
        message.pack(pady=10)
        
        # Try to load and display QR code
        try:
            # Load QR code (put qrcode.png next to the script)
            qr_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'qrcode.png')
            if os.path.exists(qr_path):
                qr_image = Image.open(qr_path)
                # Resize to reasonable size
                qr_image = qr_image.resize((200, 200), Image.LANCZOS)
                qr_photo = ImageTk.PhotoImage(qr_image)
                
                qr_label = ttk.Label(dialog, image=qr_photo)
                qr_label.image = qr_photo  # Keep reference
                qr_label.pack(pady=10)
                
                ttk.Label(dialog, text="📱 Scan with PayPal app or camera",
                         font=('Arial', 9), foreground='gray').pack()
            else:
                # Fallback if QR code not found
                ttk.Label(dialog, text="💰 PayPal QR Code",
                         font=('Arial', 12, 'bold')).pack(pady=10)
                ttk.Label(dialog, text="(Place qrcode.png next to script to display)",
                         font=('Arial', 8), foreground='gray').pack()
        except Exception as e:
            # If image loading fails
            ttk.Label(dialog, text="💰 Support via PayPal",
                     font=('Arial', 12, 'bold')).pack(pady=10)
        
        # Separator
        ttk.Separator(dialog, orient='horizontal').pack(fill='x', pady=15)
        
        # PayPal link button
        def open_paypal():
            import webbrowser
            webbrowser.open('https://paypal.me/aarondiltz')
        
        paypal_btn = ttk.Button(dialog, text="💰 Open PayPal in Browser", 
                               command=open_paypal)
        paypal_btn.pack(pady=5, ipadx=20, ipady=8)
        
        # Suggested amounts
        amounts_frame = ttk.Frame(dialog)
        amounts_frame.pack(pady=10)
        
        ttk.Label(amounts_frame, text="Suggested: ",
                 font=('Arial', 9), foreground='gray').pack(side='left')
        ttk.Label(amounts_frame, text="☕ $3  🍕 $10  🎉 $25  🚀 $50+",
                 font=('Arial', 9, 'bold')).pack(side='left')
        
        ttk.Label(dialog, text="(Any amount appreciated! Even $1 helps!)",
                 font=('Arial', 8), foreground='gray').pack()
        
        # Alternative support
        ttk.Separator(dialog, orient='horizontal').pack(fill='x', pady=10)
        
        alt_label = ttk.Label(dialog, text="""Can't donate? No problem! You can help by:
⭐ Starring on GitHub  •  🐛 Reporting bugs  •  📢 Telling friends""",
                             justify='center', font=('Arial', 9), foreground='gray')
        alt_label.pack(pady=5)
        
        # Close button
        ttk.Button(dialog, text="Maybe Later", 
                  command=dialog.destroy).pack(pady=15)
    
    def show_about(self):
        about = """
E-Paper Designer Pro v1.0

The FIRST visual drag-and-drop editor
for Waveshare e-paper displays!

🎨 100% FREE & Open Source

Created by Aaron Diltz
For the maker community

GitHub: solarsyn/Free-E-PaperDesignerPro
PayPal: paypal.me/aarondiltz

Features:
• Visual drag-and-drop editing
• WiFi, Bluetooth, Battery icons  
• Multiple display sizes
• Undo/Redo support
• Grid snapping & alignment
• Export to Python code
• Save/Load projects

━━━━━━━━━━━━━━━━━━━━━━━━

☕ Love it? Support development!
   Help → Support Development

⭐ Star on GitHub
🐛 Report bugs
📢 Share with friends

━━━━━━━━━━━━━━━━━━━━━━━━

No subscriptions. No trials. No limits.
Just a tool that works.

Thank you for using E-Paper Designer! ❤️
"""
        messagebox.showinfo("About E-Paper Designer Pro", about)


def main():
    root = tk.Tk()
    app = EpaperDesigner(root)
    root.mainloop()


if __name__ == "__main__":
    main()
