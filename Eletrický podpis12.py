import os
import time
import zipfile
from os.path import basename
from tkinter import ttk,messagebox
from tkinter.scrolledtext import ScrolledText
from tkinter.ttk import Combobox
from tkinter import filedialog as fd
import random
import hashlib
import base64
from tkinter import *
from zipfile import ZipFile



def rabinMiller(n,d):

    a = random.randint (2,(n - 2) - 2)
    x = pow (a,int (d),n)  # a^d%n
    if x == 1 or x == n - 1:
        return True

    # čtverec x
    while d != n - 1:
        x = pow (x,2,n)
        d *= 2

        if x == 1:
            return False
        elif x == n - 1:
            return True

    # není prvočíslo
    return False


def isPrime(n):
    """
        návrat True, pokud n je prvočíslo,jinak vrácení k rabinMillerovi
    """

    # 0, 1, -čísla nejsou prvočísla
    if n < 2:
        return False

    # malá prvočísla pro rychlejší zpracování
    lowPrimes = [2,3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,71,73,79,83,89,97,101,103,107,109,113,127,131,137,
                 139,149,151,157,163,167,173,179,181,191,193,197,199,211,223,227,229,233,239,241,251,257,263,269,271,
                 277,281,283,293,307,311,313,317,331,337,347,349,353,359,367,373,379,383,389,397,401,409,419,421,431,
                 433,439,443,449,457,461,463,467,479,487,491,499,503,509,521,523,541,547,557,563,569,571,577,587,593,
                 599,601,607,613,617,619,631,641,643,647,653,659,661,673,677,683,691,701,709,719,727,733,739,743,751,
                 757,761,769,773,787,797,809,811,821,823,827,829,839,853,857,859,863,877,881,883,887,907,911,919,929,
                 937,941,947,953,967,971,977,983,991,997]

    # jestli je malé prvočísla
    if n in lowPrimes:
        return True

    # malé prvočísla dělíme na n
    for prime in lowPrimes:
        if n % prime == 0:
            return False

    # nacházení čísla c, jako c * 2 ^ r = n - 1
    c = n - 1  # c jako c n nedělitelná 2
    while c % 2 == 0:
        c /= 2  # udělání c liché

    # test jestli čísla nejsou prvočísla
    for i in range (128):
        if not rabinMiller (n,c):
            return False

    return True

def generateLargePrime(keysize):
    """
        vrátit náhodně velké prvočíslo bitů velikosti klíče
    """

    while True:
        num = random.randrange (2 ** (keysize - 1),2 ** keysize - 1)
        if (isPrime (num)):
            return num


def isCoPrime(p,q):
    """
        return True, pokud je gcd(p, q) 1 relativně prvočíslo
    """

    return gcd (p,q) == 1


def gcd(p,q):
    """
        euklidovský algoritmus k nalezení gcd p a q
    """

    while q:
        p,q = q,p % q
    return p


def egcd(a,b):
    s = 0;
    old_s = 1
    t = 1;
    old_t = 0
    r = b;
    old_r = a

    while r != 0:
        quotient = old_r // r
        old_r,r = r,old_r - quotient * r
        old_s,s = s,old_s - quotient * s
        old_t,t = t,old_t - quotient * t

    # vrácení gcd, x, y
    return old_r,old_s,old_t


def modularInv(a,b):
    gcd,x,y = egcd (a,b)

    if x < 0:
        x += b

    return x

def generateKeys(k=1024):
    e = d = n = 0

    # prvočísla nums, p & q
    p = generateLargePrime (k)
    q = generateLargePrime (k)

    n = p * q  # RSA Modul
    phiN = (p - 1) * (q - 1)

    # vybrání e
    # e je coprime s phiN & 1 < e <= phiN
    while True:
        e = random.randrange (2 ** (k - 1),2 ** k - 1)
        if (isCoPrime (e,phiN)):
            break

    # vybrání d
    # d je mod inv z e s phiN, e * d (mod phiN) = 1
    d = modularInv (e,phiN)
    m=n
    return e,n,d,m

def encrypt(e,N,msg):
    cipher = ""

    for c in msg:
        m = ord (c)
        cipher += str (pow (m,e,N)) + " "

    return cipher

