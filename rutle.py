import tkinter as tk
from tkinter import messagebox
import random
import time
import math

class GelismisRulet:
    def __init__(self, root):
        self.root = root
        self.root.title("Casino Deluxe Roulette")
        self.root.geometry("600x650")
        self.root.configure(bg="#0b251a") # Koyu şık casino yeşili

        self.kasa = 10000
        self.secilen_tur = tk.StringVar(value="Sayı") # 'Sayı' veya 'Renk'
        self.secilen_renk = tk.StringVar(value="Kırmızı")
        self.gecmis_sayilar = []

        # Avrupa Ruleti Renkleri
        self.renkler = {0: "green"}
        self.kirmizilar = [1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36]
        for i in range(1, 37):
            self.renkler[i] = "red" if i in self.kirmizilar else "black"

        self.arayuz_tasarla()

    def arayuz_tasarla(self):
        # ÜST PANEL: Kasa ve Geçmiş İstatistikler
        ust_panel = tk.Frame(self.root, bg="#0b251a")
        ust_panel.pack(fill="x", padx=20, pady=10)

        self.label_kasa = tk.Label(ust_panel, text=f"BAKİYE: ${self.kasa:,}", font=("Helvetica", 18, "bold"), bg="#0b251a", fg="gold")
        self.label_kasa.pack(side="left")

        # Son 5 el istatistik tabelası
        self.tabela_frame = tk.Frame(ust_panel, bg="#0b251a")
        self.tabela_frame.pack(side="right")
        tk.Label(self.tabela_frame, text="GEÇMİŞ:", font=("Arial", 10, "bold"), bg="#0b251a", fg="white").pack(side="left", padx=5)
        self.tabela_guncelle()

        # ORTA PANEL: Görsel Rulet Çarkı Tuvali (Canvas)
        self.canvas = tk.Canvas(self.root, width=300, height=300, bg="#0b251a", highlightthickness=0)
        self.canvas.pack(pady=10)
        self.cark_ve_top_ciz("Hazır", "gray", 0, None)

        # ALT PANEL: Bahis Giriş Alanları
        bahis_frame = tk.LabelFrame(self.root, text=" BAHİS ALANI ", font=("Arial", 11, "bold"), bg="#143626", fg="gold", bd=2)
        bahis_frame.pack(fill="x", padx=30, pady=10)

        # 1. Bahis Türü Seçimi (Radyo Butonları)
        tk.Label(bahis_frame, text="Bahis Türü:", font=("Arial", 10, "bold"), bg="#143626", fg="white").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        
        rb_sayi = tk.Radiobutton(bahis_frame, text="Sayıya Oyna (35 Katı)", variable=self.secilen_tur, value="Sayı", bg="#143626", fg="white", selectcolor="#0b251a", font=("Arial", 10), command=self.girdi_aktiflik_ayarla)
        rb_sayi.grid(row=0, column=1, padx=5, sticky="w")
        
        rb_renk = tk.Radiobutton(bahis_frame, text="Renge Oyna (2 Katı)", variable=self.secilen_tur, value="Renk", bg="#143626", fg="white", selectcolor="#0b251a", font=("Arial", 10), command=self.girdi_aktiflik_ayarla)
        rb_renk.grid(row=0, column=2, padx=5, sticky="w")

        # 2. Sayı ve Renk Girdileri
        tk.Label(bahis_frame, text="Sayı Seç (0-36):", font=("Arial", 10, "bold"), bg="#143626", fg="white").grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.entry_sayi = tk.Entry(bahis_frame, font=("Arial", 11, "bold"), width=6, justify="center")
        self.entry_sayi.grid(row=1, column=1, padx=5, sticky="w")
        self.entry_sayi.insert(0, "17")

        tk.Label(bahis_frame, text="Renk Seç:", font=("Arial", 10, "bold"), bg="#143626", fg="white").grid(row=1, column=2, padx=10, pady=10, sticky="w")
        self.om_renk = tk.OptionMenu(bahis_frame, self.secilen_renk, "Kırmızı", "Siyah")
        self.om_renk.config(font=("Arial", 10), width=8, bg="#0b251a", fg="white", highlightthickness=0)
        self.om_renk.grid(row=1, column=3, padx=5, sticky="w")
        # 3. Para Miktarı Girişi
        tk.Label(bahis_frame, text="Miktar ($):", font=("Arial", 10, "bold"), bg="#143626", fg="white").grid(row=2, column=0, padx=10, pady=10, sticky="w")
        self.entry_miktar = tk.Entry(bahis_frame, font=("Arial", 11, "bold"), width=10, justify="center")
        self.entry_miktar.grid(row=2, column=1, padx=5, sticky="w")
        self.entry_miktar.insert(0, "500")

        # DURUM MESAJI VE DÖNDÜRME BUTONU
        self.label_durum = tk.Label(self.root, text="Lütfen bahsinizi belirleyin ve çarkı çevirin.", font=("Arial", 12, "italic"), bg="#0b251a", fg="#a3b899")
        self.label_durum.pack(pady=10)

        self.btn_cevir = tk.Button(self.root, text="🔥 ROULETTE WHEEL'I DÖNDÜR", font=("Helvetica", 14, "bold"), bg="#d4af37", fg="black", activebackground="#f3e5ab", bd=4, command=self.bahis_isleme)
        self.btn_cevir.pack(pady=10)
        
        self.girdi_aktiflik_ayarla()

    def girdi_aktiflik_ayarla(self):
        if self.secilen_tur.get() == "Sayı":
            self.entry_sayi.config(state="normal")
            self.om_renk.config(state="disabled")
        else:
            self.entry_sayi.config(state="disabled")
            self.om_renk.config(state="normal")

    def tabela_guncelle(self):
        for widget in self.tabela_frame.winfo_children():
            if widget.winfo_class() == 'Label' and widget.cget("text") != "GEÇMİŞ:":
                widget.destroy()

        for sayi in self.gecmis_sayilar[-5:]:
            renk = self.renkler[sayi]
            bg_c = "#cc0000" if renk == "red" else ("#111111" if renk == "black" else "#00aa00")
            lbl = tk.Label(self.tabela_frame, text=f" {sayi} ", font=("Arial", 10, "bold"), bg=bg_c, fg="white", bd=1, relief="ridge")
            lbl.pack(side="left", padx=2)

    def cark_ve_top_ciz(self, merkez_metin, daire_renk, cark_acisi, top_acisi):
        self.canvas.delete("all")
        cx, cy, r = 150, 150, 120
        self.canvas.create_oval(cx-r-10, cy-r-10, cx+r+10, cy+r+10, fill="#2a1a08", outline="#d4af37", width=5)
        
        for i in range(12):
            dilim_aci = (i * 30) + cark_acisi
            x1 = cx + r * math.cos(math.radians(dilim_aci))
            y1 = cy + r * math.sin(math.radians(dilim_aci))
            self.canvas.create_line(cx, cy, x1, y1, fill="#554433", width=1)

        self.canvas.create_oval(cx-r+15, cy-r+15, cx+r-15, cy+r-15, fill=daire_renk, outline="white", width=2)
        self.canvas.create_oval(cx-45, cy-45, cx+45, cy+45, fill="#0b251a", outline="#d4af37", width=2)
        self.canvas.create_text(cx, cy, text=merkez_metin, fill="white", font=("Helvetica", 24, "bold"))

        if top_acisi is not None:
            tr = r - 25
            tx = cx + tr * math.cos(math.radians(top_acisi))
            ty = cy + tr * math.sin(math.radians(top_acisi))
            self.canvas.create_oval(tx-7, ty-7, tx+7, ty+7, fill="#fdfefe", outline="#bdc3c7", width=1)

    def bahis_isleme(self):
        try:
            miktar = int(self.entry_miktar.get())
        except ValueError:
            messagebox.showerror("Hata", "Geçersiz bahis miktarı!")
            return

        if miktar <= 0 or miktar > self.kasa:
            messagebox.showerror("Hata", "Yetersiz bakiye veya geçersiz miktar!")
            return

        tür = self.secilen_tur.get()
        hedef_sayi = None

        if tür == "Sayı":
            try:
                hedef_sayi = int(self.entry_sayi.get())
                if hedef_sayi < 0 or hedef_sayi > 36: raise ValueError
            except ValueError:
                messagebox.showerror("Hata", "Sayı 0 ile 36 arasında olmalıdır!")
                return

        self.kasa -= miktar
        self.label_kasa.config(text=f"BAKİYE: ${self.kasa:,}")
        self.btn_cevir.config(state="disabled")
        self.label_durum.config(text="Rien ne va plus! (Top dönüyor...)", fg="gold")

        self.animasyon_baslat(tür, hedef_sayi, miktar)

    def animasyon_baslat(self, tür, hedef_sayi, miktar):
        cark_acisi = 0
        top_acisi = 0
        top_hizi = 35.0  
        cark_hizi = -5.0 

        while top_hizi > 0.5:
            cark_acisi = (cark_acisi + cark_hizi) % 360
            top_acisi = (top_acisi + top_hizi) % 360
            gecici_sayi = random.randint(0, 36)
            self.cark_ve_top_ciz(str(gecici_sayi), self.renkler[gecici_sayi], cark_acisi, top_acisi)
            self.root.update()
            top_hizi *= 0.94
            cark_hizi *= 0.95
            time.sleep(0.04)

        nihai_sayi = random.randint(0, 36)
        nihai_renk = self.renkler[nihai_sayi]
        self.cark_ve_top_ciz(str(nihai_sayi), nihai_renk, cark_acisi, top_acisi)
        
        self.gecmis_sayilar.append(nihai_sayi)
        self.tabela_guncelle()

        kazandi = False
        payout = 0
        renk_isimi = "KIRMIZI" if nihai_renk == "red" else ("SİYAH" if nihai_renk == "black" else "YEŞİL")

        if tür == "Sayı" and hedef_sayi == nihai_sayi:
            kazandi = True
            payout = miktar * 36
        elif tür == "Renk":
            tahmin_renk_eng = "red" if self.secilen_renk.get() == "Kırmızı" else "black"
            if tahmin_renk_eng == nihai_renk:
                kazandi = True
                payout = miktar * 2

        if kazandi:
            self.kasa += payout
            self.label_durum.config(text=f"🎉 KAZANDINIZ! Sonuç: {nihai_sayi} ({renk_isimi})", fg="#4ade80")
            messagebox.showinfo("Kazandınız!", f"Tebrikler! Masadan ${payout:,} çektiniz.")
        else:
            self.label_durum.config(text=f"Kaybettiniz. Sonuç: {nihai_sayi} ({renk_isimi})", fg="#f87171")

        if self.kasa <= 0:
            messagebox.showwarning("Müflis", "Hesabınızdaki para sıfırlandı! Kumarhane size $10,000 yeni kredi tanımladı.")
            self.kasa = 10000

        self.label_kasa.config(text=f"BAKİYE: ${self.kasa:,}")
        self.btn_cevir.config(state="normal")

if __name__ == "__main__":
    root = tk.Tk()
    uygulama = GelismisRulet(root)
    root.mainloop()
