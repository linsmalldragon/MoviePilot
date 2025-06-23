import base64
import json
import pickle
from cryptography.fernet import Fernet, InvalidToken

# 从二进制文件中提取出的两个最有可能的密钥
CANDIDATE_KEYS = [
    "I95rrnu0ZyWRS3o3rrzC7Z6Cw_QO7TOzdKB5YgZwXu0=",
    "c1qlByOVxi1-AnpLlYqJwP74XV9mF4GpKWUyjW1dXL8="
]
FILE_PATH = "./user.sites.v2.bin"
OUTPUT_FILE = "decrypted_sites_rules.json"


def decrypt_and_save():
    """
    尝试使用候选密钥解密文件并将内容保存到JSON文件。
    """
    try:
        with open(FILE_PATH, "rb") as f:
            encrypted_data = f.read()
    except FileNotFoundError:
        print(f"错误：加密文件未找到 at {FILE_PATH}")
        return

    saved = False
    for key_str in CANDIDATE_KEYS:
        try:
            print(f"正在尝试使用密钥: {key_str[:10]}...")
            key = key_str.encode()
            f = Fernet(key)
            decrypted_data = f.decrypt(encrypted_data)

            # 使用 pickle.loads() 来解析
            print("解密成功！正在使用 pickle 解析...")
            parsed_object = pickle.loads(decrypted_data)
            print("解析成功！正在将结果写入JSON文件...")

            with open(OUTPUT_FILE, "w", encoding="utf-8") as out_f:
                json.dump(parsed_object, out_f, ensure_ascii=False, indent=4)

            print(f"成功！已将解密后的数据保存到项目根目录下的 '{OUTPUT_FILE}' 文件中。")
            saved = True
            break
        except InvalidToken:
            print("密钥无效或数据被篡改，继续尝试下一个...")
            continue
        except Exception as e:
            print(f"使用密钥 {key_str[:10]}... 时发生错误: {e}")
            continue

    if not saved:
        print("解密失败，所有的候选密钥都无法解密文件。")


if __name__ == "__main__":
    decrypt_and_save() 