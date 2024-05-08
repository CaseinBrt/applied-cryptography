import streamlit as st
from Crypto.Cipher import ARC4
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Random import get_random_bytes
import base64
from io import BytesIO

def rc4_encrypt(message, key):
    cipher = ARC4.new(key)
    ciphertext = cipher.encrypt(message)
    return ciphertext

def rc4_decrypt(ciphertext, key):
    cipher = ARC4.new(key)
    decrypted_message = cipher.decrypt(ciphertext)
    return decrypted_message

def main():
    st.title("RC4 Encryption App")

    mode = st.sidebar.radio("Mode", ("Encrypt Text", "Decrypt Text", "Encrypt File", "Decrypt File"))

    key = st.sidebar.text_input("Enter Key", type="password")
    iv = st.sidebar.text_input("Enter IV (Initialization Vector)", type="password")
    salt = st.sidebar.text_input("Enter Salt", type="password")

    if mode in ["Encrypt Text", "Decrypt Text"]:
        text = st.text_area("Enter Text to Process")
        if st.button(mode):
            if not key:
                st.error("Please enter a key")
            else:
                derived_key = PBKDF2(key, salt.encode(), dkLen=16, count=1000000)
                if mode == "Encrypt Text":
                    if not text:
                        st.error("Please enter text to encrypt")
                    else:
                        encrypted_text = rc4_encrypt(text.encode(), derived_key)
                        encrypted_text_base64 = base64.b64encode(encrypted_text).decode('utf-8')
                        st.text_area("Processed Text", value=encrypted_text_base64, height=200)
                else:
                    if not text:
                        st.error("Please enter text to decrypt")
                    else:
                        try:
                            encrypted_text_bytes = base64.b64decode(text)
                        except base64.binascii.Error as e:
                            st.error("Invalid base64 encoded string. Please check the input and try again.")
                        else:
                            decrypted_text = rc4_decrypt(encrypted_text_bytes, derived_key)
                            st.text_area("Processed Text", value=decrypted_text.decode(), height=200)
    
    elif mode in ["Encrypt File"]:
        file = st.file_uploader("Upload File", type=["txt", "pdf"])
        if st.button(mode):
            if not key:
                st.error("Please enter a key")
            elif not file:
                st.error("Please upload a file")
            else:
                file_contents = file.read()
                derived_key = PBKDF2(key, salt.encode(), dkLen=16, count=1000000)
                if mode == "Encrypt File":
                    encrypted_file_contents = rc4_encrypt(file_contents, derived_key)
                    encrypted_file_contents_base64 = base64.b64encode(encrypted_file_contents).decode('utf-8')
                    st.download_button(
                        label="Download Encrypted File",
                        data=BytesIO(encrypted_file_contents_base64.encode()),
                        file_name="encrypted_file.txt",
                        mime="text/plain"
                    )
    elif mode == "Decrypt File":
        file = st.file_uploader("Upload File", type=["txt", "pdf"])
        if st.button(mode):
            if not key:
                st.error("Please enter a key")
            elif not file:
                st.error("Please upload a file")
            else:
                file_contents = file.read()
                derived_key = PBKDF2(key, salt.encode(), dkLen=16, count=1000000)
                try:
                    decrypted_file_contents_bytes = base64.b64decode(file_contents)
                except base64.binascii.Error as e:
                    st.error("Invalid base64 encoded file. Please check the input and try again.")
                else:
                    decrypted_file_contents = rc4_decrypt(decrypted_file_contents_bytes, derived_key)
                    st.text_area("Decrypted File", value=decrypted_file_contents.decode(), height=200)

if __name__ == "__main__":
    main()