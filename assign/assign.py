#!/usr/bin/env python3
# coding: utf-8
import os
import time
import re


letters_from_frcmod="letters_from_frcmod.txt"
term_letters_file="term_letters_file.txt"
dihedrals=[]
#check_dat="check.dat"
delete_if_less_than=10
place_to_write_whole_frcmod="info/desired.frcmod"


def delete_files(filename):
    if os.path.exists(filename):
        os.remove(filename)

def create_folder(folder):
    directory = "./"+folder
    if not os.path.exists(directory):
        os.makedirs(directory)


def file_control(input_file):
    try:
        #trying to open a file in read mode
        f = open(input_file,"r")
        content_file=f.read()
        print("File opened:")
        print(content_file)
        f.close()
    except FileNotFoundError:
        exit("File not found :(")
        #except:
            #exit("There may be a problem with your file..")
check_dat= input('Enter your gaffic frcmod file name (check.dat) :  ') or "check.dat"
file_control(check_dat)
temp_dat = input('Enter your metallic frcmod file name (temp.dat): ') or "temp.dat"
file_control(temp_dat)

try:
    number_of_atoms=int(input("How many atom types you want to change? "))
except ValueError:
    exit("How many\'s answers type must be integer :( ")
except:
    exit("Terminated...")


delete_files(place_to_write_whole_frcmod)
delete_files("info/zero.dat")
delete_files("info/non_zero_temp.dat")
delete_files("info/non_zero_check.dat")
os.system(f"grep -v 'ATTN' {temp_dat} >info/non_zero_temp.dat ")
os.system(f"grep -v 'ATTN' {check_dat} >info/non_zero_check.dat ")
os.system(f"grep -E 'ATTN|MASS|BOND|ANGLE|DIHE|IMPROPER' {temp_dat} >info/zero.dat ")


metals=['1c', '1d','1e', '1i','4i','1n', '1o','4o','1p', '1s', '2c', '2d','2e', '2i', '2n', '2o', '2p', '2s', '3c', '3d','3e', '3i', '3n','4n', '3o', '3p', '3s', '4c', '4d','4e', '4i' '4n', '4p', '4s']
gaff=["c ","cs","c1","c2","c3","ca","cp","cq","cc","cd","ce","cf","cg","ch","cx","cy","cu","cv","cz","h1","h2","h3","h4","h5","ha","hc","hn","ho","hp","hs","hw","hx","f ","cl","br","i ","n ","n1","n2","n3","n4","na","nb","nc","nd","ne","nf","nh","no","ns","nt","nx","ny","nz","n+","nu","nv","n7","n8","n9","o ","oh","os","ow","p2","p3","p4","p5","pb","pc","pd","pe","pf","px","py","s ","s2","s4","s6","sh","ss","sx","sy","i "]
gaffil=[]
metalil=[]
l1=["1n","2n","3n","4n","n ","n1","n2","n3","n4","na","nb","nc","nd","ne","nf","nh","no","ns","nt","nx","ny","nz","n+","nu","nv","n7","n8","n9"]
l2=["1p","2p","3p","4p","p2","p3","p4","p5","pb","pc","pd","pe","pf","px","py"]
l3=["1s","2s","3s","4s","s2","s4","s6","sh","ss","sx","sy"]
l4=["1o","2o","3o","4o","o ","oh","os"]
l5=["1c","2c","3c","4c","cl"]
l6=["1d","2d","3d","4d","ca"]
l7=["1e","2e","3e","4e","c ","c1","c2","c3","cp","cq","cc","cd","ce","cf","cg","ch","cx","cy","cu","cv","cz"]
l8=["1i","2i","3i","4i","i "]
def whereis(eleman1,eleman2,list):
    p=0
    if eleman1 and eleman2 in list:
        p=1
        #print("matched")
    elif eleman1 and eleman2 not in list:
        #print("This is wrong list")
        p=0
    else:
        p=0
    return p

def match_control(eleman1,eleman2,list=[l1,l2,l3,l4,l5,l6,l7,l8]):
    n=0
    for x in list:
        n= whereis(eleman1,eleman2,x)+n
    return n

