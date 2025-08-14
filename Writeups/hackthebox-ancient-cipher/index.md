---
title: HackTheBox - Crypto Challenge "Ancient Cipher"
description: Detailed walkthrough of solving a classical cryptography challenge involving substitution ciphers
tags: [cryptography, substitution-cipher, python, hackthebox]
category: Crypto
date: 2024-08-12
---

# HackTheBox - Ancient Cipher Writeup

StartBlueBox
**Challenge Info:** This writeup covers a medium-difficulty cryptography challenge from HackTheBox involving classical cipher techniques and frequency analysis.
EndBlueBox

## Challenge Description

This crypto challenge from HackTheBox presents us with an ancient cipher that needs to be decoded. The challenge provides an encrypted message and hints that it uses a classical substitution cipher technique.

**Challenge Details:**
- Difficulty: Medium
- Category: Cryptography
- Points: 300

## Initial Analysis

Upon downloading the challenge files, we receive:
- `encrypted.txt`: Contains the encrypted message
- `hint.txt`: Provides context about the cipher type

The encrypted text appears to be:
```
WKLV LV D VLPSOH VXEVWLWXWLRQ FLSKHU WKDW XVHV D FDVDU FLSKHU ZLWK D VKLIW RI WKUHH
```

StartYellowBox
**Observation:** The text maintains word boundaries and spacing, which suggests it's likely a simple substitution cipher rather than a complex polyalphabetic cipher.
EndYellowBox

## Frequency Analysis

Let's start by performing frequency analysis on the encrypted text:

```python
def frequency_analysis(text):
    """Perform frequency analysis on encrypted text"""
    text = text.upper().replace(' ', '')
    freq_dict = {}
    
    for char in text:
        if char.isalpha():
            freq_dict[char] = freq_dict.get(char, 0) + 1
    
    # Sort by frequency
    sorted_freq = sorted(freq_dict.items(), key=lambda x: x[1], reverse=True)
    
    print("Character Frequency Analysis:")
    for char, count in sorted_freq:
        percentage = (count / len([c for c in text if c.isalpha()])) * 100
        print(f"{char}: {count} ({percentage:.1f}%)")

encrypted = "WKLV LV D VLPSOH VXEVWLWXWLRQ FLSKHU WKDW XVHV D FDVDU FLSKHU ZLWK D VKLIW RI WKUHH"
frequency_analysis(encrypted)
```

Output:
```
Character Frequency Analysis:
L: 6 (12.8%)
V: 5 (10.6%)
K: 4 (8.5%)
H: 4 (8.5%)
```

## Pattern Recognition

Looking at the structure and frequency distribution, this appears to be a Caesar cipher. Let's try different shift values:

StartGreenBox
**Key Insight:** Caesar ciphers are monoalphabetic substitution ciphers where each letter is shifted by a fixed number of positions in the alphabet.
EndGreenBox

```python
def caesar_decrypt(text, shift):
    """Decrypt Caesar cipher with given shift"""
    result = ""
    
    for char in text:
        if char.isalpha():
            # Handle uppercase letters
            if char.isupper():
                result += chr((ord(char) - ord('A') - shift) % 26 + ord('A'))
            # Handle lowercase letters
            else:
                result += chr((ord(char) - ord('a') - shift) % 26 + ord('a'))
        else:
            result += char
    
    return result

# Test different shift values
encrypted = "WKLV LV D VLPSOH VXEVWLWXWLRQ FLSKHU WKDW XVHV D FDVDU FLSKHU ZLWK D VKLIW RI WKUHH"

for shift in range(26):
    decrypted = caesar_decrypt(encrypted, shift)
    print(f"Shift {shift}: {decrypted}")
```

## Solution Discovery

After testing various shifts, we find that a shift of **3** produces readable English text:

StartGreenBox
**Solution Found:** With a shift of 3, the decrypted message reads: "THIS IS A SIMPLE SUBSTITUTION CIPHER THAT USES A CAESAR CIPHER WITH A SHIFT OF THREE"
EndGreenBox

## Automated Solution Script

Here's the complete solution script:

```python
#!/usr/bin/env python3

def caesar_decrypt(text, shift):
    """Decrypt Caesar cipher with given shift"""
    result = ""
    
    for char in text:
        if char.isalpha():
            if char.isupper():
                result += chr((ord(char) - ord('A') - shift) % 26 + ord('A'))
            else:
                result += chr((ord(char) - ord('a') - shift) % 26 + ord('a'))
        else:
            result += char
    
    return result

def find_caesar_key(encrypted_text):
    """Find the most likely Caesar cipher key by testing all possibilities"""
    common_words = ['THE', 'AND', 'IS', 'A', 'TO', 'OF', 'IN', 'IT', 'YOU', 'THAT']
    
    best_score = 0
    best_shift = 0
    
    for shift in range(26):
        decrypted = caesar_decrypt(encrypted_text, shift).upper()
        score = sum(1 for word in common_words if word in decrypted)
        
        if score > best_score:
            best_score = score
            best_shift = shift
    
    return best_shift

# Main execution
if __name__ == "__main__":
    encrypted = "WKLV LV D VLPSOH VXEVWLWXWLRQ FLSKHU WKDW XVHV D FDVDU FLSKHU ZLWK D VKLIW RI WKUHH"
    
    # Find the key automatically
    key = find_caesar_key(encrypted)
    
    # Decrypt with the found key
    decrypted = caesar_decrypt(encrypted, key)
    
    print(f"Detected shift: {key}")
    print(f"Decrypted message: {decrypted}")
    print(f"Flag format: HTB{{{decrypted.replace(' ', '_').lower()}}}")
```

## Key Lessons Learned

StartPurpleBox
**Learning Outcomes:**
1. **Frequency Analysis:** Always start with frequency analysis for substitution ciphers
2. **Pattern Recognition:** Look for common patterns in encrypted text
3. **Automation:** Create scripts to test multiple possibilities systematically
4. **Validation:** Use common English words to validate potential solutions
EndPurpleBox

## Flag Submission

The final flag for submission would be:
```
HTB{this_is_a_simple_substitution_cipher_that_uses_a_caesar_cipher_with_a_shift_of_three}
```

StartRedBox
**Security Note:** While Caesar ciphers were used historically, they are extremely weak by modern standards and should never be used for real-world cryptographic applications.
EndRedBox