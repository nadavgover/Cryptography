from q2_atm import ATM, ServerResponse


def extract_PIN(encrypted_PIN):
    """Extracts the original PIN string from an encrypted PIN."""
    # Return an integer.

    # Brute force all the options
    atm = ATM()

    for pin in xrange(1000, 10000):
        msg = atm.encrypt_PIN(pin)
        if msg == encrypted_PIN:
            return pin


    #raise NotImplementedError()


def extract_credit_card(encrypted_credit_card):
    """Extracts a credit card number string from its ciphertext."""
    # Return an integer.

    # This solution is correct only for small e
    import math

    atm = ATM()
    card_key = atm.rsa_card
    n = card_key.n
    e = card_key.e

    return int(math.ceil((10 ** (math.log(encrypted_credit_card, 10) / e))))  # This is never an int, so need to take or floor or ceiling value. ceiling was decided


    # raise NotImplementedError()


def forge_signature():
    """Forge a server response that passes verification."""
    # Return a ServerResponse instance.

    # Since the message is 1, the encryption will always be 1
    sr = ServerResponse(1, 1)
    return sr

    # raise NotImplementedError()
