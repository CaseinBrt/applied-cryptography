import streamlit as st
from sympy import mod_inverse, isprime

def check_prime(p, q):
    if not isprime(p):
        st.error(f"p: {p} is not a prime number!")
    if not isprime(q):
        st.error(f"q: {q} is not a prime number!")

def rsa(p, q, message):
    check_prime(p, q)
    
    n = p * q
    t = (p - 1) * (q - 1)

    # Choose e such that 1 < e < t and e is co-prime with t
    for i in range(2, t):
        if t % i != 0:
            e = i
            break
    
    # Compute d such that (d * e) % t = 1
    d = mod_inverse(e, t)
    
    # Encryption: c = m^e mod n
    cipher_text = [pow(ord(char), e, n) for char in message]
    
    # Decryption: m = c^d mod n
    decrypted_text = ''.join([chr(pow(char, d, n)) for char in cipher_text])
    
    return e, d, n, cipher_text, decrypted_text

st.title("RSA Encryption and Decryption")
st.sidebar.header("RSA Parameters")

p = st.sidebar.number_input("Value of Prime number p:", min_value=2, step=1)
q = st.sidebar.number_input("Value of Prime number q:", min_value=2, step=1)

e, d, n, cipher_text, decrypted_text = rsa(p, q, "Hello Shiella")

st.sidebar.markdown(f"n = {n}")
st.sidebar.markdown(f"t = {(p-1) * (q-1)}")

if st.sidebar.button("Generate New Keypair"):
    pass  # Implement keypair generation here

st.write("RSA🔒🔑")
st.write("Encryption")
st.write(f"Public key: e = {e} | n = {n}")
st.write("Decryption")
st.write(f"Private key: d = {d} ^ -1 mod {n} = {d} | n = {n}")

message = st.text_input("Enter a message:")
cipher_text_str = ', '.join(map(str, cipher_text))
st.write(f"Message: {message} (inside a box, press Ctrl+Enter to execute)")
st.write(f"Message (ASCII values): {cipher_text_str}")

st.write("Cipher text:")
st.write(cipher_text_str)  # Display cipher text inside a box

st.write("To Decrypt, use private key:")
st.write(f"{d} | n = {n} (Highlighted with blue color like a box form)")

# Implement decryption key input and display here

st.write("Invalid: �������������")  # Placeholder for invalid decryption

# Implement decryption logic here

# Right side of the Streamlit app (results display)
st.write("Cipher text:")
st.write("ϱ؇ÓÓʝϸڠΥ؇ÓÓԚ (inside a box)")

st.write("To Decrypt, use private key:")
st.write(f"{d} | n = {n} (Highlighted with blue color like a box form)")

# Implement decryption key input and display here

st.write("Invalid: �������������")  # Placeholder for invalid decryption

# Implement decryption logic here
