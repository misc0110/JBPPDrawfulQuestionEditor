import zipfile
import io
import os

def uncompress(filename):
    with open(filename, "rb") as f:
        data = f.read()
        z = io.BytesIO(b'\x50\x4b\x03\x04' + data[4:])
        zfile = zipfile.ZipFile(z)
        zfile.extractall("assets")

def compress(filename):
    with open(filename, "wb") as of:
        cwd = os.getcwd()
        os.chdir("assets")
        
        z = io.BytesIO()
        zfile = zipfile.ZipFile(z, "w", zipfile.ZIP_DEFLATED, False)

        for root, dirs, files in os.walk("."):
            for f in files:
                zfile.write(os.path.join(root, f))
                
        for zf in zfile.filelist:
            zf.create_system = 0
        
        zfile.close()
        z.seek(4)
        of.write(b'\x4a\x42\x47\x50' + z.read())
        os.chdir(cwd)
        