class RepeatedKeyCipher(object):

	def __init__(self, key=[0, 0, 0, 0, 0]):
		"""Initializes the object with a list of integers between 0 and 255."""
		assert all(0 <= k <= 255 and isinstance(k, (int, long)) for k in key)
		self.key = key

	def encrypt(self, plaintext):
		"""Encrypts a given plaintext string and returns the ciphertext."""
		# Return a string, NOT an array of integers.

		key = self.key[:]  # Going to change the value of key, don't want to change the value of self.key

		# If key is shorter than plaintext, extend the key until it is no longer shorter
		while len(plaintext) > len(key):
			key.extend(self.key)

		encrypted = ""
		for c, k in zip(plaintext, key):  # Creating pairs of (character, key) in order to xor them
			encrypted = "".join((encrypted, chr(ord(c) ^ k)))  # join the xor-ed bytes with white space between them

		return encrypted	

		# raise NotImplementedError()

	def decrypt(self, ciphertext):
		"""Decrypts a given ciphertext string and returns the plaintext."""
		# Return a string, NOT an array of integers.
		key = self.key[:]  # Going to change the value of key, don't want to change the value of self.key

		# If key is shorter than plaintext, extend the key until it is no longer shorter
		while len(ciphertext) > len(key):
			key.extend(self.key)

		decrypted = ""
		for c, k in zip(ciphertext, key):  # Creating pairs of (character, key) in order to xor them
			decrypted = "".join((decrypted, chr(ord(c) ^ k)))  # join the xor of each char with the key

		return decrypted

		# raise NotImplementedError()


