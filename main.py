import os
import re
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.utils import get_color_from_hex

Window.clearcolor = get_color_from_hex('#1e1e1e')

class ZeyAntiApp(App):
    def build(self):
        self.title = "ZeyAnti Antivirus v1.0"
        self.signature_database = {
            r"os\.system\(['\"]shutdown": "Sistemi məcburi söndürmə əmri",
            r"eval\(base64": "Şifrələnmiş gizli kod icrası (Troyan)",
            r"keylogger|pynput\.keyboard": "Klaviaturadakı yazıları oğurlayan sistem"
        }
        
        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        header = Label(text="🛡️ ZeyAnti 🛡️", font_size='40sp', color=get_color_from_hex('#00FF00'), bold=True, size_hint_y=None, height=80)
        layout.add_widget(header)
        
        self.path_input = TextInput(text='C:\\Users\\ulviz\\OneDrive\\Desktop', multiline=False, font_size='18sp', background_color=get_color_from_hex('#333333'), foreground_color=[1,1,1,1], padding_y=(10,10))
        layout.add_widget(Label(text="Skan etmək istədiyiniz qovluq yolu:", color=[1,1,1,1], font_size='16sp'))
        layout.add_widget(self.path_input)
        
        scan_btn = Button(text="SKAN ET", font_size='22sp', background_color=get_color_from_hex('#008800'), background_normal='', bold=True, size_hint_y=None, height=70)
        scan_btn.bind(on_press=self.start_scan)
        layout.add_widget(scan_btn)
        
        self.result_view = ScrollView(size_hint=(1, 1))
        self.result_label = Label(text="Nəticələr burada görünəcək...", size_hint_y=None, color=[1,1,1,1], halign='left', valign='top', font_size='14sp', padding=(10,10))
        self.result_label.bind(texture_size=self.result_label.setter('size'))
        self.result_view.add_widget(self.result_label)
        layout.add_widget(self.result_view)
        
        return layout

    def start_scan(self, instance):
        folder_path = self.path_input.text.strip()
        self.result_label.text = f"[+] '{folder_path}' skan edilir...\n\n"
        
        if not os.path.exists(folder_path):
            self.result_label.text += "[🚨 XƏTA] Daxil edilən yol tapılmadı!"
            return

        detected_count = 0
        total_scanned = 0
        scan_results = ""

        for root, dirs, files in os.walk(folder_path):
            for file in files:
                total_scanned += 1
                full_path = os.path.join(root, file)
                try:
                    if os.path.getsize(full_path) > 10 * 1024 * 1024: continue
                    with open(full_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                    for pattern, description in self.signature_database.items():
                        if re.search(pattern, content, re.IGNORECASE):
                            scan_results += f"🛑 [TƏHLÜKƏ] {description}\n📍 Fayl: {file}\n\n"
                            detected_count += 1
                except: continue

        final_report = f"---------------------------------\n"
        final_report += f"✅ Skan tamamlandı!\n"
        final_report += f"🔍 Ümumi yoxlanılan: {total_scanned}\n"
        final_report += f"🚨 Tapılan təhlükə: {detected_count}\n"
        final_report += f"---------------------------------\n\n"
        
        self.result_label.text = final_report + scan_results

if __name__ == '__main__':
    ZeyAntiApp().run()
