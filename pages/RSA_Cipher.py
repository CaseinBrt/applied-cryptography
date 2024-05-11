import streamlit as st

def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

def generate_keypair(p, q):
    n = p * q
    t = (p - 1) * (q - 1)
    
    # Find e such that gcd(e, t) = 1
    for e in range(2, t):
        if gcd(e, t) == 1:
            break
    
    # Find d such that (d * e) % t == 1
    for d in range(2, t):
        if (d * e) % t == 1:
            break
    
    return (e, n), (d, n)

def encrypt(message, public_key):
    e, n = public_key
    return [pow(ord(char), e, n) for char in message]

def decrypt(ciphertext, private_key):
    d, n = private_key
    return ''.join([chr(pow(char, d, n)) for char in ciphertext])

def main():
    st.title("RSA Encryption and Decryption")

    # Sidebar
    st.sidebar.title("RSA Parameters")
    p = st.sidebar.number_input("Value of Prime number p:", value=43)
    q = st.sidebar.number_input("Value of Prime number q:", value=41)

    # Calculate n and t
    n = p * q
    t = (p - 1) * (q - 1)

    # Display RSA parameters
    st.write("RSA Parameters")
    st.write(f"Value of Prime number p:")
    st.write(f"{p}                        +-(we can add and minus)")
    st.write(f"Value of Prime number q:")
    st.write(f"{q}                        +-(we can add and minus)")
    st.write(f"p: {p}")
    st.write(f"q: {q}")
    st.write(f"n = {p}*{q} = {n}")
    st.write(f"t = ({p}-1)*({q}-1) = {t}")

    # Generate keypair
    if st.sidebar.button("Generate Key Pair"):
        public_key, private_key = generate_keypair(p, q)
        st.sidebar.write(f"gcd({public_key[0]}, {t}) = 1")
        st.sidebar.write(f"e = {public_key[0]}")
        st.sidebar.write(f"d = {private_key[0]} = pow({public_key[0]}, -1, {t})")

    # Main panel
    st.header("RSA🔒🔑")
    st.subheader("Encryption")
    if 'public_key' in locals():
        st.write(f"Public key: e = {public_key[0]} | n = {public_key[1]}")
        message = st.text_area("Enter your message for encryption:")
        if st.button("Encrypt"):
            if message:
                ciphertext = encrypt(message, public_key)
                st.write("Cipher text:", ciphertext)

    st.subheader("Decryption")
    if 'private_key' in locals():
        st.write(f"Private key: d = {private_key[0]} = pow({public_key[0]}, -1, {t}) | n = {private_key[1]}")
        encrypted_message = st.text_area("Enter cipher text (comma-separated):")
        if st.button("Decrypt"):
            if encrypted_message:
                ciphertext = [int(char) for char in encrypted_message.split(',') if char.strip().isdigit()]
                plaintext = decrypt(ciphertext, private_key)
                st.write("Decrypted message:", plaintext)

if __name__ == "__main__":
    main()