def get_input():
    lives=number_of_atoms
    while (lives>0):
        print("""Now write atom type pairs you want to change.
        -first atom type must be gaff and second must be metalic ff
        between the two atom type pairs use space and press enter
        For example: os 1o 
        and then enter second, third, exc.. atom type pairs in the same way""")
        g, m = map(str, input().split())
        if(len(g))==1 : g=g+" "
        k=match_control(g,m)
        if m not in metals:
            print(f"ERR:1 {m} is not a metalic ff. Please enter again: {lives}")
        
        elif g not in gaff: 
            print(f"ERR 2: {g} is not from gaff Please enter again: Lives: {lives}  ")
        
        #elif g[0]!=m[1]:
        #        print(f" ERR 3: attention {m} atom do not equal to {g} these atoms are different. Lives: {lives} ")
        
        elif g in metals: 
            print(f"ERR 4: attention {m} atom do not equal to {g} these atoms are different.Lives: {lives} ")
        elif k==0:
            print("match error")
        else:
            lives=lives-1
            gaffil.append(g)
            metalil.append(m)
            if lives==0: break
            print(gaffil)
            print(metalil)
            print(f"{g} atom type will change with {m} now {lives} atoms remains")
            print(len(gaffil))

def select (temp_dat,term_type):
    word1="MASS"
    word2="BOND"
    word3="ANGLE"
    word4="DIHE"
    word5="IMPROPER"
    word6="NONBON"
    word7="\n"
    inFile = open(temp_dat)
    outFile = open(letters_from_frcmod, "w")
    buffer = []
    if term_type=="mass":
        start_word=word1
        end_word=word2
        b=3
    elif term_type=="bond":
        start_word=word2
        end_word=word3
        b=5
    elif term_type=="angle":
        start_word=word3
        end_word=word4
        b=8
    elif term_type=="dihedral":
        start_word=word4
        end_word=word5
        b=11
    elif term_type=="improper":
        start_word=word5
        end_word=word6
        b=11
    elif term_type=="nonbond":
        start_word=word6
        end_word=word7
        b=5
    for line in inFile:
        if line.startswith(start_word):
            buffer = ['']
        elif line.startswith(end_word):
            outFile.write("".join(buffer))
            buffer = []
        elif buffer:
            buffer.append(line)
    inFile.close()
    outFile.close()

    with open(letters_from_frcmod, 'r') as file:
        txt = file.read()
    x = txt.split('\n')
    term_letters=[]
    dihedral_ara=[]
    f = open(term_letters_file, "w")
    for i in range(len(x)):
        n=x[i][0:b]
        m=x[i][b:] + "\n"
        term_letters.append(n)
        #print('%s %s' % (n,m))
#if you want to write letters into a file (letters_from_frcmod variable) please remove comment from f.write function below:
        #f.write('%s %s' % (n,m))
        #remove duplicates
        term_letters = list(dict.fromkeys(term_letters))
        #remove blanks
    if '' in term_letters: term_letters.remove('')
    file.close()
    f.close()
    inFile.close()
    outFile.close()
    return term_letters
#search reverse terms too...
def reverse_term(term_letters,term_type):
    word_ters=[]
    temp_variable=list(term_letters)
    for x in range(len(term_letters)):
        #a=len(temp_variable[x])
        if term_type=="dihedral":
            #print(term_type)
            a1=temp_variable[x][0:2]
            a2=temp_variable[x][3:5]
            a3=temp_variable[x][6:8]
            a4=temp_variable[x][9:12]
            n=a4+"-"+a3+"-"+a2+"-"+a1
            word_ters.append(n)
            j="X -"+a3+"-"+a2+"-X "
            word_ters.append(j)
        elif term_type=="angle":
            #print(term_type)
            a1=temp_variable[x][0:2]
            a2=temp_variable[x][3:5]
            a3=temp_variable[x][6:8]
            n=a3+"-"+a2+"-"+a1
            word_ters.append(n)
        elif term_type=="bond":
            a1=temp_variable[x][0:2]
            a2=temp_variable[x][3:5]
            n=a2+"-"+a1
            word_ters.append(n)
    return word_ters

