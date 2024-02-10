import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from tkinter import StringVar


class Aplikacija:
    def __init__(self, master):
        self.master = master
        self.master.title("Aplikacija s Tkinterom i SQLite")

        # Povezivanje s bazom podataka
        self.conn = sqlite3.connect('baza_podataka.db')
        self.cur = self.conn.cursor()

        # Stvaranje tablica ako već ne postoje
        self.create_tables()

        # Stvaranje GUI-a
        self.create_gui()

    def create_tables(self):
        # Stvaranje tablice za korisnike
        self.cur.execute('''
            CREATE TABLE IF NOT EXISTS korisnici (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ime TEXT,
                prezime TEXT,
                email TEXT,
                broj_telefona TEXT,
                sektor TEXT,
                pozicija TEXT
            )
        ''')
        self.conn.commit()

    def create_gui(self):
        self.master.geometry("800x600")  

        style = ttk.Style()
        style.configure("TButton", padding=5, font=("Helvetica", 12))

        self.frame = ttk.Frame(self.master, padding="20")
        self.frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        korisnici_button = ttk.Button(self.frame, text="Prikazi korisnike", command=self.prikazi_korisnike)
        korisnici_button.grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)

        dodaj_korisnika_button = ttk.Button(self.frame, text="Dodaj korisnika", command=self.dodaj_korisnika)
        dodaj_korisnika_button.grid(row=0, column=1, padx=10, pady=10, sticky=tk.W)

        uredi_korisnika_button = ttk.Button(self.frame, text="Uredi korisnika", command=self.uredi_korisnika)
        uredi_korisnika_button.grid(row=0, column=2, padx=10, pady=10, sticky=tk.W)

        obrisi_korisnika_button = ttk.Button(self.frame, text="Obrisi korisnika", command=self.obrisi_korisnika)
        obrisi_korisnika_button.grid(row=0, column=3, padx=10, pady=10, sticky=tk.W)

        # Dodavanje Treeview-a
        self.tree = ttk.Treeview(self.master)
        self.tree["columns"] = ("ID", "Ime", "Prezime", "Email", "Broj telefona", "Sektor", "Pozicija")

        self.tree.column("#0", width=0, stretch=tk.NO)
        self.tree.column("ID", anchor=tk.W, width=50)
        self.tree.column("Ime", anchor=tk.W, width=100)
        self.tree.column("Prezime", anchor=tk.W, width=100)
        self.tree.column("Email", anchor=tk.W, width=150)
        self.tree.column("Broj telefona", anchor=tk.W, width=100)
        self.tree.column("Sektor", anchor=tk.W, width=100)
        self.tree.column("Pozicija", anchor=tk.W, width=100)

        self.tree.heading("#0", text="", anchor=tk.W)
        self.tree.heading("ID", text="ID", anchor=tk.W)
        self.tree.heading("Ime", text="Ime", anchor=tk.W)
        self.tree.heading("Prezime", text="Prezime", anchor=tk.W)
        self.tree.heading("Email", text="Email", anchor=tk.W)
        self.tree.heading("Broj telefona", text="Broj telefona", anchor=tk.W)
        self.tree.heading("Sektor", text="Sektor", anchor=tk.W)
        self.tree.heading("Pozicija", text="Pozicija", anchor=tk.W)

        self.tree.grid(row=1, column=0, padx=10, pady=10, columnspan=4)

    def prikazi_korisnike(self):
        self.cur.execute("SELECT * FROM korisnici")
        korisnici = self.cur.fetchall()

        for child in self.tree.get_children():
            self.tree.delete(child)

        for korisnik in korisnici:
            self.tree.insert("", tk.END, values=korisnik)

    def dodaj_korisnika(self):
        prozor_dodaj_korisnika = tk.Toplevel(self.master)
        prozor_dodaj_korisnika.title("Dodaj korisnika")

        label_ime = ttk.Label(prozor_dodaj_korisnika, text="Ime:")
        label_ime.grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)
        entry_ime = ttk.Entry(prozor_dodaj_korisnika)
        entry_ime.grid(row=0, column=1, padx=10, pady=10)

        label_prezime = ttk.Label(prozor_dodaj_korisnika, text="Prezime:")
        label_prezime.grid(row=1, column=0, padx=10, pady=10, sticky=tk.W)
        entry_prezime = ttk.Entry(prozor_dodaj_korisnika)
        entry_prezime.grid(row=1, column=1, padx=10, pady=10)

        label_email = ttk.Label(prozor_dodaj_korisnika, text="Email:")
        label_email.grid(row=2, column=0, padx=10, pady=10, sticky=tk.W)
        entry_email = ttk.Entry(prozor_dodaj_korisnika)
        entry_email.grid(row=2, column=1, padx=10, pady=10)

        label_broj_telefona = ttk.Label(prozor_dodaj_korisnika, text="Broj telefona:")
        label_broj_telefona.grid(row=3, column=0, padx=10, pady=10, sticky=tk.W)
        entry_broj_telefona = ttk.Entry(prozor_dodaj_korisnika)
        entry_broj_telefona.grid(row=3, column=1, padx=10, pady=10)

        # Dropdown meni za sektor
        label_sektor = ttk.Label(prozor_dodaj_korisnika, text="Sektor:")
        label_sektor.grid(row=4, column=0, padx=10, pady=10, sticky=tk.W)

        # Opcije za sektor
        opcije_sektora = ["sektor1", "sektor2", "sektor3"]

        # Varijabla za odabir sektora
        self.sektor_var = StringVar()
        self.sektor_var.set(opcije_sektora[0])  

        # Dropdown meni
        dropdown_sektor = ttk.Combobox(prozor_dodaj_korisnika, textvariable=self.sektor_var, values=opcije_sektora)
        dropdown_sektor.grid(row=4, column=1, padx=10, pady=10)

        label_pozicija = ttk.Label(prozor_dodaj_korisnika, text="Pozicija:")
        label_pozicija.grid(row=5, column=0, padx=10, pady=10, sticky=tk.W)
        entry_pozicija = ttk.Entry(prozor_dodaj_korisnika)
        entry_pozicija.grid(row=5, column=1, padx=10, pady=10)

        potvrdi_button = ttk.Button(prozor_dodaj_korisnika, text="Potvrdi", command=lambda: self.potvrdi_dodavanje_korisnika(prozor_dodaj_korisnika, entry_ime.get(), entry_prezime.get(), entry_email.get(), entry_broj_telefona.get(), self.sektor_var.get(), entry_pozicija.get()))
        potvrdi_button.grid(row=6, column=1, padx=10, pady=10)

    def potvrdi_dodavanje_korisnika(self, prozor_dodaj_korisnika, ime, prezime, email, broj_telefona, sektor, pozicija):
        if not ime or not prezime or not email or not broj_telefona or not sektor or not pozicija:
            messagebox.showwarning("Upozorenje", "Sva polja moraju biti popunjena.")
            return

        self.cur.execute("INSERT INTO korisnici (ime, prezime, email, broj_telefona, sektor, pozicija) VALUES (?, ?, ?, ?, ?, ?)", (ime, prezime, email, broj_telefona, sektor, pozicija))
        self.conn.commit()
        prozor_dodaj_korisnika.destroy()
        self.prikazi_korisnike()

    def uredi_korisnika(self):
        prozor_uredi_korisnika = tk.Toplevel(self.master)
        prozor_uredi_korisnika.title("Uredi korisnika")

        selektirani_item = self.tree.selection()

        if not selektirani_item:
            messagebox.showwarning("Upozorenje", "Molimo odaberite korisnika za uređivanje.")
            return

        korisnik_id = self.tree.item(selektirani_item)['values'][0]
        self.cur.execute("SELECT * FROM korisnici WHERE id=?", (korisnik_id,))
        korisnik = self.cur.fetchone()

        label_ime = ttk.Label(prozor_uredi_korisnika, text="Ime:")
        label_ime.grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)
        entry_ime = ttk.Entry(prozor_uredi_korisnika)
        entry_ime.insert(0, korisnik[1])
        entry_ime.grid(row=0, column=1, padx=10, pady=10)

        label_prezime = ttk.Label(prozor_uredi_korisnika, text="Prezime:")
        label_prezime.grid(row=1, column=0, padx=10, pady=10, sticky=tk.W)
        entry_prezime = ttk.Entry(prozor_uredi_korisnika)
        entry_prezime.insert(0, korisnik[2])
        entry_prezime.grid(row=1, column=1, padx=10, pady=10)

        label_email = ttk.Label(prozor_uredi_korisnika, text="Email:")
        label_email.grid(row=2, column=0, padx=10, pady=10, sticky=tk.W)
        entry_email = ttk.Entry(prozor_uredi_korisnika)
        entry_email.insert(0, korisnik[3])
        entry_email.grid(row=2, column=1, padx=10, pady=10)

        label_broj_telefona = ttk.Label(prozor_uredi_korisnika, text="Broj telefona:")
        label_broj_telefona.grid(row=3, column=0, padx=10, pady=10, sticky=tk.W)
        entry_broj_telefona = ttk.Entry(prozor_uredi_korisnika)
        entry_broj_telefona.insert(0, korisnik[4])
        entry_broj_telefona.grid(row=3, column=1, padx=10, pady=10)

        label_sektor = ttk.Label(prozor_uredi_korisnika, text="Sektor:")
        label_sektor.grid(row=4, column=0, padx=10, pady=10, sticky=tk.W)
        entry_sektor = ttk.Entry(prozor_uredi_korisnika)
        entry_sektor.insert(0, korisnik[5])
        entry_sektor.grid(row=4, column=1, padx=10, pady=10)

        label_pozicija = ttk.Label(prozor_uredi_korisnika, text="Pozicija:")
        label_pozicija.grid(row=5, column=0, padx=10, pady=10, sticky=tk.W)
        entry_pozicija = ttk.Entry(prozor_uredi_korisnika)
        entry_pozicija.insert(0, korisnik[6])
        entry_pozicija.grid(row=5, column=1, padx=10, pady=10)

        potvrdi_button = ttk.Button(prozor_uredi_korisnika, text="Potvrdi", command=lambda: self.potvrdi_uredi_korisnika(prozor_uredi_korisnika, korisnik_id, entry_ime.get(), entry_prezime.get(), entry_email.get(), entry_broj_telefona.get(), entry_sektor.get(), entry_pozicija.get()))
        potvrdi_button.grid(row=6, column=1, padx=10, pady=10, sticky=tk.E)

    def potvrdi_uredi_korisnika(self, prozor_uredi_korisnika, korisnik_id, ime, prezime, email, broj_telefona, sektor, pozicija):
        if not ime or not prezime or not email or not broj_telefona or not sektor or not pozicija:
            messagebox.showwarning("Upozorenje", "Sva polja moraju biti popunjena.")
            return

        self.cur.execute("UPDATE korisnici SET ime=?, prezime=?, email=?, broj_telefona=?, sektor=?, pozicija=? WHERE id=?", (ime, prezime, email, broj_telefona, sektor, pozicija, korisnik_id))
        self.conn.commit()
        prozor_uredi_korisnika.destroy()
        self.prikazi_korisnike()

    def obrisi_korisnika(self):
        selektirani_item = self.tree.selection()

        if not selektirani_item:
            messagebox.showwarning("Upozorenje", "Molimo odaberite korisnika za brisanje.")
            return

        odgovor = messagebox.askyesno("Potvrda brisanja", "Jeste li sigurni da želite obrisati odabranog korisnika?")

        if odgovor:
            korisnik_id = self.tree.item(selektirani_item)['values'][0]
            self.cur.execute("DELETE FROM korisnici WHERE id=?", (korisnik_id,))
            self.conn.commit()
            self.prikazi_korisnike()

if __name__ == "__main__":
    root = tk.Tk()
    aplikacija = Aplikacija(root)
    root.mainloop()