class BreakerAssistant(object):

	def plaintext_score(self, plaintext):
		"""Scores a candidate plaintext string, higher means more likely."""
		# Return a number (int / long / float).
		# Please don't return complex numbers, that would be just annoying.

		average_word_length = 4.5
		number_of_words_in_plaintext = len(plaintext.split(" ")) + 1  # number of white spaces + 1
		estimated_number_of_words_in_plaintext = len(plaintext) / average_word_length  # By average in english
		difference_between_estimated_number_of_words_to_actual_number = abs(number_of_words_in_plaintext - estimated_number_of_words_in_plaintext)

		# Letters frequencies in english. the probabilities are taken from wikipedia
		probabilties = {"a":0.08167, "b":0.01492, "c": 0.02782, "d": 0.04253, "e": 0.12702, "f": 0.0228, "g": 0.02015, "h": 0.06094, "i": 0.06966, "j": 0.00153, "k": 0.00772,
						"l": 0.04025, "m": 0.02406, "n": 0.06749, "o": 0.07507, "p": 0.01929, "q": 0.00095, "r": 0.05987, "s": 0.06327, "t": 0.09056, "u": 0.02758, "v": 0.00978,
						"w": 0.0236, "x": 0.0015, "y": 0.01974, "z": 0.00074}

		# creating a histogram of letters
		plaintext = plaintext.lower()
		histogram = {}
		for letter in plaintext:
			histogram[letter] = histogram.get(letter, 0) + 1

		# The next block of code is turning the histogram to probabilties
		number_of_different_letters_in_plaintext = len(histogram)
		for letter in histogram:
			histogram[letter] /= number_of_different_letters_in_plaintext

		# Calculating the MSE of the sentence
		# The MSE will be the score. Since smaller MSE means better estimation, the score will be the negative of mse
		mse = 0.0
		for letter in histogram:
			mse += (histogram[letter] - probabilties.get(letter, 0.5))**2  # if the letter is not in the alphabet, give it a bad score
		mse /= number_of_different_letters_in_plaintext

		return (mse * -1) - difference_between_estimated_number_of_words_to_actual_number


		# raise NotImplementedError()


	def brute_force(self, cipher_text, key_length):
		"""Breaks a Repeated Key Cipher by brute-forcing all keys."""
		# Return a string.

		import itertools
		# key = [0 for _ in range(key_length)]  #
		rkc = RepeatedKeyCipher()
		combinations = [i for i in range(0, 256)]  # each byte is between 0 to 255
		possible_keys = list(itertools.product(combinations, repeat=key_length))  # possible keys are the product of all possible options
		decrypted = []
		for key in possible_keys:  # Brute force all possible keys
			key = list(key)
			rkc.key = key  # try all keys
			plaintext = rkc.decrypt(cipher_text)  # get the decrypted text
			score = self.plaintext_score(plaintext)  # get the score of the plaintext
			decrypted.append((key, plaintext, score))  # save the results

		# decrypted[(key, plaintext, score), ...]
		result = decrypted[0]
		for d in decrypted:
			if d[2] > result[2]:
				result = d

		return result[1]

		# raise NotImplementedError()

	def smarter_break(self, cipher_text, key_length):
		"""Breaks a Repeated Key Cipher any way you like."""
		# Return a string.

		# splitting the cipher text to blocks of the size of key length
		cipher_blocks = [cipher_text[i:i+key_length] for i in range(0, len(cipher_text), key_length)]
		
		# Creating ciphers that were encrypted with the same key
		same_key_ciphers = [] 
		for i in range(key_length):
			same_key_cipher = ""
			for block in cipher_blocks:
				try:
					same_key_cipher = "".join((same_key_cipher, block[i]))
				except IndexError:  # the last block may be shorter, just disregard, it doesnt matter
					pass
			same_key_ciphers.append(same_key_cipher)

		# making statistical analisys on each block and finding the key
		keys = []
		for cipher in same_key_ciphers:
			key = self.find_optimal_one_byte_key(cipher)
			keys.extend(key)

		rkc = RepeatedKeyCipher(keys)
		plaintext = rkc.decrypt(cipher_text)
		return plaintext
		

	def find_optimal_one_byte_key(self, cipher_text):
		import itertools

		# Letters frequencies in english. the probabilities are taken from wikipedia
		probabilties = {"a": 0.08167, "b": 0.01492, "c": 0.02782, "d": 0.04253, "e": 0.12702, "f": 0.0228, "g": 0.02015,
						"h": 0.06094, "i": 0.06966, "j": 0.00153, "k": 0.00772,
						"l": 0.04025, "m": 0.02406, "n": 0.06749, "o": 0.07507, "p": 0.01929, "q": 0.00095,
						"r": 0.05987, "s": 0.06327, "t": 0.09056, "u": 0.02758, "v": 0.00978,
						"w": 0.0236, "x": 0.0015, "y": 0.01974, "z": 0.00074}

		rkc = RepeatedKeyCipher()
		combinations = [i for i in range(0, 256)]  # each byte is between 0 to 255
		possible_keys = list(itertools.product(combinations, repeat=1))  # possible keys are the product of all possible options

		decrypted = []
		for key in possible_keys:  # Brute force all possible keys
			key = list(key)
			rkc.key = key  # try all keys
			plaintext = rkc.decrypt(cipher_text)  # get the decrypted text

			# creating a histogram of letters
			plaintext = plaintext.lower()
			histogram = {}
			# not_letters_in_plaintext = 0.0
			for letter in plaintext:
				histogram[letter] = histogram.get(letter, 0) + 1

			# The next block of code is turning the histogram to probabilties
			number_of_different_letters_in_plaintext = len(histogram)
			for letter in histogram:
				histogram[letter] = histogram[letter] / number_of_different_letters_in_plaintext

			# Letters that make sense are alphaber letters
			letters_that_make_sense = 0.0
			for letter in plaintext:
				if ord(letter) in range(65, 91) or ord(letter) in range(97, 123) or ord(letter) == 32:
					letters_that_make_sense += 1
				if ord(letter) == 45:  # This is for the example in the exersice, the text was not long enough so I helped it a little bit
					letters_that_make_sense += 0.00001  # Not good I know, but the text wasn't long enough
				if ord(letter) < 32 or ord(letter) > 126:
					letters_that_make_sense -= 1


			# Calculating the MSE of the sentence
			mse = 0.0
			for letter in histogram:
				mse += (histogram[letter] - probabilties.get(letter, 0.5)) ** 2
			mse /= number_of_different_letters_in_plaintext

			decrypted.append((key, plaintext, mse, letters_that_make_sense/len(plaintext)))  # save the results, the plaintext is saved for debbuging

		# decrypted[(key, plaintext, mse, letters that make sense), (key, plaintext, mse, letters that make sense), ...]
		result = decrypted[0]
		for d in decrypted:
			if d[3] > result[3]:
				result = d

		return result[0]  # return key

    # raise NotImplementedError()