#### this function assigns metal parameters and it uses gaff atom atomic counterparts of metal atoms:
def parametre_ata(file,dizi,term):
    letters=[]
    numbers=[]
    bitti=[]
    dizi=list(set(dizi))
    #print("Getting parameters from your files...: ")
    gaffic=metallic=list(dizi)#will be gaffic
    #print(f"metallic --> {metallic}")

    for z in range(len(gaffil)):
        gaffic = [w.replace(metalil[z],gaffil[z]) for w in gaffic]
    #test## gaffic = [w.replace('2p', 'p5') for w in gaffic]
    #print(f"gaffic --> {gaffic}")
    content = open(file).readlines()
    for x in range(len(gaffic)):
        line_number = [line_num for line_num, line_content in enumerate(content) if gaffic[x] in line_content]
        numbers.append('')
        letters.append('')
        bitti.append('')
        for n in range(len(line_number)):
            #print(content[line_number[n]])
            if term=="dihedral":
                numbers[x]=content[line_number[n]][12:54]
                letters[x]=metallic[x][0:12]
            if term=="improper":
                numbers[x]=content[line_number[n]][12:54]
                letters[x]=metallic[x][0:12]
            elif term=="angle":
                numbers[x]=content[line_number[n]][8:50]
                letters[x]=metallic[x][0:8]
            elif term=="bond":
                #print(term)
                numbers[x]=content[line_number[n]][6:48]
                letters[x]=metallic[x][0:6]
            elif term=="mass":
                #print(term)
                numbers[x]=content[line_number[n]][3:34]
                letters[x]=metallic[x][0:3]+" "
            elif term=="nonbond":
                #print(term)
                numbers[x]=content[line_number[n]][5:33]
                letters[x]="  "+metallic[x][0:5]+" "
        z=letters[x]+numbers[x]
        if(len(numbers[x]))>0:
            print("")
            #print(f"no-->{numbers[x]}")
            #print(f"lett-->{letters[x]}")
        if '' in bitti: bitti.remove('')
        bitti.append(z)
        if len(z)>0: 
            print("")
            #print(f"z-->{z}")
            #print("----")
    return bitti
#this function clears empty and/or duplicate parameters
#Finally, this function write metal frcmod file
def write_novel_parameters(filePath,novel_parameters):
    if os.path.exists(filePath):
        os.remove(filePath)
    f16 = open(filePath, "a")
    #index_sayisi=int(index_sayisi)
    #for i in range(index_sayisi):
    for i in range(len(novel_parameters)):
        f16.write('%s \n' % (novel_parameters[i]))
    f16.close()
########################FROM PARMCHK#####################################
#tempfiles=["temp_mass.dat","temp_bonds.dat","temp_angles.dat","temp_dihedrals.dat","temp_impropers.dat","temp_nonbond.dat"]
#normalfiles=["gaff2_mass.dat","gaff2_bonds.dat","gaff2_angles.dat","gaff2_dihedrals.dat","gaff2_impropers.dat","gaff2_nonbond.dat"]
#parmchkfiles=["check_mass.dat","check_bonds.dat","check_angles.dat","check_dihedrals.dat","check_impropers.dat","check_nonbond.dat"]
#utempfiles=["utemp_mass.dat","utemp_bonds.dat","utemp_angles.dat","utemp_dihedrals.dat","utemp_impropers.dat","utemp_nonbond.dat"]
#start=["MASS","BOND","ANGLE","DIHE","IMPROPER","NONBON"]
#end=["BOND","ANGLE","DIHE","IMPROPER","NONBON","$p"]





create_folder("info")

get_input()

# In[2]:

def clear_parameters(terms):
    parametreler=[]
    parametreler.clear
    p=list(terms)
    for x in range(len(p)):
        #print(p[x][10:11])
        #print(p[x])
        if(p[x]!=""):#remove empty lines
            parametreler.append(p[x].strip())
            parametreler=list(set(parametreler))
    return parametreler

# In[3]:


#now temp_dat is not temp.dat anymore:

