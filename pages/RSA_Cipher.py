from sympy.ntheory.primetest import isprime
from sympy.core.numbers import mod_inverse

def generate_keypair(p, q):
    n = p * q
    t = (p - 1) * (q - 1)
    e = 65537  # commonly used value for e
    d = mod_inverse(e, t)
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

    # Generate keypair
    if st.sidebar.button("Generate Key Pair"):
        if isprime(p) and isprime(q):
            public_key, private_key = generate_keypair(p, q)
            st.sidebar.write(f"Public key: e = {public_key[0]} | n = {public_key[1]}")
            st.sidebar.write(f"Private key: d = {private_key[0]} | n = {private_key[1]}")
        else:
            st.sidebar.error("Both p and q must be prime numbers.")

    # Main panel
    st.header("RSA Encryption and Decryption")
    message = st.text_area("Enter your message:")
    if st.button("Encrypt"):
        if message:
            if 'public_key' in locals():
                ciphertext = encrypt(message, public_key)
                st.write("Cipher text:", ciphertext)
            else:
                st.error("Please generate key pair first.")

    encrypted_message = st.text_area("Enter cipher text (comma-separated):")
    if st.button("Decrypt"):
        if encrypted_message:
            ciphertext = [int(char) for char in encrypted_message.split(',')]
            if 'private_key' in locals():
                plaintext = decrypt(ciphertext, private_key)
                st.write("Decrypted message:", plaintext)
            else:
                st.error("Please generate key pair first.")

if __name__ == "__main__":
    main()
