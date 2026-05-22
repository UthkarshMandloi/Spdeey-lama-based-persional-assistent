with open("d:/temp/Spdeey-lama-based-persional-assistent/speedy.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

new_lines = []
imports_injected = False

for i, line in enumerate(lines):
    if line.startswith("engine = pyttsx3.init('sapi5')") and not imports_injected:
        new_lines.extend([
            "import threading\n",
            "import customtkinter as ctk\n",
            "\n",
            "app = None\n",
            "def gui_update_status(text):\n",
            "    if app:\n",
            "        try:\n",
            "            app.after(0, app.update_status, text)\n",
            "        except: pass\n",
            "def gui_log(msg):\n",
            "    print(msg)\n",
            "    if app:\n",
            "        try:\n",
            "            app.after(0, app.log_message, str(msg))\n",
            "        except: pass\n\n",
            "class JarvisUI(ctk.CTk):\n",
            "    def __init__(self):\n",
            "        super().__init__()\n",
            "        self.title('Speedy - Jarvis UI')\n",
            "        self.geometry('800x600')\n",
            "        self.configure(fg_color='#0a0a0a')\n",
            "        self.title_label = ctk.CTkLabel(self, text='J.A.R.V.I.S. SYSTEM ONLINE', font=('Courier New', 30, 'bold'), text_color='#00ffff')\n",
            "        self.title_label.pack(pady=20)\n",
            "        self.status_label = ctk.CTkLabel(self, text='INITIALIZING...', font=('Courier New', 18), text_color='#00ffff')\n",
            "        self.status_label.pack(pady=10)\n",
            "        self.log_box = ctk.CTkTextbox(self, width=700, height=400, font=('Courier New', 14), fg_color='#111111', text_color='#00ffff')\n",
            "        self.log_box.pack(pady=20)\n",
            "    def update_status(self, text):\n",
            "        self.status_label.configure(text=text)\n",
            "    def log_message(self, msg):\n",
            "        self.log_box.insert('end', msg + '\\n')\n",
            "        self.log_box.see('end')\n\n"
        ])
        imports_injected = True
        new_lines.append(line)
    elif "def speak(audio):" in line:
        new_lines.append(line)
        new_lines.append("    gui_log(f'Speedy: {audio}')\n")
    elif "print('Listening......')" in line:
        new_lines.append(line.replace("print", "gui_log"))
        new_lines.append("        gui_update_status('LISTENING...')\n")
    elif "print('recognizing......')" in line:
        new_lines.append(line.replace("print", "gui_log"))
        new_lines.append("            gui_update_status('RECOGNIZING...')\n")
    elif "print(f\"usersaid:{command}\\n\")" in line:
        new_lines.append("            gui_log(f'User: {command}')\n")
    elif line.startswith("wishme()"):
        new_lines.append("def assistant_loop():\n")
        new_lines.append("    " + line)
    elif i > 163:
        new_lines.append("    " + line)
    else:
        new_lines.append(line)

new_lines.extend([
    "\n",
    "if __name__ == '__main__':\n",
    "    app = JarvisUI()\n",
    "    t = threading.Thread(target=assistant_loop, daemon=True)\n",
    "    t.start()\n",
    "    app.mainloop()\n"
])

with open("d:/temp/Spdeey-lama-based-persional-assistent/speedy.py", "w", encoding="utf-8") as f:
    f.writelines(new_lines)
