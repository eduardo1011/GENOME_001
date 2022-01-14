from tkinter import ttk
from tkinter import *
import tkinter
from tkinter import messagebox
from tkinter import filedialog
import tkinter.colorchooser
import os, subprocess

def buildjobs():
    ls=[]
    for i in os.listdir("./"):
        if re.search('Blast_DB_[0-9]{1,5}',str(i)):
            ls.append(i)
    if ls == []:
        new_folder='Blast_DB_1'
        xoxo='1'
        os.makedirs('Blast_DB_1',exist_ok=True)
    else:
        nnn=max([int(x) for x in re.findall('[0-9]{1,5}',str(ls))])
        xoxo=str(nnn+1)
        nnn=str(nnn)
        old_folder=''.join(re.findall('Blast_DB_'+nnn,str(ls)))
        new_folder=re.sub(nnn,xoxo,old_folder)
        os.makedirs(new_folder,exist_ok=True)
    return new_folder

import ctypes

ctypes.windll.shcore.SetProcessDpiAwareness(1)

root = Tk()
#root.tk.call('tk', 'scaling', 1.5)
root.title("BlasPyt")
root.geometry("570x770")
#root.iconbitmap(r'ncbi.ico')
#root.resizable(0, 0) # fija las dimensiones de la ventana
root.configure(background='white')
menubar = Menu(root)

blanco = Label(root, text=" ", bg = 'white')
blanco.grid(column=0, row=0)

uno = Label(root, text="Building a BLAST Database", font=("Arial", 8, "bold"), fg = 'darkblue', bg = 'white')
uno.grid(column=1, row=0, sticky= 'W')

tool = LabelFrame(root, text = "1. Sequence type", font=("Arial", 7))
tool.grid(column=1, row=1, sticky= 'WN')
tool.configure(background='white')

method = IntVar()
tipos = ['Nucleotide', 'Protein']
metodo = {0:'nucl', 1:'prot'}
for i, tips in enumerate(tipos):
    once = Radiobutton(tool, text='         '+tips+'           ', font=("Arial", 8), cursor="hand2", borderwidth=1,
                       indicatoron=0, selectcolor='darkblue', bg = 'silver',  fg = 'white',
                       variable=method, value=i)
    once.grid(column=i, row=0, sticky= 'WE')


def getFilePath():
    file_path = filedialog.askopenfilename()
    filePath.set(file_path)
    labebl.configure(text = ' '+file_path.split('/')[-1][0:37]+'...')

ffile = LabelFrame(root, text = "2. File", font=("Arial", 7))
ffile.grid(column=1, row=2, rowspan = 2, sticky= 'WEN')
ffile.configure(background='white')


filePath = StringVar()
subir_archivo1 = Radiobutton(ffile, text="            Upload:                      ", bg = 'white',
                indicatoron=0, selectcolor='darkblue', fg="white", borderwidth = 1,
                font=("Arial", 7), cursor="hand2", command=getFilePath)
subir_archivo1.grid(column=0, row=0, sticky= 'W')

labebl = Label(ffile, text= '', font=("Arial", 7), fg="black", bg = 'white')
labebl.grid(column = 0, row = 1, sticky= 'W')


running = StringVar()
running.set('         RUN                    ')
root.update()

def buildDB():
    running.set('         RUNING              ')
    botonrun.config(background= 'red')
    root.update()
    
    folder = buildjobs()
    labeb2.configure(text = ' DB: '+folder+'  ')
            
    makedb = subprocess.check_output(['makeblastdb', '-in', filePath.get(), '-dbtype', metodo[method.get()],
                                      '-parse_seqids',
                                      '-out', folder+'/'+filePath.get().split('/')[-1].split('.')[0]])
    
    messagebox.showinfo('Status', makedb.decode())

    nums = {}
    db = {}
    for i in os.listdir("./"):
        if re.search('Blast_DB_[0-9]{1,5}',str(i)):
            numero = i.split('_')[-1]
            nums[int(numero)] = i
            db[i] = os.listdir(i)[0].split('.')[0][0:20]+'...'

    LS = []
    for nu in sorted(list(nums.keys())):
        LS.append(nums[nu])
    
    
    text.insert(0, LS[-1]+': '+db[LS[-1]])
    
    running.set('         RUN                    ')
    botonrun.config(background= 'darkblue')
    root.update()

