import streamlit as st

def is_prime(num):
    if num <= 1:
        return False
    if num == 2:
        return True
    if num % 2 == 0:
        return False
    for i in range(3, int(num**0.5) + 1, 2):
        if num % i == 0:
            return False
    return True

def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

def generate_keypair(p, q):
    if not is_prime(p):
        st.error(f"p: {p} is not a prime number!")
        return None, None
    if not is_prime(q):
        st.error(f"q: {q} is not a prime number!")
        return None, None
    
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
    if public_key is None:
        return None
    e, n = public_key
    return [pow(ord(char), e, n) for char in message]

def decrypt(ciphertext, private_key):
    d, n = private_key
    return ''.join([chr(pow(char, d, n)) for char in ciphertext])

def main():
    st.title("RSA Encryption and Decryption")

    # Sidebar
    st.sidebar.title("RSA Parameters")
    p = st.sidebar.number_input("Value of Prime number p:", value=43, min_value=2, step=1)
    q = st.sidebar.number_input("Value of Prime number q:", value=41, min_value=2, step=1)

    # Generate keypair
    if st.sidebar.button("Gen new keypair"):
        public_key, private_key = generate_keypair(p, q)
    else:
        public_key, private_key = None, None

    # Display RSA parameters
    st.write("RSA Parameters")
    st.write(f"p: {p}")
    st.write(f"q: {q}")
    if public_key is not None and private_key is not None:
        st.write(f"n = {p}*{q} = {public_key[1]}")
        st.write(f"t = ({p}-1)*({q}-1) = {((p-1)*(q-1))}")
        st.write("e =", public_key[0])
        st.write("d =", private_key[0], f"= pow({public_key[0]}, -1, {(p - 1)*(q - 1)})")

    # Display message if 'p' is not prime
    if not is_prime(p):
        st.error(f"p: {p} is not a prime number!")

    # Encryption and Decryption
    st.subheader("RSA🔒🔑")
    message = st.text_input("Message:")
    encrypted_message = None
    if message:
        encrypted_message = encrypt(message, public_key)
        if encrypted_message:
            decrypted_message = decrypt(encrypted_message, private_key)
            st.write("Encryption")
            st.write(f"Public key: e = {public_key[0]} | n = {public_key[1]}")
            st.write("Deryption")
            st.write(f"Private key: d = {private_key[0]} ^ -1 mod {public_key[1]} = {private_key[1]} | n = {public_key[1]}")
            st.write("Message:")
            st.write(f"message: {message}")
            st.write(f"message: {[ord(char) for char in message]}")
            st.write("Cipher text:")
            st.write(encrypted_message)
            st.write("Cipher text:")
            st.write(''.join([chr(char) for char in encrypted_message]))

    # Display decryption key and invalid message
    if encrypted_message:
        st.subheader("Cipher text:")
        st.write(''.join([chr(char) for char in encrypted_message]))
        st.write("To Decrypt, use private key", f"{private_key[0]} | n = {public_key[1]}")
        st.subheader("Key:")
        key = st.number_input("1", value=1, step=1)
        st.subheader("n:")
        n_value = st.number_input("1", value=1, step=1)
        st.write("Invalid: �������������")

if __name__ == "__main__":
    main()
