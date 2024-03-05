from tkinter import *
from tkinter import ttk
import sqlite3
import webbrowser
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Image


root = Tk()

class Relatorio():
    def Abrir_Relatorio(self):
        webbrowser.open("Clientes.pdf")
    def Gerar_Relatorio(self):
        self.canvas = canvas.Canvas("Clientes.pdf")
        
        self.canvas.setFont("Helvetica", 24)
        self.canvas.drawString(200, 790,'Relatorio de clientes')

        
        self.canvas.setFont("Times-Roman", 16)
        self.canvas.drawString(74, 730, 'Código:')
        self.canvas.drawString(174, 730, 'Nome:')
        self.canvas.drawString(274, 730, 'Cidade:')
        self.canvas.drawString(374, 730, 'Telefone:')
        self.canvas.drawString(474, 730, 'UF:')

        self.connectDB()

        relatorio = self.cursor.fetchall()

       
        Yposition = 700
        for linha in relatorio:
            self.canvas.drawString(74, Yposition, str(linha))
            Yposition -= 20

        self.disconnectDB()

        self.canvas.showPage()
        self.canvas.save()
        self.Abrir_Relatorio()
        
class Funcs(Relatorio):
    def connectDB(self):
        self.conn = sqlite3.connect('Clientes DB')
        self.cursor = self.conn.cursor()
    def disconnectDB(self):
        self.conn.close()
    def createDB(self):
        self.connectDB()
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS clientes(
                codigo INTEGER PRIMARY KEY,
                nome VARCHAR(40) NOT NULL,
                tel INTEGER (20),
                cidade VARCHAR(40),
                UF CHAR(2)
            );
        """)
        self.conn.commit()
        self.disconnectDB()
    def variaveis(self):
        self.codigo = self.codigo_entry.get()
        self.nome = self.nome_entry.get()
        self.cidade = self.cidade_entry.get()
        self.tel = self.tel_entry.get()
        self.UF = self.UF_entry.get()
    def limpa_tela(self):
        self.codigo_entry.delete(0, END)
        self.nome_entry.delete(0, END)
        self.cidade_entry.delete(0, END)
        self.tel_entry.delete(0, END)
        self.UF_entry.delete(0, END)
    def btn_novo(self):
        self.codigo = self.codigo_entry.get()
        self.nome = self.nome_entry.get()
        self.cidade = self.cidade_entry.get()
        self.tel = self.tel_entry.get()
        self.UF = self.UF_entry.get()
        
        self.connectDB(); print('Conectando ao banco de dados')
        
        self.cursor.execute("""INSERT INTO clientes ( nome, cidade, tel, UF) 
            values (?, ?, ?, ?) """, (self.nome, self.cidade, self.tel, self.UF))
        self.conn.commit()
        self.disconnectDB()
        self.select_treeview()
        self.limpa_tela()
    def select_treeview(self):
        self.treeview.delete(*self.treeview.get_children())
        self.connectDB()
        lista = self.cursor.execute(""" 
            SELECT codigo, nome, cidade, tel, UF FROM clientes
                ORDER BY codigo ASC; 
            """)
        for i in lista:
            self.treeview.insert("", END, values=i)
        self.disconnectDB
    def double_click(self, event):
       self.limpa_tela()
       self.treeview.selection()
       
       for n in self.treeview.selection():
           col1, col2, col3, col4, col5 = self.treeview.item(n, 'values')
           self.codigo_entry.insert(END, col1)
           self.nome_entry.insert(END, col2)
           self.cidade_entry.insert(END, col3)
           self.tel_entry.insert(END, col4)
           self.UF_entry.insert(END, col5)
    def btn_apagar(self):
           self.variaveis()
           self.connectDB()
           self.cursor.execute("""DELETE FROM clientes WHERE codigo = ? """, (self.codigo,))
           self.conn.commit()
           self.disconnectDB()
           self.limpa_tela()
           self.select_treeview()
    def alterar_cliente(self):
        self.variaveis()
        self.connectDB()
        self.cursor.execute(""" UPDATE clientes SET nome = ?, cidade  = ?, tel = ?, UF = ? WHERE codigo = ? """, (self.nome, self.cidade, self.tel, self.UF, self.codigo))
        self.conn.commit()
        self.disconnectDB()
        self.select_treeview()
        self.limpa_tela()
    def Btn_Buscar(self):
        self.variaveis()
        self.connectDB()
        self.treeview.delete(*self.treeview.get_children())
        lista = self.cursor.execute(""" SELECT codigo, nome, cidade, tel, UF FROM clientes
            WHERE codigo LIKE '%' || ? || '%'
                AND nome LIKE '%' || ? || '%'
                AND cidade LIKE '%' || ? || '%'
                AND tel LIKE '%' || ? || '%'
                AND UF LIKE '%' || ? || '%'
            ORDER BY codigo ASC;""", (self.codigo, self.nome, self.cidade, self.tel, self.UF))
        self.conn.commit()
        for i in lista:
          self.treeview.insert("", END, values=i)
        self.disconnectDB()
    def menu(self):
        menu_bar = Menu(self.root)
        self.root.config(menu = menu_bar)
        menu_options = Menu(menu_bar)
        menu_help = Menu(menu_bar)
        
        menu_bar.add_cascade(label = "Opções", menu = menu_options)
        menu_bar.add_cascade(label = "Ajuda", menu = menu_help)
        
        
        menu_options.add_command(label = "Tema")
        menu_options.add_command(label = "Imprimir", command = self.Gerar_Relatorio)
             
        menu_help.add_command(label = "Sobre")
        menu_help.add_command(label = "Como Usar")

class MeuApp(Funcs, Relatorio):
    def __init__(self):
        #Chamada das funcoes e Loop
        self.root = root
        self.janela()
        self.frame()
        self.Widgets_Frame1()
        self.createDB()
        self.treeview()
        self.select_treeview()
        self.limpa_tela()
        self.menu()
        
        root.mainloop()
        
    def janela(self):
        #Janela Mae
        self.root.title("Meu App")
        self.root.minsize(width=1080, height=720)
        self.root.configure(bg='#1e3743') 
        
    def frame(self):
        #Frame_Superior
        self.frame_1 = Frame(self.root, bg='#fffafa', bd=4, highlightbackground='#759fe6', highlightthickness=3)
        self.frame_1.place(relx=0.02, rely=0.01, relwidth=0.962, relheight=0.485)
        
        #Frame_Inferior
        self.frame_2 = Frame(self.root, bg='#fffafa', bd=4, highlightbackground='#759fe6', highlightthickness=3)
        self.frame_2.place(relx=0.02, rely=0.50, relwidth=0.962, relheight=0.49)
        
    def Widgets_Frame1(self):
        #Criação de Botões
        self.btn_limpar = Button(self.frame_1, text='Limpar', bg='#107db2', fg='white', font=('verdana', 8), command=self.limpa_tela)
        self.btn_limpar.place(relx=0.28, rely=0.07, relwidth=0.10, relheight=0.15)
        
        self.btn_buscar = Button(self.frame_1, text='Buscar', bg='#107db2', fg='white', font=('verdana', 8), command=self.Btn_Buscar)
        self.btn_buscar.place(relx=0.18, rely=0.07, relwidth=0.1, relheight=0.15)
        
        self.btn_novo = Button(self.frame_1, text='Novo', bg='#107db2', fg='white', font=('verdana', 8), command=self.btn_novo)
        self.btn_novo.place(relx=0.52, rely=0.07, relwidth=0.1, relheight=0.15)
              
        self.btn_alterar = Button(self.frame_1, text='Alterar', bg='#107db2', fg='white', font=('verdana', 8), command=self.alterar_cliente)
        self.btn_alterar.place(relx=0.62, rely=0.07, relwidth=0.1, relheight=0.15)      
              
        self.btn_apagar = Button(self.frame_1, text='Apagar', bg='#107db2', fg='white', font=('verdana', 8), command=self.btn_apagar)
        self.btn_apagar.place(relx=0.72, rely=0.07, relwidth=0.1, relheight=0.15)
        
        #Criação labels e entradas
        self.lbl_codigo = Label(self.frame_1, text='Código', bg='#fffafa', font= ('verdana', 8))
        self.lbl_codigo.place(relx=0.01, rely=0.07)
        
        self.codigo_entry = Entry(self.frame_1)
        self.codigo_entry.place(relx=0.09, rely=0.07, relwidth=0.05)
        
        
        self.lbl_tel = Label(self.frame_1, text='Tel', bg='#fffafa', font= ('verdana', 8))
        self.lbl_tel.place(relx=0.01, rely=0.7)
        
        self.tel_entry = Entry(self.frame_1)
        self.tel_entry.place(relx=0.09, rely=0.7, relwidth=0.32)
        
                
        self.lbl_nome = Label(self.frame_1, text='Nome', bg='#fffafa', font= ('verdana', 8))
        self.lbl_nome.place(relx=0.01, rely=0.3)
        
        self.nome_entry = Entry(self.frame_1)
        self.nome_entry.place(relx=0.09, rely=0.3, relwidth=0.82)
        
        
        self.lbl_cidade = Label(self.frame_1, text='Cidade', bg='#fffafa', font= ('verdana', 8))
        self.lbl_cidade.place(relx=0.01, rely=0.5)
        
        self.cidade_entry = Entry(self.frame_1)
        self.cidade_entry.place(relx=0.09, rely=0.5,relwidth=0.81)
        
        
        self.lbl_UF = Label(self.frame_1, text='UF', bg='#fffafa', font= ('verdana', 8))
        self.lbl_UF.place(relx=0.52, rely=0.7)
        
        self.UF_entry = Entry(self.frame_1)
        self.UF_entry.place(relx=0.56, rely=0.7, relwidth=0.05)
        
        
        #Criação do Treeview
    def treeview(self):
        self.treeview = ttk.Treeview(self.frame_2, height=3, column=('col1', 'col2', 'col3', 'col4', 'col5'))
        self.treeview.heading('#0', text='')
        self.treeview.heading('#1', text='Código')
        self.treeview.heading('#2', text='Nome')
        self.treeview.heading('#3', text='Cidade')
        self.treeview.heading('#4', text='Telefone')
        self.treeview.heading('#5', text='UF')
        
        self.treeview.column('#0', width=1)
        self.treeview.column('#1', width=30)
        self.treeview.column('#2', width=200)
        self.treeview.column('#3', width=150)
        self.treeview.column('#4', width=100)
        self.treeview.column('#5', width=20)
        
        
        self.treeview.place(relx=0.01, rely=0.05, relwidth=0.95, relheight=0.90)
        
        #ScrollBar
        self.scrollbar = Scrollbar(self.frame_2, orient='vertical')
        self.treeview.configure(yscroll=self.scrollbar.set)
        self.scrollbar.place(relx=0.96, rely=0.05, relheight=0.96)
        self.treeview.bind("<Double-1>", self.double_click)
        
#Iniciar o aplicativo        
MeuApp()