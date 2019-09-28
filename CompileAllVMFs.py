'''
Author: rob5300
Description: Takes all the .vmf files in the same directory of this py file and compiles them with vbsp, vrad and vvis.
			 The paths and locations can be easily customised below.
			 The finished map can also be copied to an additional directory.
             Python 3 only
'''
import os
import shutil
import threading
import subprocess

# ----------------------------- Settings -----------------------------------

# The location of the bin directory in your HL2 installation. Should be in your steamapps/common folder.
hl2bindir = "D:\\SteamLibrary\\steamapps\\common\\Half-Life 2\\bin"

# Game data to use and where vbsp should place your maps after compiling. This should be the top directory of the mod, the Half-Life 2, or ep2 folder for example.
targetmapdir = "D:\\SteamLibrary\\steamapps\\common\\Half-Life 2\\ep2"

# Should we copy the map to another directory too? (set to True or False)
copyToAdditionalFolder = True

# If the above is True, the Additional dir to also copy the compiled map to. This copies the finished map with vis and rad applied.
additionalmapDir = "D:\\SteamLibrary\\steamapps\\sourcemods\\MyMod\\maps"

##--------------------------------------------------------------------------
commandvbps = [f"{hl2bindir}\\vbsp.exe",  "-game",  targetmapdir]
commandvrad = [f"{hl2bindir}\\vrad.exe", "-both", "-StaticPropLighting"]
commandvvis = [f"{hl2bindir}\\vvis.exe"]

endmessages = []
maperrors = []
threads = []
mapsremaining = 0

ourpath = os.path.dirname(__file__)

def CompileAll():
    print("--== Batch .vmf compiler by github.com/rob5300 ==--")
    print(".vmf files will be located and compiled. Please wait for a message saying that all have finished before closing the window/program.\n")
    files = os.listdir(ourpath)
    global mapsremaining #Python is stupid soo we need this?
    mapsremaining = 0
    for file in files:
        if(".vmf" in file):
            thread = threading.Thread(target=CompileVMF, args=(file,))
            mapsremaining += 1
            thread.start()
            threads.append(thread)
            
    for t in threads:
        if(t.is_alive()): t.join()

    print("\n")
    for message in endmessages:
        print(message)

    if(maperrors.__len__() > 0):
        print("")
        print("There were map errors! They are listed below:")
        for message in maperrors:
            print("   " + message)

    print(f"\nDone!! You may close this window.")

def CompileVMF(vmf):
    print("##### Compiling " + vmf + " #####")
    # Compile the map
    print(f"## Running vbps on {vmf}")
    executeonfile(commandvbps, ourpath + "\\" + vmf)
    # Send new bsp to vrad and vvis.
    print(f"## Running vrad on {vmf}")
    executeonfile(commandvrad, GetBSP(vmf))
    print(f"## Running vvis on {vmf}")
    executeonfile(commandvvis, GetBSP(vmf))
    global mapsremaining #Python is stupid soo we need this?
    mapsremaining -= 1
    print(f"##### Compile finished on {vmf}, {mapsremaining} still processing... #####")

    # Copy the finished file to the target games map dir.
    name = os.path.splitext(vmf)[0]
    shutil.copyfile(GetBSP(vmf), f"{targetmapdir}\\maps\\{name}.bsp")

    #endmessages.append(f"{vmf} was sent to vbsp, vvis and vrad")

    if(copyToAdditionalFolder):
        shutil.copyfile(GetBSP(vmf), f"{additionalmapDir}\\{name}.bsp")
        endmessages.append(f"Map {name} was copied to additional map dir at: {additionalmapDir}")

def executeonfile(cmd, file):
    newcommand = cmd.copy()
    newcommand.append(file)
    result = subprocess.run(newcommand, stdout=subprocess.PIPE).stdout.decode('utf-8')
    splitresult = result.split("\n")
    for line in splitresult:
        if("leaked!" in line or "Error" in line or "WARNING" in line or "bad" in line):
            maperrors.append(f"Error from {file}: {line}")
    

#Get the new bsp path.
def GetBSP(file):
    name = os.path.splitext(file)[0]
    return f"{ourpath}\\{name}.bsp"



CompileAll()
input()
