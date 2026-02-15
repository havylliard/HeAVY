import os
import sys
import zipfile
import webbrowser
import shutil
from datetime import datetime
import customtkinter as ctk
from PIL import Image
from tkinter import messagebox

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


LANGUAGES = {
    "Português": {
        "map_tab": "Atualizar Mapa", "portal_tab": "Res. Backup", "play": "JOGAR", "root": "ABRIR PASTA RAIZ", "launcher": "LAUNCHER",
        "site": "SITE", "forum": "FÓRUM", "map_title": "ATUALIZAR MAPA (CHUNKS)", 
        "patch_warn": "⚠️ AVISO: Chunks em mapas pré-WordGen 2 (Patch 3.0) podem quebrar!",
        "file_col": "ARQUIVO (.BIN)", "date_col": "DATA / HORA (RECENTES NO TOPO)", 
        "warn_1": "1 - PROTEÇÃO DE FARMS: Salve e saia no local para o arquivo subir ao topo.",
        "warn_2": "2 - SPAWN: Arquivos em vermelho são o início do mundo.", "warn_3": "3 - RECUPERAÇÃO: Use 'Restaurar Backup' em caso de erro.",
        "btn_del": "EXCLUIR SELECIONADOS", "btn_res": "Restaurar Backup", "btn_upd": "Atualizar Lista",
        "portal_title": "RECUPERAÇÃO DE MUNDO", "action_col": "AÇÃO", "restore_warn": "A restauração substitui o universo atual pelo ZIP selecionado.",
        "btn_restore": "RESTAURAR", "confirm_del": "Excluir arquivos?", "confirm_res": "Restaurar último backup?", "success": "Concluído!",
        "spawn_txt": "[0.0 SPAWN]", "base_txt": "[0.1 POSSÍVEL BASE]"
    },
    "English": {
        "map_tab": "Update Map", "portal_tab": "Res. Backup", "play": "PLAY", "root": "OPEN ROOT FOLDER", "launcher": "LAUNCHER",
        "site": "SITE", "forum": "FORUM", "map_title": "UPDATE MAP (CHUNKS)", 
        "patch_warn": "⚠️ WARNING: Chunks in pre-WordGen 2 maps (Patch 3.0) may break!",
        "file_col": "FILE (.BIN)", "date_col": "DATE / TIME (NEWEST ON TOP)", 
        "warn_1": "1 - FARM PROTECTION: Save and exit on site to bring the file to top.",
        "warn_2": "2 - SPAWN: Files in red are the world start.", "warn_3": "3 - RECOVERY: Use 'Restore Backup' if needed.",
        "btn_del": "DELETE SELECTED", "btn_res": "Restore Backup", "btn_upd": "Refresh List",
        "portal_title": "WORLD RECOVERY", "action_col": "ACTION", "restore_warn": "Restoration replaces current universe with ZIP.",
        "btn_restore": "RESTORE", "confirm_del": "Delete files?", "confirm_res": "Restore last backup?", "success": "Done!",
        "spawn_txt": "[0.0 SPAWN]", "base_txt": "[0.1 POSSIBLE BASE]"
    },
    "Español": {
        "map_tab": "Actualizar Mapa", "portal_tab": "Res. Backup", "play": "JUGAR", "root": "ABRIR CARPETA RAÍZ", "launcher": "LAUNCHER",
        "site": "SITIO", "forum": "FORO", "map_title": "ACTUALIZAR MAPA (CHUNKS)", 
        "patch_warn": "⚠️ AVISO: ¡Chunks en mapas pre-WordGen 2 (Patch 3.0) pueden romperse!",
        "file_col": "ARCHIVO (.BIN)", "date_col": "FECHA / HORA (RECIENTES ARRIBA)", 
        "warn_1": "1 - PROTECCIÓN DE FARMS: Guarde y salga para subir el archivo.",
        "warn_2": "2 - SPAWN: Archivos en rojo son el inicio del mundo.", "warn_3": "3 - RECUPERACIÓN: Use 'Restaurar Copia' en caso de error.",
        "btn_del": "ELIMINAR SELECCIONADOS", "btn_res": "Restaurar Copia", "btn_upd": "Actualizar Lista",
        "portal_title": "RECUPERACIÓN DE MUNDO", "action_col": "ACCIÓN", "restore_warn": "La restauración reemplaza el universo actual por el ZIP.",
        "btn_restore": "RESTAURAR", "confirm_del": "¿Eliminar archivos?", "confirm_res": "¿Restaurar última copia?", "success": "¡Hecho!",
        "spawn_txt": "[0.0 SPAWN]", "base_txt": "[0.1 POSIBLE BASE]"
    },
    "Русский": {
        "map_tab": "Обновить карту", "portal_tab": "Res. Backup", "play": "ИГРАТЬ", "root": "ОТКРЫТЬ КОРЕНЬ", "launcher": "LAUNCHER",
        "site": "САЙТ", "forum": "ФОРУМ", "map_title": "ОБНОВЛЕНИЕ КАРТЫ (ЧАНКИ)", 
        "patch_warn": "⚠️ ВНИМАНИЕ: Чанки в картах до WordGen 2 (Patch 3.0) могут сломаться!",
        "file_col": "ФАЙЛ (.BIN)", "date_col": "ДАТА / ВРЕМЯ (НОВЫЕ СВЕРХУ)", 
        "warn_1": "1 - ЗАЩИТА ФЕРМ: Сохранитесь и выйдите, чтобы файл поднялся вверх.",
        "warn_2": "2 - СПАУН: Красные файлы — это начало мира.", "warn_3": "3 - ВОССТАНОВЛЕНИЕ: Используйте 'Восстановить бэкап'.",
        "btn_del": "УДАЛИТЬ ВЫБРАННОЕ", "btn_res": "Восстановить бэкап", "btn_upd": "Обновить список",
        "portal_title": "ВОССТАНОВЛЕНИЕ МИРА", "action_col": "ДЕЙСТВИЕ", "restore_warn": "Восстановление заменяет вселенную выбранным ZIP.",
        "btn_restore": "ВОССТАНОВИТЬ", "confirm_del": "Удалить файлы?", "confirm_res": "Восстановить бэкап?", "success": "Готово!",
        "spawn_txt": "[0.0 SPAWN]", "base_txt": "[0.1 ВОЗМ. БАЗА]"
    },
    "Français": {
        "map_tab": "Mise à jour", "portal_tab": "Res. Backup", "play": "JOUER", "root": "OUVRIR RACINE", "launcher": "LAUNCHER",
        "site": "SITE", "forum": "FORUM", "map_title": "MISE À JOUR DE LA CARTE", 
        "patch_warn": "⚠️ ATTENTION: Les chunks pré-WordGen 2 (Patch 3.0) peuvent casser!",
        "file_col": "FICHIER (.BIN)", "date_col": "DATE / HEURE (RÉCENTS EN HAUT)", 
        "warn_1": "1 - PROTECTION FARMS: Sauvegardez et quittez pour remonter le fichier.",
        "warn_2": "2 - SPAWN: Les fichiers en rouge sont le début du monde.", "warn_3": "3 - RÉCUPÉRATION: Utilisez 'Restaurer'.",
        "btn_del": "SUPPRIMER SÉLECTION", "btn_res": "Restaurer Backup", "btn_upd": "Actualiser",
        "portal_title": "RÉCUPÉRATION DU MONDE", "action_col": "ACTION", "restore_warn": "La restauration remplace l'univers par le ZIP.",
        "btn_restore": "RESTAURER", "confirm_del": "Supprimer?", "confirm_res": "Restaurer sauvegarde?", "success": "Terminé!",
        "spawn_txt": "[0.0 SPAWN]", "base_txt": "[0.1 BASE POSSIBLE]"
    },
    "हिन्दी": {
        "map_tab": "मानचित्र अपडेट", "portal_tab": "Res. Backup", "play": "खेलें", "root": "रूट फोल्डर", "launcher": "LAUNCHER",
        "site": "साइट", "forum": "फोरम", "map_title": "मानचित्र अपडेट (Chunks)", 
        "patch_warn": "⚠️ चेतावनी: पैच 3.0 से पहले के मानचित्र खराब हो सकते हैं!",
        "file_col": "फ़ाइल (.BIN)", "date_col": "समय (नया ऊपर)", 
        "warn_1": "1 - फ़ार्म सुरक्षा: फ़ाइल को ऊपर लाने के लिए सहेजें और बाहर निकलें।",
        "warn_2": "2 - स्पॉन: लाल फ़ाइलें विश्व की शुरुआत हैं।", "warn_3": "3 - रिकवरी: 'बैकअप रीस्टोर' का उपयोग करें।",
        "btn_del": "चुना हुआ हटाएं", "btn_res": "बैकअप रीस्टोर", "btn_upd": "सूची अपडेट",
        "portal_title": "विश्व रिकवरी", "action_col": "कार्रवाई", "restore_warn": "रीस्टोर वर्तमान डेटा को ज़िप से बदल देता है।",
        "btn_restore": "रीस्टोर", "confirm_del": "हटाएं?", "confirm_res": "बैकअप रीस्टोर करें?", "success": "हो गया!",
        "spawn_txt": "[0.0 SPAWN]", "base_txt": "[0.1 संभावित आधार]"
    },
    "日本語": {
        "map_tab": "マップ更新", "portal_tab": "Res. Backup", "play": "プレイ", "root": "ルートフォルダ", "launcher": "LAUNCHER",
        "site": "サイト", "forum": "フォーラム", "map_title": "マップ更新 (チャンク)", 
        "patch_warn": "⚠️ 警告: パッチ3.0以前のマップは壊れる可能性があります！",
        "file_col": "ファイル (.BIN)", "date_col": "日時 (新しい順)", 
        "warn_1": "1 - ファーム保護: ファイルを一番上にするには現地で保存して終了してください。",
        "warn_2": "2 - スポーン: 赤いファイルは世界の始まりです。", "warn_3": "3 - 復旧: 「バックアップ復元」を使用してください。",
        "btn_del": "選択削除", "btn_res": "バックアップ復元", "btn_upd": "リスト更新",
        "portal_title": "ワールド復旧", "action_col": "操作", "restore_warn": "復元すると現在のデータがZIPに置き換わります。",
        "btn_restore": "復元", "confirm_del": "削除しますか？", "confirm_res": "最新を復元しますか？", "success": "完了！",
        "spawn_txt": "[0.0 SPAWN]", "base_txt": "[0.1 拠点の可能性]"
    },
    "中文": {
        "map_tab": "更新地图", "portal_tab": "Res. Backup", "play": "开始游戏", "root": "打开根目录", "launcher": "LAUNCHER",
        "site": "网站", "forum": "论坛", "map_title": "更新地图 (区块)", 
        "patch_warn": "⚠️ 警告：Patch 3.0 之前的地图区块可能会损坏！",
        "file_col": "文件 (.BIN)", "date_col": "日期/时间 (最新在上)", 
        "warn_1": "1 - 农场保护：在位保存并退出以置顶文件。",
        "warn_2": "2 - 出生点：红色文件是世界起点。", "warn_3": "3 - 恢复：出错时请使用“还原备份”。",
        "btn_del": "删除所选", "btn_res": "还原备份", "btn_upd": "刷新列表",
        "portal_title": "世界恢复", "action_col": "操作", "restore_warn": "还原将用所选 ZIP 替换当前宇宙。",
        "btn_restore": "还原", "confirm_del": "确认删除？", "confirm_res": "还原最后备份？", "success": "完成！",
        "spawn_txt": "[0.0 SPAWN]", "base_txt": "[0.1 可能基地]"
    }
}

class HeAVYApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.current_lang = "Português"
        self.title("HeAVY")
        self.geometry("935x540")
        ctk.set_appearance_mode("dark")
        
        
        self.base_user_path = os.path.join(os.path.expanduser("~"), 'AppData', 'Roaming', 'Hytale', 'UserData')
        self.burns_path = os.path.join(self.base_user_path, 'Saves', 'Burns')
        self.chunks_path = os.path.join(self.burns_path, 'universe', 'worlds', 'default', 'chunks')
        self.heavy_backup_path = os.path.join(self.chunks_path, "HeAVY_Backups")
        self.hytale_backup_path = os.path.join(self.burns_path, 'backup')
        self.universe_path = os.path.join(self.burns_path, 'universe')
        
        self.launcher_dir = r"C:\Program Files\Hypixel Studios\Hytale Launcher"
        self.launcher_exe = os.path.join(self.launcher_dir, "hytale-launcher.exe")
        
        self.selected_files = {}
        self.active_tab = "mapa"
        self.setup_ui()

    def t(self, key):
        return LANGUAGES.get(self.current_lang, LANGUAGES["English"]).get(key, key)

    def change_lang(self, new_lang):
        self.current_lang = new_lang
        self.setup_ui()

    def create_menu_button(self, master, text, icon_name, command, width=180, height=35, fg_color="#2b2b2b", icon_size=(20, 20)):
        try:
            pil_img = Image.open(resource_path(f"assets/imgs/{icon_name}")).convert("RGBA")
            img = ctk.CTkImage(light_image=pil_img, dark_image=pil_img, size=icon_size)
        except: img = None
        return ctk.CTkButton(master, text=text, image=img, compound="left", command=command, width=width, height=height,
                             fg_color=fg_color, corner_radius=8, font=("Arial", 11, "bold"), anchor="w")

    def setup_ui(self):
        for widget in self.winfo_children(): widget.destroy()
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        
        self.sidebar = ctk.CTkFrame(self, width=220, corner_radius=0)
        self.sidebar.grid(row=0, column=0, rowspan=2, sticky="nsew")

        try:
            logo_h = ctk.CTkImage(Image.open(resource_path("assets/imgs/hytale2.png")).convert("RGBA"), size=(140, 80))
            ctk.CTkLabel(self.sidebar, image=logo_h, text="").pack(pady=(10, 10))
        except: pass

        self.create_menu_button(self.sidebar, self.t("map_tab"), "mapa.png", lambda: self.show_tab("mapa"), fg_color="#1f538d").pack(pady=4, padx=15)
        self.create_menu_button(self.sidebar, self.t("portal_tab"), "bug.png", lambda: self.show_tab("portal"), fg_color="#2d5a27").pack(pady=4, padx=15)

        self.sidebar_footer = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        self.sidebar_footer.pack(side="bottom", pady=10)
        row_web = ctk.CTkFrame(self.sidebar_footer, fg_color="transparent")
        row_web.pack(pady=(0, 5))
        self.create_menu_button(row_web, self.t("site"), "8b.png", lambda: webbrowser.open("https://8bits.tec.br"), 85, 28, icon_size=(16,16)).pack(side="left", padx=2)
        self.create_menu_button(row_web, self.t("forum"), "forum.png", lambda: webbrowser.open("https://8bits.tec.br/forum"), 85, 28, icon_size=(16,16)).pack(side="left", padx=2)

        
        self.header = ctk.CTkFrame(self, height=60, corner_radius=0, fg_color="#141414")
        self.header.grid(row=0, column=1, sticky="new")
        
        h_btns = ctk.CTkFrame(self.header, fg_color="transparent")
        h_btns.pack(side="left", padx=20, pady=5)
        self.create_menu_button(h_btns, self.t("play"), "hytale.png", self.open_game, 120, 38, "#28a745", (22,22)).pack(side="left", padx=5)
        self.create_menu_button(h_btns, self.t("root"), "pasta.png", lambda: os.startfile(self.base_user_path), 160, 38, icon_size=(18,18)).pack(side="left", padx=5)
        self.create_menu_button(h_btns, self.t("launcher"), "pasta.png", lambda: os.startfile(self.launcher_dir), 110, 38, icon_size=(18,18)).pack(side="left", padx=5)

        self.lang_menu = ctk.CTkOptionMenu(self.header, values=list(LANGUAGES.keys()), command=self.change_lang, width=120, height=25)
        self.lang_menu.set(self.current_lang)
        self.lang_menu.pack(side="right", padx=20, pady=15)

        
        self.content_frame = ctk.CTkFrame(self, corner_radius=12, fg_color="#1e1e1e", border_width=2, border_color="#333")
        self.content_frame.grid(row=0, column=1, sticky="nsew", padx=15, pady=(70, 75))
        
        
        self.general_footer = ctk.CTkFrame(self, fg_color="transparent")
        self.general_footer.grid(row=0, column=1, sticky="s", pady=(0, 10)) 
        try:
            heavy_logo_img = Image.open(resource_path("assets/imgs/Heavy.png")).convert("RGBA")
            heavy_logo = ctk.CTkImage(heavy_logo_img, size=(120, 55))
            logo_label = ctk.CTkLabel(self.general_footer, image=heavy_logo, text="", cursor="hand2")
            logo_label.pack()
            logo_label.bind("<Button-1>", lambda e: webbrowser.open("https://instagram.com/HAVYLLIARD"))
        except: pass

        self.show_tab(self.active_tab)

    def show_tab(self, tab_name):
        self.active_tab = tab_name
        for widget in self.content_frame.winfo_children(): widget.destroy()
        if tab_name == "mapa": self.render_map_tab()
        elif tab_name == "portal": self.render_portal_tab()

    def render_map_tab(self):
        ctk.CTkLabel(self.content_frame, text=self.t("map_title"), font=("Arial", 16, "bold")).pack(pady=(10, 2))
        ctk.CTkLabel(self.content_frame, text=self.t("patch_warn"), font=("Arial", 10, "bold"), text_color="#ff4444").pack(pady=(0, 10))

        h_table = ctk.CTkFrame(self.content_frame, fg_color="#141414", height=25)
        h_table.pack(fill="x", padx=15, pady=(0, 0))
        ctk.CTkLabel(h_table, text=self.t("file_col"), width=220, anchor="w", font=("Arial", 10, "bold")).pack(side="left", padx=35)
        ctk.CTkLabel(h_table, text=self.t("date_col"), width=300, anchor="w", font=("Arial", 10, "bold")).pack(side="left")
        
        self.scroll = ctk.CTkScrollableFrame(self.content_frame, height=140, fg_color="#0f0f0f")
        self.scroll.pack(fill="both", expand=True, padx=15, pady=5)
        
        warn_box = ctk.CTkFrame(self.content_frame, fg_color="#2b2111", border_width=1, border_color="#ffcc00")
        warn_box.pack(fill="x", padx=15, pady=5)
        avisos = f"{self.t('warn_1')}\n{self.t('warn_2')}\n{self.t('warn_3')}"
        ctk.CTkLabel(warn_box, text=avisos, font=("Arial", 9, "bold"), justify="left", text_color="#ffcc00").pack(pady=5, padx=10)
        
        btn_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        btn_frame.pack(pady=10)
        ctk.CTkButton(btn_frame, text=self.t("btn_del"), fg_color="#8b0000", command=self.delete_selected, width=180).pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text=self.t("btn_res"), fg_color="#2d5a27", command=self.restore_last_heavy_backup, width=150).pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text=self.t("btn_upd"), command=self.load_chunks_ui, width=120).pack(side="left", padx=5)
        self.load_chunks_ui()

    def load_chunks_ui(self):
        for widget in self.scroll.winfo_children(): widget.destroy()
        self.selected_files = {}
        if not os.path.exists(self.chunks_path): return
        files = sorted([(f, os.path.getmtime(os.path.join(self.chunks_path, f))) 
                       for f in os.listdir(self.chunks_path) if f.endswith('.bin')], key=lambda x: x[1], reverse=True)
        for name, mtime in files:
            dt = datetime.fromtimestamp(mtime).strftime('%d/%m/%Y | %H:%M')
            is_00 = name in ["0.0.region.bin", "0.0.bin"]
            is_01 = name in ["0.1.region.bin", "0.1.bin"]
            color = "#FF4444" if (is_00 or is_01) else "#FFFFFF"
            
            row = ctk.CTkFrame(self.scroll, fg_color="transparent")
            row.pack(fill="x", pady=1)
            cb = ctk.CTkCheckBox(row, text="", width=20)
            cb.pack(side="left", padx=5)
            
            lbl_name = ctk.CTkLabel(row, text=name, width=220, anchor="w", text_color=color, font=("Consolas", 10))
            lbl_name.pack(side="left")
            ctk.CTkLabel(row, text=dt, width=160, anchor="w", font=("Consolas", 10)).pack(side="left")
            
            if is_00:
                ctk.CTkLabel(row, text=self.t("spawn_txt"), text_color="#FF4444", font=("Arial", 9, "bold")).pack(side="left")
            elif is_01:
                ctk.CTkLabel(row, text=self.t("base_txt"), text_color="#FF4444", font=("Arial", 9, "bold")).pack(side="left")
            self.selected_files[name] = cb

    def delete_selected(self):
        to_del = [n for n, cb in self.selected_files.items() if cb.get()]
        if not to_del: return
        if messagebox.askyesno("CONFIRMAR", self.t("confirm_del")):
            try:
                if not os.path.exists(self.heavy_backup_path): os.makedirs(self.heavy_backup_path)
                zip_n = os.path.join(self.heavy_backup_path, f"BACKUP_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip")
                with zipfile.ZipFile(zip_n, 'w') as z:
                    for f in os.listdir(self.chunks_path):
                        if f.endswith('.bin'): z.write(os.path.join(self.chunks_path, f), f)
                for f in to_del: os.remove(os.path.join(self.chunks_path, f))
                messagebox.showinfo("HeAVY", self.t("success"))
                self.load_chunks_ui()
            except Exception as e: messagebox.showerror("Erro", str(e))

    def restore_last_heavy_backup(self):
        if not os.path.exists(self.heavy_backup_path): return
        zips = sorted([f for f in os.listdir(self.heavy_backup_path) if f.endswith('.zip')], reverse=True)
        if not zips: return
        if messagebox.askyesno("HeAVY", self.t("confirm_res")):
            try:
                with zipfile.ZipFile(os.path.join(self.heavy_backup_path, zips[0]), 'r') as z:
                    z.extractall(self.chunks_path)
                messagebox.showinfo("HeAVY", self.t("success"))
                self.load_chunks_ui()
            except Exception as e: messagebox.showerror("Erro", str(e))

    def render_portal_tab(self):
        ctk.CTkLabel(self.content_frame, text=self.t("portal_title"), font=("Arial", 16, "bold")).pack(pady=10)
        h_table = ctk.CTkFrame(self.content_frame, fg_color="#141414", height=25)
        h_table.pack(fill="x", padx=15, pady=(5, 0))
        ctk.CTkLabel(h_table, text="BACKUP (.ZIP)", width=350, anchor="w", font=("Arial", 10, "bold")).pack(side="left", padx=20)
        ctk.CTkLabel(h_table, text=self.t("action_col"), width=100, anchor="w", font=("Arial", 10, "bold")).pack(side="left")
        self.portal_scroll = ctk.CTkScrollableFrame(self.content_frame, height=200, fg_color="#0f0f0f")
        self.portal_scroll.pack(fill="both", expand=True, padx=15, pady=5)
        ctk.CTkLabel(self.content_frame, text=self.t("restore_warn"), font=("Arial", 10), text_color="#ccc").pack(pady=5)
        self.load_portal_backups()

    def load_portal_backups(self):
        for widget in self.portal_scroll.winfo_children(): widget.destroy()
        if not os.path.exists(self.hytale_backup_path): return
        zips = sorted([(f, os.path.getmtime(os.path.join(self.hytale_backup_path, f))) 
                      for f in os.listdir(self.hytale_backup_path) if f.endswith('.zip')], key=lambda x: x[1], reverse=True)
        for name, mtime in zips:
            row = ctk.CTkFrame(self.portal_scroll, fg_color="transparent")
            row.pack(fill="x", pady=1)
            dt = datetime.fromtimestamp(mtime).strftime('%d/%m/%Y %H:%M')
            ctk.CTkLabel(row, text=f"{name}  ({dt})", width=380, anchor="w", font=("Consolas", 10)).pack(side="left", padx=10)
            ctk.CTkButton(row, text=self.t("btn_restore"), width=90, height=22, fg_color="#2d5a27", command=lambda n=name: self.restore_portal_backup(n)).pack(side="left", padx=5)

    def restore_portal_backup(self, zip_name):
        if messagebox.askyesno("CONFIRMAR", f"Restaurar {zip_name}?"):
            try:
                if os.path.exists(self.universe_path): shutil.rmtree(self.universe_path)
                with zipfile.ZipFile(os.path.join(self.hytale_backup_path, zip_name), 'r') as z:
                    z.extractall(self.universe_path)
                messagebox.showinfo("HeAVY", self.t("success"))
            except Exception as e: messagebox.showerror("Erro", str(e))

    def open_game(self):
        if os.path.exists(self.launcher_exe): os.startfile(self.launcher_exe)
        else: messagebox.showwarning("Erro", "Launcher not found.")

if __name__ == "__main__":
    app = HeAVYApp()
    app.mainloop()