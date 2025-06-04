#funcion para decodificar texto de windows-1252 a utf-8
def decode_win1252(text):
    if text is None:
        return None
    return text.encode('latin1').decode('windows-1252').encode('utf-8')