out = LabelFrame(root, text = "3. Output", font=("Arial", 7))
out.grid(column=1, row=5, sticky= 'WNE')
out.configure(background='white')
    
botonrun = Button(out, textvariable= running, bg="darkblue", fg="white", borderwidth=1,
                font=("Arial", 8), command = buildDB, cursor="hand2")
botonrun.grid(column = 0, row = 0, sticky= 'W')

labeb2 = Label(out, text= '            ', font=("Arial", 7), fg="grey", bg = 'white')
labeb2.grid(column = 1, row = 0, sticky= 'WE')


nums = {}
db = {}
for i in os.listdir("./"):
    if re.search('Blast_DB_[0-9]{1,5}',str(i)):
        numero = i.split('_')[-1]
        nums[int(numero)] = i
        db[i] = os.listdir(i)[0].split('.')[0][0:20]

LS = []
for nu in list(reversed(sorted(list(nums.keys())))):
    LS.append(nums[nu]+': '+db[nums[nu]][0:20]+'...')

blanco = Label(root, text=" ", bg = 'white')
blanco.grid(column=2, row=0)


opcionesplot = LabelFrame(root, text = "Databases built", font=("Arial", 7))
opcionesplot.grid(column=2, row=1, rowspan = 8, sticky= 'NW')
opcionesplot.configure(background='white')

items = StringVar()
items.set(LS)
text = Listbox(opcionesplot, font=("Arial", 7), width = 37, height = 8, listvariable=items)
text.grid(column=0, sticky= 'WN')


####################################
blanco = Label(root, text=" ", bg = 'white')
blanco.grid(column=0, row=6)


dos = Label(root, text="BLAST", font=("Arial", 8, "bold"), fg = 'darkblue', bg = 'white')
dos.grid(column=1, row=7, sticky= 'W')

tooll = LabelFrame(root, text = "1. Program Selection", font=("Arial", 7))
tooll.grid(column=1, row=8, columnspan = 2, sticky= 'WN')
tooll.configure(background='white')

programa = IntVar()
progs = ['blastn', 'blastp', 'blastx', 'tblastn', 'tblastx']
programas_correspondencia = {0:'blastn', 1:'blastp', 2:'blastx', 3:'tblastn', 4:'tblastx'}

metodo = {0:'nucl', 1:'prot'}
for e, tipos in enumerate(progs):
    once = Radiobutton(tooll, text=' '+tipos+'  ', font=("Arial", 8), cursor="hand2", borderwidth=1,
                       indicatoron=0, selectcolor='darkblue', bg = 'silver',  fg = 'white',
                       variable=programa, value=e)
    once.grid(column=e, row=0, sticky= 'WE')

enter = LabelFrame(root, text = "2. FASTA sequence", font=("Arial", 7))
enter.grid(column=1, row=9, columnspan = 2, sticky= 'W')
enter.configure(background='white')

textBox=Text(enter, height=8, width=77, font=("Arial", 7), bd = 2, bg = 'lemonchiffon')
textBox.grid(column=0, row=0, columnspan = 2, sticky= 'W')


############
def getFilePath2():
    file_path2 = filedialog.askopenfilename()
    filePath2.set(file_path2)
    labeb22.configure(text = '  '+file_path2.split('/')[-1])


cuadro = LabelFrame(root, text = "", font=("Arial", 7))
cuadro.grid(column=1, row=10, columnspan = 2, sticky= 'WNE')
cuadro.configure(background='white') 


filePath2 = StringVar()
fileFind2 = Radiobutton(cuadro, text="     Or       Upload:                  ", bg = 'white',
                indicatoron=0, selectcolor='darkblue', fg="white", borderwidth = 1,
                font=("Arial", 7), cursor="hand2", command=getFilePath2)