# In[4]:
zero_dat="info/zero.dat"
masses=select(zero_dat,"mass")
masses=list(set(masses))
#print(*masses,sep="\n")
masses=parametre_ata("data/gaff2_masses.dat",masses,"mass")
masses=clear_parameters(masses)

# In[5]:

bonds=select(zero_dat,"bond")
bond_reverse=reverse_term(bonds,"bond")
bonds=bonds+bond_reverse
bonds=list(set(bonds))
#print("bonds")
#print(*bonds,sep="\n")
bonds=parametre_ata("data/gaff2_bonds.dat",bonds,"bond")
bonds=clear_parameters(bonds)

# In[6]:

angles=select(zero_dat,"angle")
angle_reverse=reverse_term(angles,"angle")
angles=angles+angle_reverse
angles=list(set(angles))
#print(*angles,sep="\n") 
angles=parametre_ata("data/gaff2_angles.dat",angles,"angle")
angles=clear_parameters(angles)

##angles from parmchk2##############this is for next version!!!!!!!!!!!!!!!!!!!!
#os.system(f"sed -n '/ANGLE/,/DIHE/p' info/non_zero_check.dat > info/angle_parmchk.dat")
#angles_parmchk=select("info/non_zero_check.dat","angle")
#angle_reverse_parmchk=reverse_term(angles,"angle")
#angles_parmchk=angles_parmchk+angle_reverse_parmchk
#angles_parmchk=list(set(angles_parmchk))
#angles_parmchk=parametre_ata("info/angle_parmchk.dat",angles,"angle")
#angles_parmchk=clear_parameters(angles_parmchk)
#angles=angles+angles_parmchk


dihedrals=select(temp_dat,"dihedral")
dihedral_reverse=reverse_term(dihedrals,"dihedral")
dihedrals=dihedrals+dihedral_reverse
dihedrals=list(set(dihedrals))
#print(*dihedrals,sep="\n")
dihedrals=parametre_ata("data/gaff2_dihedrals.dat",dihedrals,"dihedral")
dihedrals=clear_parameters(dihedrals)

# In[9]:

impropers=select(zero_dat,"improper")
improper_reverse=reverse_term(impropers,"improper")
impropers=impropers+improper_reverse
impropers=list(set(impropers))
#print(*impropers,sep="\n")
impropers=parametre_ata("data/gaff2_impropers.dat",impropers,"improper")
impropers=clear_parameters(impropers)

# In[10]:

nonbonds=select(zero_dat,"nonbond")
nonbonds=list(set(nonbonds))
#print(*nonbonds,sep="\n")
nonbonds=parametre_ata("data/gaff2_nonbonds.dat",nonbonds,"nonbond")
nonbonds=clear_parameters(nonbonds)

# In[11]:

prefix_ADD = "  "
nonbonds = [prefix_ADD + x for x in nonbonds if isinstance(x, str)]

prefix=["matching atoms here...", "MASS"]
masses.append("\nBOND")
bonds.append("\nANGLE")
angles.append("\nDIHE")
dihedrals.append("\nIMPROPER")
impropers.append("\nNONBON")
temp_frcmod=prefix+masses+bonds+angles+dihedrals+impropers+nonbonds
write_novel_parameters(place_to_write_whole_frcmod,temp_frcmod)

masses.pop()
bonds.pop()
angles.pop()
dihedrals.pop()
impropers.pop()
#now write what you all things what you get...
#print("writing..")
#slowly... be sure you wrote.
time.sleep(0.001)
#wake up and finish this is not sunday :)
print("matching parameters are combined")

