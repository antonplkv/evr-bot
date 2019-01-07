
def get_service_text():
    f = open('service', 'r', encoding= 'cp1251')
    text = f.read()
    f.close()
    return text