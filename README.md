# Compile All VMFs
This simple python script gets all avaliable .vmf files in the same directory and compiles them at the same time. All maps are sent to vbsp, vrad then vvis.

## Customisation
Edit these variables inside the script to ensure it works with your hl2/source installation.

- ``hl2bindir``: The directory where your vbsp, vrad and vvis executables are found. Set this to your hl2 or other source game bin folder
- ``targetmapdir``: Where the finished maps will be placed once they have finished their compile process.
- ``copyToAdditionalFolder``: Set to ``True`` or ``False`` to tell the script to copy the finished file to an additional directory after.
- ``additionalmapDir``: The additional directory to copy to if enabled.

Advanced options to customise, these will need to be changed if your are not on windows to target the correct file name.
- ``commandvbsp``: An array of the commands to use to execute vbsp. Edit this to add [extra launch arguments](https://developer.valvesoftware.com/wiki/VBSP).
- ``commandvrad``: An array of the commands to use to execute vrad. Edit this to add [extra launch arguments](https://developer.valvesoftware.com/wiki/VRAD).
- ``commandvvis``: An array of the commands to use to execute vvis. Edit this to add [extra launch arguments](https://developer.valvesoftware.com/wiki/VVIS).


This script uses threading to compile maps at the same time to ensure it finishes faster. Certain errors are caught and displayed at the end of execution. If one isn't and you would like to see it please open an issue/pull request.
