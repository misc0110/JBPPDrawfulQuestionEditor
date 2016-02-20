import zipfile
import io
import os
import json
import struct

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
        
        
def create_patch(filename, folder, info):
        z = io.BytesIO()
        
        pinfo = json.dumps(info).encode("utf-8")
        z.write(b'JBPP')
        z.write(struct.pack('I', len(pinfo)))
        z.write(pinfo)
        
        zfile = zipfile.ZipFile(z, "w", zipfile.ZIP_DEFLATED, False)

        for root, dirs, files in os.walk(folder):
            for f in files:
                zfile.write(os.path.join(root, f))
                
        for zf in zfile.filelist:
            zf.create_system = 0
        
        zfile.close()
        z.seek(0)
        with open(filename, "wb") as of:
            of.write(z.read())


def apply_patch(filename):
        with open(filename, "rb") as f:
            magic = f.read(4)
            if magic != b'JBPP': raise Exception('Wrong magic')
            json_len = struct.unpack('I', f.read(4))
            info = json.loads(f.read(json_len[0]).decode("utf-8"))
            
            zfile = zipfile.ZipFile(io.BytesIO(f.read()))
            zfile.extractall()


def patch_info(filename):
        with open(filename, "rb") as f:
            magic = f.read(4)
            if magic != b'JBPP': raise Exception('Wrong magic')
            json_len = struct.unpack('I', f.read(4))
            data = f.read(json_len[0])
            info = json.loads(data.decode("utf-8"))
            return info
