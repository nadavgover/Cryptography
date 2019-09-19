# Cryptography

## Stream Cipher
In this project we focus on a simple stream cipher called Repeated Key cipher. A repeated key cipher works by XOR-ing the bytes of the plaintext with the bytes of the key similarly to a one-time pad:

* The first byte of the plaintext is XOR-ed with the first byte of the key
* The second byte of the plaintext is XOR-ed with the second byte of the key
* ...
* If the plaintext is longer than the key, start using the key again from the beginning (first it’s first byte, then it’s second byte, etc.)

### Plaintext Score
We have the `plaintext_score` method in the `BreakerAssistant` class.<br/> 
The method takes a string (of any length) and returns a numeric score such that a string containing a plausible text in English will receive (with a high probability) a higher score than a random string of the same length.

* For example, it gives this string "I am a sentence!" a higher score than "\xc6\xc9u\xd0v\x14\xe2\xcf\xc5\xf5\x1eZ\x10Yd\xd3".

In this project, this is done by comparing the letter frequency in the plaintext to the well known studied frequency of letters in the English language.
The way it was implemeted was creating a histogram of letters in the plain text, afterwards turning this histogram into probabilties by dividing each letter by the number of letters. 
Then we needed to come up with an error estimation, a way to measure if the frequency of letters is consistent with English.
The error measure is chosen to be the MSE (mean square average). This was implemented by taking the difference between the frequency of the letters in the plaintext (in the histogram) and the frequency of letters in English. Then squaring this difference.
Summing all the differences together and dividing by the number of letters to get the mean.
This gave us a number between 0-1, the closer to zero means less error and therefore means more probable to be english. Since we want to make a score that a higher score is better so we simply multiply the mse by -1.
This method alone might work for long texts, where the frequency of letters are lined up.

### Brute Force
There is also the `brute_force` method in the `BreakerAssistant` class.<br/>
The function receives a key length, attempts all possible keys of the given length, evaluates the plaintext possibilities using the plaintext_score, and returns the “correct” plaintext.

### Smarter Break
The problem with the brute force method is, well, that it’s brute force.<br/>
This means we try many attempts without much thought. Trying to a break a key longer than a few bytes is going to be impractical (as we need 2<sup>8(number of bytes)</sup> attempts).<br/>
So we need to find a way which is much faster, and for example, can break a key of length 10 or higher. And we may assume the ciphertext is long.

We can take advantage of the fact that we know the encryption algorithm and based on the assumption that the ciphertext is long.
The way decided here to take advantage of the poor encryption algorithm is to make the cipher text to blocks in the size of the key length. Since every byte of the ciphertext in steps of the size of key length was encrypted with the same byte of the key, we can say that it was encrypted with a key of the length of one!!! Now all we have to do is break the one byte key by brutefoce.
Well this is not a hard task, we just iterate over all 256 options, take a score and return the best score.
We obviously need to do that as many times as the length of the key, but every time it is just brute forcing a key with length of 1. This fact makes it a not time consuming method and therefore feasible.

You can see that in action in the `smarter_break` method in the `BreakerAssistant` class.

## RSA
In this section we broke several simplistic schemes that are based on RSA.

### Overview
Inside `q2_atm.py`, you can find the code for a (hypothetical) ATM.<br/>
After inserting the credit card, the machine sends both the credit card and the PIN code the user entered, to a remote server for verification. Once the server responds, the ATM verifies the response and if it’s valid, it gives the user his money.

When a user enters a 4-digit PIN code, the machine encrypts it with a 2048 bit RSA public key before sending it to the server.<br/>
The problem with that is since we know the pin is a 4 digit number, we can iterate through all possible options and encrypt them using the encryption method of RSA. we can compare each option with the encrypted pin we intercepted.
Then we returned the matched pin.<br/>
You can see that in action `q2.py` in the `extract_PIN` method.

The same ATM machine also sends the encrypted credit card number, a 8-9 digit number, to the server. Since the developers of the ATM were paranoid, they encrypted the credit card number with a different 2048 bit RSA key.<br/>
Inside `q2.py`, you can see the `extract_card` method. The method receives an encrypted credit card and returns the original card number.<br/>
This time the vulnerability is that e is small (e = 3).
We notice that the biggest credit card number is 999999999 and that this number to the power of e is less than n.
So we can say that this solution is correct only for small e.
We remember that in RSA the encryption is c = m<sup>e</sup> (mod n), but in this case, since m<sup>e</sup> is less than n, c = m<sup>e</sup>.
So we can take the logarithm of both sides (Let's say base 10, doesn't matter).
Computing the log of this number is not hard computationaly. 
After all algebra we get m = 10<sup>(log(c) / e)</sup>









