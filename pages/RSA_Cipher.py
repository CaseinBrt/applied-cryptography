import streamlit as st
import random

def generate_prime(bits):
    # Generate a random prime number of specified bit length
    while True:
        num = random.getrandbits(bits)
        if is_prime(num):
            return num

def is_prime(n, k=5):
    # Miller-Rabin primality test
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0:
        return False

    # Write n as 2^r * d + 1
    d = n - 1
    r = 0
    while d % 2 == 0:
        d //= 2
        r += 1

    # Test primality k times
    for _ in range(k):
        a = random.randint(2, n - 2)
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True

def gcd(a, b):
    # Euclidean algorithm for finding greatest common divisor
    while b != 0:
        a, b = b, a % b
    return a

def multiplicative_inverse(e, phi):
    # Extended Euclidean algorithm for finding multiplicative inverse
    d = 0
    x1, x2 = 0, 1
    y1, y2 = 1, 0
    temp_phi = phi

    while e > 0:
        temp1 = temp_phi // e
        temp2 = temp_phi - temp1 * e
        temp_phi = e
        e = temp2

        x = x2 - temp1 * x1
        y = y2 - temp1 * y1

        x2 = x1
        x1 = x
        y2 = y1
        y1 = y

    if temp_phi == 1:
        return y2 + phi

def generate_keypair(bits):
    # Generate RSA key pair
    p = generate_prime(bits)
    q = generate_prime(bits)
    n = p * q
    phi = (p - 1) * (q - 1)

    while True:
        e = random.randrange(2, phi)
        if gcd(e, phi) == 1:
            break

    d = multiplicative_inverse(e, phi)
    return (e, n), (d, n)

def encrypt(public_key, plaintext):
    e, n = public_key
    cipher_text = [pow(ord(char), e, n) for char in plaintext]
    return cipher_text

def decrypt(private_key, cipher_text):
    d, n = private_key
    plain_text = [chr(pow(char, d, n)) for char in cipher_text]
    return ''.join(plain_text)

# Streamlit app
st.title("RSA Encryption and Decryption")
st.markdown("### RSA Key Generation, Encryption, and Decryption")

# Ask the user for the bit length of primes
bits = st.slider("Select the bit length for primes", min_value=32, max_value=1024, step=32, value=512)

# Generate RSA key pair
public_key, private_key = generate_keypair(bits)

# Ask the user for the plaintext message
plaintext = st.text_input("Enter the message to encrypt", "Hello, RSA!")

# Encrypt the message using the public key
encrypted_message = encrypt(public_key, plaintext)

# Display the encrypted message
st.markdown(f"**Encrypted message:** {encrypted_message}")

# Decrypt the message using the private key
decrypted_message = decrypt(private_key, encrypted_message)

# Display the decrypted message
st.markdown(f"**Decrypted message:** {decrypted_message}")
