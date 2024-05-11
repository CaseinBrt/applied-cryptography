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
    st.write(f"p: {p}")
    st.write(f"q: {q}")
    st.write(f"n = {p}*{q} = {n}")
    st.write(f"t = ({p}-1)*({q}-1) = {t}")

    # Generate keypair
    if st.sidebar.button("Generate Key Pair"):
        public_key, private_key = generate_keypair(p, q)
        st.sidebar.write(f"Public key: e = {public_key[0]}")
        st.sidebar.write(f"Private key: d = {private_key[0]}")

    # Main panel
    st.header("RSA Encryption and Decryption")
    # Rest of the code for encryption and decryption...

if __name__ == "__main__":
    main()
