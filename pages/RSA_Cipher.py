import random

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def mod_inverse(e, phi):
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
        d = y2 + phi

    return d

def generate_keypair(p, q):
    n = p * q
    phi = (p - 1) * (q - 1)
    e = random.randrange(1, phi)
    g = gcd(e, phi)

    while g != 1:
        e = random.randrange(1, phi)
        g = gcd(e, phi)

    d = mod_inverse(e, phi)
    return ((e, n), (d, n))

def encrypt(public_key, plaintext):
    e, n = public_key
    cipher_text = [pow(ord(char), e, n) for char in plaintext]
    return cipher_text

def decrypt(private_key, cipher_text):
    d, n = private_key
    plain_text = [chr(pow(char, d, n)) for char in cipher_text]
    return ''.join(plain_text)

# Example usage
p = 61
q = 53
public_key, private_key = generate_keypair(p, q)
message = "Hello Robo! How are you?"
cipher_text = encrypt(public_key, message)
decrypted_text = decrypt(private_key, cipher_text)

print(f"Public key: e={public_key[0]} n={public_key[1]}")
print(f"Cipher text: {cipher_text}")
print(f"Decrypted text: {decrypted_text}")