fileFind2.grid(column=0, row=1, sticky= 'W')

labeb22 = Label(cuadro, text= '', font=("Arial", 7), fg="black", bg = 'white')
labeb22.grid(column = 1, row = 1, sticky= 'W')

#################

database = LabelFrame(root, text = "3. Select Folder", font=("Arial", 7))
database.grid(column=1, row=11, columnspan = 2, sticky= 'WNE')
database.configure(background='white')

def getFolderPath():
    folder_selected = filedialog.askdirectory()
    folderPath.set(folder_selected)
    printdatabase.configure(text = '  '+folder_selected.split('/')[-1])

folderPath = StringVar()
btnFind = Radiobutton(database, text="              Database                ", bg = 'white',
                indicatoron=0, selectcolor='darkblue', fg="white", borderwidth = 1,
                font=("Arial", 7), cursor="hand2", command=getFolderPath)
btnFind.grid(column=0, row=0,sticky= 'W')


printdatabase = Label(database, text= '', font=("Arial", 7), fg="black", bg = 'white')
printdatabase.grid(column = 1, row = 0, sticky= 'W')

#################

parametros = LabelFrame(root, text = "4. General Parameters", font=("Arial", 7))
parametros.grid(column=1, row=12, columnspan = 2, rowspan = 5, sticky= 'WNE')
parametros.configure(background='white')
parametros.option_add('*TCombobox*Listbox.font', ("Arial", 7))


par2 = Label(parametros, text= 'Expect threshold', font=("Arial", 7), fg="black", bg = 'white')
par2.grid(column = 0, row = 0, sticky= 'W')
Evalue = Entry(parametros, bd =2, width = 20, font=("Arial", 7)) # para introducir titulo de la barra
Evalue.grid(column = 1, row = 0, sticky= 'W')
Evalue.focus_set()

par1 = Label(parametros, text= 'max_target_seqs', font=("Arial", 7), fg="black", bg = 'white')
par1.grid(column = 0, row = 1, sticky= 'W')
Max_target = StringVar()
cinco222 = ttk.Combobox(parametros, textvariable = Max_target, font=("Arial", 7),
                     values = [str(i) for i in list(range(1, 501))], width=17)
cinco222.grid(column=1, row=1, sticky= S+W)
cinco222.current(45)


par3 = Label(parametros, text= 'max_hsps', font=("Arial", 7), fg="black", bg = 'white')
par3.grid(column = 0, row = 2, sticky= 'W')
Max_hsps = StringVar()
cinco2222 = ttk.Combobox(parametros, textvariable = Max_hsps, font=("Arial", 7),
                     values = [str(i) for i in list(range(1, 501))], width=17)
cinco2222.grid(column=1, row=2, sticky= S+W)
cinco2222.current(45)


par4 = Label(parametros, text= 'Matrix', font=("Arial", 7), fg="black", bg = 'white')
par4.grid(column = 0, row = 3, sticky= 'W')
matrix = StringVar()
cinco2222 = ttk.Combobox(parametros, textvariable = matrix, font=("Arial", 7),
                     values = ['PAM30', 'PAM70', 'PAM250', 'BLOSUM80', 'BLOSUM62', 'BLOSUM45',
                               'BLOSUM50', 'BLOSUM90'], width=17)
cinco2222.grid(column=1, row=3, sticky= S+W)
cinco2222.current(4)


par5 = Label(parametros, text= 'Output File', font=("Arial", 7), fg="black", bg = 'white')
par5.grid(column = 0, row = 4, sticky= 'W')

name_output = Entry(parametros, bd =2, width = 20, font=("Arial", 7)) # para introducir titulo de la barra
name_output.grid(column = 1, row = 4, sticky= 'W')
name_output.focus_set()