def decrypt(d,N,cipher):
    msg = ""

    parts = cipher.split ()
    for part in parts:
        if part:
            c = int (part)
            msg += chr (pow (c,d,N))

    return msg

def dispKeys(k):

    new_e, new_n, new_d, new_m = generateKeys(k)
    e.set(new_e)
    n.set(new_n)
    d.set(new_d)
    m.set(new_m)
    e_input.delete(1.0, END)
    e_input.insert(1.0, e.get())
    n_input.delete(1.0, END)
    n_input.insert(1.0, n.get())
    d_input.delete(1.0, END)
    d_input.insert(1.0, d.get())
    m_input.delete(1.0, END)
    m_input.insert(1.0, m.get())

def setKeys():
    keypath = fd.asksaveasfilename (initialfile='RSA VEŘEJNÝ_KLÍČ_V_BASE64.pub',title="Vybererte kam chcete veřejný klíč .pub uložit")
    if not keypath:
        messagebox.showerror ("Error","Nic jsi nevybral!Proím vyber si kam chceš uložit daný soubor")
    else:

     keys_public=open(keypath,'w')
     keys_public.write(
        str(e_input.get(1.0,END)).strip() + "\n" +
        str(n_input.get(1.0,END)).strip()
     )
     keys_public.close()
    
    keypath1 = fd.asksaveasfilename (initialfile='RSA SOUKROMÝ_KLÍČ_V_BASE64.priv',
                                    title="Vybererte kam chcete soukromý klíč .priv uložit")
    if not keypath:
        messagebox.showerror ("Error","Nic jsi nevybral!Proím vyber si kam chceš uložit daný soubor")
    else:
     keys_private = open (keypath1,'w')
     keys_private.write (
        str (d_input.get (1.0,END)).strip () + "\n" +
        str (m_input.get (1.0,END)).strip ()
     )
     keys_private.close()
def hash_file(filename):

   h = hashlib.sha3_512()


   with open(filename,'rb') as file:

       chunk = 0
       while chunk != b'':

           chunk = file.read(1024)
           h.update(chunk)

   return h.hexdigest()

def sign():
    filename = fd.askopenfilename (title="Vybererte soubor, ketrý chcete podepsat")
    if not filename:
        messagebox.showerror ("Error","Nic jsi nevybral!Proím vyber si jaký soubor chceš podepsat")
    else:
     hashoffile=hash_file(filename)
    #print (hash_file (filename))
    sizeofifle=os.path.getsize(filename)
    name_type = os.path.splitext(filename)
    filetype = name_type[1]
    nameoffile1=os.path.basename(filename)
    nameoffile=os.path.splitext(os.path.basename(filename))[0]
    pathoffile=os.path.abspath(filename)
    creationdateoffile=time.ctime(os.path.getctime(filename))
    lastmodifiedfile=time.ctime(os.path.getmtime(filename))
    str='Název souboru:{}\nTyp souboru:{}\nOriginální velikost souboru:{}mb\nCesta souboru:{}\
    \nDatum vytvoření souboru:    {}\nPoslední modifikace souboru:{}\nHash souboru:{}'.format(nameoffile,filetype,sizeofifle/1000000,pathoffile,
                                                                                        creationdateoffile,lastmodifiedfile,hashoffile)

    msg3_input.insert(1.0,nameoffile1)
    keypath = fd.askopenfilename (title="Vybererte soukromý klíč .priv",filetypes=[("Priv key","*.priv")])
    keysfile = open (keypath)
    keys = keysfile.read ()
    keys = keys.split ("\n")
    d = int (keys[0])
    m = int (keys[1])
    print(e)
    encrypted_hash = encrypt (d,m,hashoffile)
    encrypted_hash64=encrypted_hash.encode("ascii")
    base64_bytes = base64.b64encode (encrypted_hash64)
    base64_string = base64_bytes.decode ("ascii")
    msg_input.delete (1.0,END)
    msg_input.insert(1.0,str)
    sig_input.delete(1.0,END)
    sig_input.insert(1.0,base64_string)
    savefile = open ('RSA_SHA3_512 PODPIS_V_BASE64.sign','w')
    savefile.write (base64_string)
    savefile.close ()

    filepath = fd.asksaveasfilename (initialfile ="Podpis+soubor.zip",title="Vybererte kam chcete .zip soubor uložit")
    print (filepath)
    if not filepath:
        messagebox.showerror ("Error","Nic jsi nevybral!Proím vyber si kam chceš .zip soubor uložit")
    else:

     zipObj = ZipFile (filepath,'w')
    #zipObj = ZipFile ("test.zip",'w')
    zipObj.write (filename,basename(filename))
    zipObj.write("RSA_SHA3_512 PODPIS_V_BASE64.sign")
    os.remove ("RSA_SHA3_512 PODPIS_V_BASE64.sign")
    zipObj.close ()

    #savefile=fd.asksaveasfile(defaultextension='.sign',initialfile ="RSA_SHA3-512 PODPIS_V_BASE64")
    #savefile.write(base64_string)
    keysfile.close ()