############START COMBINING#######################################
def combine (temp_dat,term_type):
    word1="MASS"
    word2="BOND"
    word3="ANGLE"
    word4="DIHE"
    word5="IMPROPER"
    word6="NONBON"
    word7="\n"
    inFile = open(temp_dat)
    outFile = open(letters_from_frcmod, "w")
    buffer = []
    if term_type=="mass":
        start_word=word1
        end_word=word2
        b=3
    elif term_type=="bond":
        start_word=word2
        end_word=word3
        b=5
    elif term_type=="angle":
        start_word=word3
        end_word=word4
        b=8
    elif term_type=="dihedral":
        start_word=word4
        end_word=word5
        b=11
    elif term_type=="improper":
        start_word=word5
        end_word=word6
        b=11
    elif term_type=="nonbond":
        start_word=word6
        end_word=word7
        b=5
    for line in inFile:
        if line.startswith(start_word):
            buffer = ['']
        elif line.startswith(end_word):
            outFile.write("".join(buffer))
            buffer = []
        elif buffer:
            buffer.append(line)
        
    inFile.close()
    outFile.close()

    
    with open(letters_from_frcmod, 'r') as file:
        txt = file.read()
    x = txt.split('\n')
    term_letters=[]
    dihedral_ara=[]
    p=[]
    f = open(term_letters_file, "w")
    for i in range(len(x)):
        n=x[i][0:b]
        #print("n------->"+n)
        m=x[i][b:]
        #print("m------->"+m)
        p=n+m
        #print("p------->"+p)
        term_letters.append(p)
       
        #print('%s %s' % (n,m))
#if you want to write letters into a file (letters_from_frcmod variable) please remove comment from f.write function below:
        #f.write('%s %s' % (n,m))
        #remove duplicates
        term_letters = list(dict.fromkeys(term_letters))
        #remove blanks
    if '' in term_letters: term_letters.remove('')
    #print(term_letters)
    file.close()
    f.close()
    inFile.close()
    outFile.close()
    return term_letters


mass1=combine("info/non_zero_check.dat" ,"mass")
mass2=combine("info/non_zero_temp.dat" ,"mass")
mass3=combine("info/desired.frcmod" ,"mass")
bond1=combine("info/non_zero_check.dat" ,"bond")
bond2=combine("info/non_zero_temp.dat" ,"bond")
bond3=combine("info/desired.frcmod" ,"bond")
angle1=combine("info/non_zero_check.dat" ,"angle")
angle2=combine("info/non_zero_temp.dat" ,"angle")
angle3=combine("info/desired.frcmod" ,"angle")
dihe1=combine("info/non_zero_check.dat" ,"dihedral")
dihe2=combine("info/non_zero_temp.dat" ,"dihedral")
dihe3=combine("info/desired.frcmod" ,"dihedral")
imp1=combine("info/non_zero_check.dat" ,"improper")
imp2=combine("info/non_zero_temp.dat" ,"improper")
imp3=combine("info/desired.frcmod" ,"improper")
nonbond1=combine("info/non_zero_check.dat" ,"nonbond")
nonbond2=combine("info/non_zero_temp.dat" ,"nonbond")
nonbond3=combine("info/desired.frcmod" ,"nonbond")

prefix_ADD = "  "
nonbonds = [prefix_ADD + x for x in nonbonds if isinstance(x, str)]
mass_frcmod=mass1+mass2+mass3
bond_frcmod=bond1+bond2+bond3
angle_frcmod=angle1+angle2+angle3
dihe_frcmod=dihe1+dihe2+dihe3
imp_frcmod=imp1+imp2+imp3
nonbond3.append("  Pd          1.2360  0.0282             https://pubs.acs.org/doi/10.1021/ct400146w") #for nonbond Pd
non_frcmod=nonbond1+nonbond2+nonbond3

prefix=["matching atoms here...", "MASS"]
mass_frcmod.append("\nBOND")
bond_frcmod.append("\nANGLE")
angle_frcmod.append("\nDIHE")
dihe_frcmod.append("\nIMPROPER")
imp_frcmod.append("\nNONBON")
temp_frcmod=prefix+mass_frcmod+bond_frcmod+angle_frcmod+dihe_frcmod+imp_frcmod+non_frcmod
temp_frcmod = [w.replace('X   ', 'X    ') for w in temp_frcmod]

#for x in range(len(temp_frcmod)):
#    temp_frcmod[x] = re.sub("^([0-9]|[A-z]){0,2}", "$1--", temp_frcmod[x])

write_novel_parameters("result.frcmod",temp_frcmod)

#now write what you all things what you get...
#print("writing..")
#slowly... be sure you wrote.
time.sleep(0.001)
delete_files(letters_from_frcmod)
delete_files(term_letters_file)
print("finished....\n please check result.frcmod file ")
