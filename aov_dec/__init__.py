import os
import zstandard as zstd
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

DICT_PATH = "dict"
ZSTD_DICT = open(DICT_PATH, "rb").read() if os.path.exists(DICT_PATH) else b""

class JG:
    MAGIC = bytes.fromhex("22 4A 67")

    @staticmethod
    def get_name(file_path):
        base = os.path.basename(file_path)
        return os.path.splitext(base)[0]

    @staticmethod
    def _key(name):
        h = 0
        for ch in name:
            c = ord(ch)
            if 97 <= c <= 122:
                c -= 32
            h = ((h * 31) + c) & 0xFFFFFFFF
            
        k = bytearray(bytes.fromhex("99 64 b1 b0 6b 03 8d 7f b7 7d b6 a7 54 90 8b 73"))
        k0, k1, k2, k3 = (h & 0xFF, (h >> 8) & 0xFF, (h >> 16) & 0xFF, (h >> 24) & 0xFF)
        for i in range(len(k)):
            k[i] ^= (k0, k1, k2, k3)[i & 3]
        return bytes(k)

    @staticmethod
    def decrypt(all_code, name):
        key = JG._key(name)
        ct = all_code[8:]
        cipher = AES.new(key, AES.MODE_CBC, b"\x00" * 16)
        try:
            decrypted_data = cipher.decrypt(ct)
            return unpad(decrypted_data, AES.block_size)
        except (ValueError, KeyError):
            raise ValueError("Giải mã mã hóa AES lỗi: Sai key hoặc dữ liệu hỏng.")

    @staticmethod
    def encrypt(all_code, name):
        key = JG._key(name)
        original_len = len(all_code)
        pt_padded = pad(all_code, AES.block_size)
        
        cipher = AES.new(key, AES.MODE_CBC, b"\x00" * 16)
        ct = cipher.encrypt(pt_padded)
        hdr = JG.MAGIC + b"\x00" + original_len.to_bytes(4, "little")
        return hdr + ct


class ZSTD:
    @staticmethod
    def dec(all_code):
        compressed_data = all_code[8:]
        dctx = zstd.ZstdDecompressor(dict_data=zstd.ZstdCompressionDict(ZSTD_DICT))
        return dctx.decompress(compressed_data)

    @staticmethod
    def com(all_code):
        cctx = zstd.ZstdCompressor(level=17, dict_data=zstd.ZstdCompressionDict(ZSTD_DICT))
        compressed = bytearray(cctx.compress(all_code))
        compressed[0:0] = len(all_code).to_bytes(4, byteorder="little")
        compressed[0:0] = b"\"J\x00\xef"
        return compressed

def auto(file_path):
    try:
        with open(file_path, "rb") as f:
            all_code = f.read()
            
        if not all_code: 
            return

        if all_code[0:3] == JG.MAGIC:
            new_code = JG.decrypt(all_code, JG.get_name(file_path))
            with open(file_path, "wb") as f: f.write(new_code)
            print("\33[1;32mDECRYPT AES", file_path)
        elif all_code[0:4] == b"\"J\x00\xef":
            new_code = ZSTD.dec(all_code)
            with open(file_path, "wb") as f: f.write(new_code)
            print("\33[1;32mDECOMPRESS ZSTD", file_path)
        else:
            new_code = ZSTD.com(all_code)
            with open(file_path, "wb") as f: f.write(new_code)
            print("\33[1;36mENCOMPRESS ZSTD", file_path)
            
    except Exception as e:
        print(f"\33[1;31mERROR {file_path}: {e}")


def mode(file_path, mode):
    try:
        with open(file_path, "rb") as f:
            all_code = f.read()
            
        if not all_code: 
            return

        if mode == "COM_ZSTD":
            new_code = ZSTD.com(all_code)
            msg = "\33[1;36mENCOMPRESS ZSTD"
        elif mode == "DEC_ZSTD":
            new_code = ZSTD.dec(all_code)
            msg = "\33[1;32mDECOMPRESS ZSTD"
        elif mode == "ENC_AES":
            new_code = JG.encrypt(all_code, JG.get_name(file_path))
            msg = "\33[1;36mENCRYPT AES"
        elif mode == "DEC_AES":
            new_code = JG.decrypt(all_code, JG.get_name(file_path))
            msg = "\33[1;32mDECRYPT AES"
        else:
            return

        with open(file_path, "wb") as f:
            f.write(new_code)
        print(msg, file_path)
        
    except Exception as e:
        print(f"\33[1;31mERROR {file_path}: {e}")