def readKeys():
    keypath = fd.askopenfilename (title="Vybererte veřejný klíč .pub",filetypes=[("Pub key","*.pub")])
    keypath1 = fd.askopenfilename (title="Vybererte soukromý klíč .priv",filetypes=[("Priv key","*.priv")])

    keysfile=open(keypath)
    keysfile1=open(keypath1)
    keys=keysfile.read()
    keys1=keysfile1.read()
    keys=keys.split("\n")
    keys1 = keys1.split("\n")
    e.set(keys[0])
    n.set(keys[1])
    d.set(keys1[0])
    m.set(keys1[1])
    e_input.delete(1.0, END)
    e_input.insert(1.0, e.get())
    n_input.delete(1.0, END)
    n_input.insert(1.0, n.get())
    d_input.delete(1.0, END)
    d_input.insert(1.0, d.get())
    m_input.delete(1.0, END)
    m_input.insert(1.0, m.get())
    keysfile.close()
    keysfile1.close()


def readData(): # For verify signature

    filename = msg3_input.get ("1.0",'end-1c')
    print (filename)

    global file_names
    file_names = fd.askopenfilenames (initialdir="/",title="Vyber .zip s podepsaným souborem",filetypes=[("Zip file","*.zip")])
    if not file_names:
        messagebox.showerror ("Error","Nic jsi nevybral!Proím vyber si .zip soubor, který chces ověřit")
    else:

     for file_name in file_names:
        if file_name.endswith ('.zip'):
            with ZipFile (file_name,'r') as zip:
                zip.extractall ()

    """
    unzipped_file = zipfile.ZipFile ("test.zip","r")
    a_file = unzipped_file.read ("RSA_SHA3_512 PODPIS_V_BASE64.sign")
    enc_hash64 = a_file.decode ("utf-8")
    print (enc_hash64)
    """
    enchash = open ("RSA_SHA3_512 PODPIS_V_BASE64.sign")
    enc_hash64 = enchash.read ()
    print(enc_hash64)

   #with zipfile.ZipFile("TEST.zip", 'r') as file:

#        file.extractall()

    #filename = fd.askopenfilename (title="Vybererte soubor, který chcete ověřit")
    #print(filename)
    hashoffile=hash_file(filename)
    print(hashoffile)

    sizeofifle = os.path.getsize (filename)
    name_type = os.path.splitext (filename)
    filetype = name_type[1]
    # nameoffile=os.path.basename(filename)
    nameoffile = os.path.splitext (os.path.basename (filename))[0]
    pathoffile = os.path.abspath (filename)
    creationdateoffile = time.ctime (os.path.getctime (filename))
    lastmodifiedfile = time.ctime (os.path.getmtime (filename))
    str = 'Název souboru:{}\nTyp souboru:{}\nOriginální velikost souboru:{}mb\nCesta souboru:{}\
        \nDatum vytvoření souboru:{}\nPoslední modifikace souboru:{}\nHash souboru:{}'.format (nameoffile,filetype,
                                                                                               sizeofifle / 1000000,
                                                                                               pathoffile,
                                                                                               creationdateoffile,
                                                                                               lastmodifiedfile,
                                                                                               hashoffile)

    #hashfile=fd.askopenfile(title="Vyberte eletrický podpis pro ověření")
    #enc_hash64 = hashfile.read()
    base64_bytes = enc_hash64.encode ("ascii")
    sample_string_bytes = base64.b64decode (base64_bytes)
    enc_hash = sample_string_bytes.decode ("ascii")
    msg2_input.delete (1.0,END)
    msg2_input.insert (1.0,str)
    keypath1 = fd.askopenfilename (title="Vybererte veřejný klíč .pub",filetypes=[("Pub key","*.pub")])
    if not filename:
        messagebox.showerror ("Error","Nic jsi nevybral!Proím vyber si .priv soubor")
    else:
     keysfile = open (keypath1)
    keys = keysfile.read ()
    keys = keys.split ("\n")
    e = int (keys[0])
    n = int (keys[1])
    #dec_hash=sig_input.get(1.0,END)

    dec_hash = decrypt (e,n,enc_hash)
    #print(decrypted_hash)
    sig2_input.delete (1.0,END)
    sig2_input.insert (1.0,dec_hash)
    if (hashoffile == dec_hash):
        res.set (u'\u2705'"Podpis byl úspěšně ověřen!"u'\u2705')
    else:
        res.set (u'\u274c'"Podpis není stejný!!"u'\u274c')

    enchash.close()
    os.remove ("RSA_SHA3_512 PODPIS_V_BASE64.sign")
    os.remove (filename)
    keysfile.close ()
    #unzipped_file.close()


