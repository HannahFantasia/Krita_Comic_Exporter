import os
from krita import *
iO = InfoObject()
pathList = []
app = Krita.instance()

### THE PATH INSIDE THE QUOTE IS WHERE YOUR FILES ARE INSIDE OF ###
rootDir = R"G:\My Drive\Juno\Comic\Sketch"

### THIS IS THE FOLDER INSIDE THE PATH ABOVE WHERE IT EXPORTS INTO ###
exportdir = os.path.join(rootDir, "Preview")

# CURRENTLY ONLY JPEG AND PNG SUPPORT
suffix = '.jpeg'

PNG_SETTINGS = [("alpha", False),
                ("indexed", False),
                ("interlaced", False),
                ("saveSRGBProfile", True),
                ("compression", 6),
                ("transparencyFillcolor", [255,255,255])]

JPEG_SETTINGS = [("baseline", True),
                 ("exif", True),
                 ("storeAuthor", True),
                 ("filters", 'ToolInfo,Anonymizer'),
                 ("forceSRGB", True),
                 ("xmp", True),
                 ("iptc", True),
                 ("is_sRGB", True),
                 ("optimize", True),
                 ("progressive", False),
                 ("saveprofile", True),
                 ("quality", 100),
                 ("smoothing", 0),
                 ("subsampling", 0),
                 ("transparencyFillcolor", [255,255,255])]

### SETTINGS PNG ###
if suffix == '.png':
    for name, setting in PNG_SETTINGS:
        iO.setProperty(name,setting)

### SETTINGS JPEG ###
elif suffix == '.jpeg' or suffix == ".jpg":
    for name, setting in JPEG_SETTINGS:
        iO.setProperty(name,setting)

for subdir, dirs, files in os.walk(os.path.normpath(rootDir)):
    # os.path.join geeft al str terug
    # list comprehension van alle files in de folder die eindigen met .kra
    paths = [os.path.join(subdir,file) for file in files if file.endswith('.kra')]
    pathList.extend(paths)

for file in pathList:
    splitted = os.path.split(file)
    filename = os.path.splitext(splitted[1])[0]
    exported = os.path.join(exportdir, filename + suffix)
    exported = os.path.normpath(exported) # Normalise path for inter-OS compatibility

    if not os.path.isfile(exported):
        print(f"exporting image to: {exported}")
        newDocument = app.openDocument(file)
        app.activeWindow().addView(newDocument)
        currentDocument = app.activeDocument()
        currentDocument.setBatchmode(True)
        
        node = None
        if currentDocument.nodeByName("LETTERS"):
            node = currentDocument.nodeByName("LETTERS")
            node.setVisible(True) # CHANGE TO TRUE IF YOU WANT TO SEE TEMP LETTERING
            currentDocument.refreshProjection()
        currentDocument.exportImage(exported, iO)
        
        if node:
            node.setVisible(True)

        app.action('file_close').trigger()

    else:
        print(f"{exported} already exists!")
