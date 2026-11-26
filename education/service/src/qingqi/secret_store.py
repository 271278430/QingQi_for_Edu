"""Machine-local encrypted API credentials; plaintext never enters the public config view."""
import base64,ctypes,os
from pathlib import Path
from .contracts import ContractError


class SecretStore:
    def __init__(self,root:Path):self.root=root.resolve()

    def _windows(self,value:bytes,encrypt:bool):
        from ctypes import wintypes
        class Blob(ctypes.Structure):_fields_=[('length',wintypes.DWORD),('data',ctypes.POINTER(ctypes.c_ubyte))]
        source=ctypes.create_string_buffer(value);entropy=ctypes.create_string_buffer(str(self.root).encode())
        input_blob=Blob(len(value),ctypes.cast(source,ctypes.POINTER(ctypes.c_ubyte)))
        entropy_blob=Blob(len(entropy.raw)-1,ctypes.cast(entropy,ctypes.POINTER(ctypes.c_ubyte)));output=Blob()
        fn=ctypes.windll.crypt32.CryptProtectData if encrypt else ctypes.windll.crypt32.CryptUnprotectData
        fn.argtypes=[ctypes.POINTER(Blob),ctypes.c_void_p,ctypes.POINTER(Blob),ctypes.c_void_p,ctypes.c_void_p,wintypes.DWORD,ctypes.POINTER(Blob)]
        fn.restype=wintypes.BOOL
        if not fn(ctypes.byref(input_blob),None,ctypes.byref(entropy_blob),None,None,1,ctypes.byref(output)):raise ContractError('本机凭据保护失败，配置没有保存。')
        try:return ctypes.string_at(output.data,output.length)
        finally:
            ctypes.windll.kernel32.LocalFree.argtypes=[ctypes.c_void_p];ctypes.windll.kernel32.LocalFree(ctypes.cast(output.data,ctypes.c_void_p))

    def _fernet(self):
        from cryptography.fernet import Fernet
        file=self.root/'model-secrets.key.local'
        if not file.exists():
            try:
                fd=os.open(file,os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o600)
                with os.fdopen(fd,'wb') as out:out.write(Fernet.generate_key())
            except FileExistsError:pass
        if file.is_symlink() or file.stat().st_mode & 0o077:raise ContractError('本机凭据文件权限过宽，请限制为仅当前用户可读。')
        return Fernet(file.read_bytes())

    def seal(self,value:str):
        raw=value.encode()
        return 'dpapi:'+base64.b64encode(self._windows(raw,True)).decode() if os.name=='nt' else 'fernet:'+self._fernet().encrypt(raw).decode()

    def open(self,value:str):
        try:
            if value.startswith('dpapi:') and os.name=='nt':return self._windows(base64.b64decode(value[6:]),False).decode()
            if value.startswith('fernet:') and os.name!='nt':return self._fernet().decrypt(value[7:].encode()).decode()
        except Exception as error:raise ContractError('本机密钥不能解密，请在模型配置中重新设置。') from error
        raise ContractError('本机凭据格式不兼容，请重新设置。')