root = Tk()
root.title("RSA eletrický podpis")
root.geometry("920x750")
s = ttk.Style(root)
s.configure("TNotebook", tabposition='n',background='#6C6C6C')
s.configure("TFrame",background='#FAEBD7')
notebook = ttk.Notebook(root,padding=20);
notebook.pack(expand=1, fill="both")
frame1 = ttk.Frame(notebook,relief=GROOVE,padding=5)
frame2 = ttk.Frame(notebook,relief=GROOVE,padding=5)
frame3 = ttk.Frame(notebook,relief=GROOVE,padding=5)
notebook.add(frame1, text='   Generování klíčů    ')
notebook.add(frame2, text='   Podpis souboru   ')
notebook.add(frame3, text='   Ověření podpisu   ')
keysizes=[10,25,50,100]
current_keysize=IntVar();
current_keysize.set(100);
Generate_Keys_Label=Label(frame1,text="  Generování klíčů: ",font=('Arial', 14, 'bold'),background='#FAEBD7')
Generate_Keys_Label.grid(padx=5,pady=10,row=0,column=0)
Public_Key_Label = Label(frame1,text="  Veřejný klíč: ",font=('Arial', 12),background='#FAEBD7')
Public_Key_Label.grid(padx=5,pady=10,row=2, column=0)
Label(frame1,text="e: ",font=('Arial', 12),background='#FAEBD7').grid(padx=5,pady=10,row=3,column=0)
e=IntVar()
e_input=ScrolledText(frame1,width=80,height=5)
e_input.grid(padx=5,pady=10,row=3, column=1,sticky="E",columnspan=4)
Label(frame1,text="n: ",font=('Arial', 12),background='#FAEBD7').grid(padx=5,pady=10,row=4,column=0)
n=IntVar()
n_input=ScrolledText(frame1,width=80,height=5)
n_input.grid(padx=5,pady=10,row=4, column=1,sticky="E",columnspan=4)
Private_Key_Label=Label(frame1,text="  Soukromý klíč: ",font=('Arial', 12),background='#FAEBD7')
Private_Key_Label.grid(padx=5,pady=10,row=5,column=0)
Label(frame1,text="d: ",font=('Arial', 12),background='#FAEBD7').grid(padx=5,pady=10,row=6,column=0)
d=IntVar()
d_input=ScrolledText(frame1,width=80,height=5)
d_input.grid(padx=5,pady=10,row=6, column=1,sticky="E",columnspan=4)
m=IntVar()
Label(frame1,text="m: ",font=('Arial', 12),background='#FAEBD7').grid(padx=5,pady=10,row=7,column=0)
m_input=ScrolledText(frame1,width=80,height=5)
m_input.grid(padx=5,pady=10,row=7, column=1,sticky="E",columnspan=4)
Read_Keys_Button=Button(frame1,text = " Načtení klíče ",font=('Arial', 12),activebackground='Coral',background='Coral',relief=FLAT,command=readKeys)
Read_Keys_Button.grid(ipadx=10,ipady=10,padx=5,pady=10,row=9,column=1)
Generate_Keys_Button=Button(frame1,text = " Generování klíče ",font=('Arial', 12),activebackground='Coral',background='LightSeaGreen',relief=FLAT,command=lambda: dispKeys(int(current_keysize.get()//2)))
Generate_Keys_Button.grid(ipadx=10,ipady=10,padx=5,pady=10,row=9,column=2)
Set_Keys_Button=Button(frame1,text = " Uložení klíče ",font=('Arial', 12),activebackground='Coral',background='LightSkyBlue',relief=FLAT,command=setKeys)
Set_Keys_Button.grid(ipadx=10,ipady=10,padx=5,pady=10,row=9,column=3)
Label(frame2,text="  Eletrický podpis:   ",font=('Arial', 14, 'bold'),background='#FAEBD7').grid(padx=5,pady=10,row=11,column=0)
msg=StringVar(frame2,"")
Label(frame2,text=" Info. o souboru : ",font=('Arial', 12),background='#FAEBD7').grid(padx=5,pady=10,row=13,column=0)
msg_input=ScrolledText(frame2,width=80,height=10)
msg_input.grid(padx=5,pady=10,row=13, column=1,sticky="E",columnspan=4)
Sign_Button=Button(frame2,text = " Podpis souboru ",font=('Arial', 12),activebackground='Coral',background='LightSeaGreen',relief=FLAT,command=sign)
Sign_Button.grid(ipadx=10,ipady=10,padx=5,pady=10,row=14,column=2)
sig=IntVar()
Label(frame2,text=" Podpis:      ",font=('Arial', 12),background='#FAEBD7').grid(padx=5,pady=10,row=15,column=0)
sig_input=ScrolledText(frame2,width=80,height=10)
sig_input.grid(padx=5,pady=10,row=15, column=1,sticky="E",columnspan=4)
Label(frame3,text="  Ověření podpisu: ",font=('Arial', 14, 'bold'),background='#FAEBD7').grid(padx=5,pady=10,row=14,column=0)
msg2=StringVar()
Read_Data_Button=Button(frame3,text = " Ověření souboru ",font=('Arial', 12),activebackground='Coral',background='LightSeaGreen',relief=FLAT,command=readData)
Read_Data_Button.grid(ipadx=10,ipady=10,padx=5,pady=10,row=20,column=0,sticky="E")
Label(frame3,text=" Info. o souboru: ",font=('Arial', 12),background='#FAEBD7').grid(padx=5,pady=10,row=21,column=0)
msg2_input=ScrolledText(frame3,width=80,height=10)
msg2_input.grid(padx=5,pady=10,row=21, column=1,sticky="E",columnspan=4)
Label(frame3,text=" Název souboru: ",font=('Arial', 12),background='#FAEBD7').grid(row=90,column=0)
msg3_input=ScrolledText(frame3,width=30,height=1)
msg3_input.grid(padx=5,pady=10,row=100, column=0,columnspan=2)
sig2=IntVar()
Label(frame3,text=" Podpis: ",font=('Arial', 12),background='#FAEBD7').grid(padx=5,pady=10,row=23,column=0)
sig2_input=ScrolledText(frame3,width=80,height=10)
sig2_input.grid(padx=5,pady=10,row=23, column=1,sticky="E",columnspan=4)
res=StringVar(frame3,"Pro ověření zmáčkněte tlačítko .")
Label(frame3,textvariable=res,font=('Arial', 14),background='#FAEBD7').grid(padx=5,pady=10,row=24,column=2)
Label(frame1,text=" Velikost klíče: ",font=('Arial', 12),background='#FAEBD7').grid(padx=5,pady=10,row=1,column=0,columnspan=3)
KeySizes_Drop = Combobox( frame1 ,textvariable=current_keysize ,values=keysizes)
KeySizes_Drop.grid(padx=5,pady=10,row=1,column=2)
root.mainloop()