#fileout = IntVar()
#modos = ['Txt', 'Tsv', 'Excel']
#archivo_correspondencia = {0:'Txt', 1:'Tsv', 2:'Excel'}
#ee = 2
#for e, tipos in enumerate(modos):
#    doce = Radiobutton(parametros, text=' '+tipos+'  ', font=("Arial", 8), cursor="hand2", borderwidth=1,
#                       indicatoron=0, selectcolor='darkblue', bg = 'silver',  fg = 'white',
#                       variable=fileout, value=e)
#    doce.grid(column=ee, row=4, sticky= 'WE')
#    ee += 1


#################


running2 = StringVar()
running2.set('         RUN                    ')
root.update()

def runblast():
    running2.set('         RUNING              ')
    botonrun2.config(background= 'red')
    root.update()
    
    result=textBox.get("1.0","end")
    
    if ((len(result) > 2), (len(filePath2.get()) > 2)) == (False, False):
        messagebox.showinfo('Status', 'Paste or select Fasta sequence')
    else:
        if len(result) > 5:
            f = open('user_sequence.fasta', 'w')
            f.write(result)
            f.close()
            input_file = 'user_sequence.fasta'
            print(input_file)
        else:
            input_file = filePath2.get()
            print(input_file)


        if folderPath.get() == '':
            messagebox.showinfo('Status', 'Select a Database Folder')
        else:
            
            folder_de_database = folderPath.get()
            archivo_dentro = os.listdir(folder_de_database)[0].split('.')[0]
            database_location = folder_de_database+'/'+archivo_dentro
            print(database_location)
            if Evalue.get() == '':
                evalue = 1E-3
                print(evalue)
            else:
                evalue = Evalue.get()
                print(evalue)
            print(Max_target.get())
            print(Max_hsps.get())
            print(matrix.get())
            print(input_file)
            
            if name_output.get() == '':
                nombre_de_salida = 'Output_'+programas_correspondencia[programa.get()]+'.'+archivo_correspondencia[fileout.get()]
                print(nombre_de_salida)
            else:
                nombre_de_salida = name_output.get()
                print(nombre_de_salida)
            
            
            #print(archivo_correspondencia[fileout.get()])


            if programas_correspondencia[programa.get()] == 'blastn':
                subprocess.call(programas_correspondencia[programa.get()]+' -db '+database_location+' -query '+input_file+\
                                ' -evalue '+str(evalue)+' -outfmt "6 qacc sacc qlen slen length qstart qend sstart send score bitscore evalue pident nident mismatch positive gaps gapopen stitle" -max_target_seqs '+str(Max_target.get())+' -max_hsps '+str(Max_hsps.get())+' -out '+nombre_de_salida, shell = True)
            else:
                print(programas_correspondencia[programa.get()]+' -db '+database_location+' -query '+input_file+' -evalue '+str(evalue)+' -outfmt "6 qacc sacc qlen slen length qstart qend sstart send score bitscore evalue pident nident mismatch positive gaps gapopen stitle" -matrix '+matrix.get()+' -max_target_seqs '+str(Max_target.get())+' -max_hsps '+str(Max_hsps.get())+' -out '+nombre_de_salida+' -export_search_strategy AAAAAAAA.txt')
                subprocess.call(programas_correspondencia[programa.get()]+' -db '+database_location+' -query '+input_file+\
                                ' -evalue '+str(evalue)+' -outfmt "6 qacc sacc qlen slen length qstart qend sstart send score bitscore evalue pident nident mismatch positive gaps gapopen stitle" -matrix '+matrix.get()+' -max_target_seqs '+str(Max_target.get())+' -max_hsps '+str(Max_hsps.get())+' -out '+nombre_de_salida+' -export_search_strategy AAAAAAAA.txt', shell = True)


    running2.set('         RUN                    ')
    botonrun2.config(background= 'darkblue')
    root.update()

out2 = LabelFrame(root, text = "   Blast   ", font=("Arial", 7))
out2.grid(column=1, row=18, sticky= 'WN')
out2.configure(background='white')
    
botonrun2 = Button(out2, textvariable= running2, bg="darkblue", fg="white", borderwidth=1,
                font=("Arial", 8), command = runblast, cursor="hand2")
botonrun2.grid(column = 0, row = 0, sticky= 'W')


##################

root.mainloop()