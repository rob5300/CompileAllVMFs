'''
Author: rob5300
Description: Takes all the .vmf files in the same directory of this py file and compiles them with vbsp, vrad and vvis.
			 The paths and locations can be easily customised below.
			 The finished map can also be copied to an additional directory.
'''
import os
import shutil

# ----------------------------- Settings -----------------------------------

# The location of the bin directory in your HL2 installation. Should be in your steamapps/common folder.
hl2bindir = "D:\\SteamLibrary\\steamapps\\common\\Half-Life 2\\bin"

# Where vbsp should place your maps after compiling. This should be the top directory of the mod, the Half-Life 2, or ep2 folder for example.
targetmapdir = "D:\\SteamLibrary\\steamapps\\common\\Half-Life 2\\ep2"

# Should we copy the map to another directory too? (set to True or False)
copyToAdditionalFolder = True

# If the above is True, the Additional dir to also copy the compiled map to. This copies the finished map with vis and rad applied.
additionalmapDir = "D:\\SteamLibrary\\steamapps\\sourcemods\\MyMod\\maps"

##--------------------------------------------------------------------------
commandvbps = f"\"{hl2bindir}\\vbsp.exe\" -game \"{targetmapdir}\" "
commandvrad = f"\"{hl2bindir}\\vrad.exe\" -both -StaticPropLighting "
commandvvis = f"\"{hl2bindir}\\vvis.exe\" "

endmessages = []

ourpath = os.path.dirname(__file__)

def CompileAll():
    
    files = os.listdir(ourpath)
    for file in files:
        if(".vmf" in file):
            print("\n### Compiling " + file + " ###\n")
            # Compile the map
            executeonfile(commandvbps, ourpath + "\\" + file)
            # Send new bsp to vrad and vvis.
            executeonfile(commandvrad, GetBSP(file))
            executeonfile(commandvvis, GetBSP(file))

            endmessages.append(f"{file} was sent to vbsp, vvis and vrad")

            if(copyToAdditionalFolder): 
                name = os.path.splitext(file)[0]
                shutil.copyfile(GetBSP(file), f"{additionalmapDir}\\{name}.bsp")
                endmessages.append(f"Map {name} was copied to additional map dir at: {additionalmapDir}")

    print("\n")
    for message in endmessages:
        print(message)
    print("Done!!!")

def executeonfile(cmd, file):
    toexec = f"\"{cmd}\"{file}\"\""
    os.system(toexec)

def GetBSP(file):
    name = os.path.splitext(file)[0]
    return f"{targetmapdir}\\maps\\{name}.bsp"

CompileAll()
input()
