import streamlit as st
from Crypto.Cipher import ARC4
from Crypto.Protocol.KDF import PBKDF2
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
    st.title("Rivest Cipher 4🔐")

    mode = st.radio("Mode", ("Encrypt Text", "Decrypt Text", "Encrypt File", "Decrypt File"))
    key = st.text_input("Enter Key", type="password")
    salt = st.text_input("Enter Salt", type="password")

    if mode == "Encrypt File" or mode == "Decrypt File":
        file = st.file_uploader("Upload File", type=["pdf", "txt"], accept_multiple_files=False)
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
                    st.download_button(
                        label="Download Encrypted File",
                        data=BytesIO(encrypted_file_contents),
                        file_name="encrypted_file" + file.name[-4:],
                        mime="application/octet-stream"
                    )
                else:
                    decrypted_file_contents = rc4_decrypt(file_contents, derived_key)
                    st.download_button(
                        label="Download Decrypted File",
                        data=BytesIO(decrypted_file_contents),
                        file_name="decrypted_file" + file.name[-4:],
                        mime="application/octet-stream"
                    )

    else:
        text = st.text_area("Enter Text to Process")
        if st.button(mode):
            if not key:
                st.error("Please enter a key")
            elif not text:
                st.error("Please enter text to process")
            else:
                derived_key = PBKDF2(key, salt.encode(), dkLen=16, count=1000000)
                if mode == "Encrypt Text":
                    encrypted_text = rc4_encrypt(text.encode(), derived_key)
                    st.text_area("Processed Text", value=base64.b64encode(encrypted_text).decode(), height=200)
                else:
                    try:
                        encrypted_text_bytes = base64.b64decode(text)
                        decrypted_text = rc4_decrypt(encrypted_text_bytes, derived_key)
                        st.text_area("Processed Text", value=decrypted_text.decode(), height=200)
                    except base64.binascii.Error as e:
                        st.error("Invalid base64 encoded string. Please check the input and try again.")

if __name__ == "__main__":
    main()
