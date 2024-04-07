from clases import Token, ErrorLexico
import re
def analizador_lexico(area_texto_inicial, area_texto_final):
    tokens = []
    errores_lexicos = []
    palabra = ""
    dentro_cadena = False  
    
    texto = area_texto_inicial.get("1.0", "end")
    fila = 1
    columna = 0
    for char in texto:
        columna += 1
        if char == '"':
            dentro_cadena = not dentro_cadena
            palabra += char
            continue
        if dentro_cadena:
            palabra += char
            continue
        
        if char.isalnum(): 
            palabra += char
        else:
            if palabra:
                
                if palabra in ['Inicio', 'Encabezado', 'TituloPagina', 'Cuerpo', 'Titulo', 'texto', 'posicion', 'tamaño', 'color', 'Fondo', 'Parrafo', 'fuente', 'Texto', 'Codigo', 'Negrita', 'Subrayado', 'Tachado', 'Cursiva', 'Tabla', 'filas', 'columnas', 'elemento', 'fila', 'columna', 'Salto', 'cantidad']:
                    tokens.append(Token("Palabra Reservada", palabra, fila, columna - len(palabra)))
                elif palabra.isdigit():
                    tokens.append(Token("Número", palabra, fila, columna - len(palabra)))
                else:
                    tokens.append(Token("Cadena", palabra, fila, columna - len(palabra)))
                palabra = ""
            
            if char in [',', '.', '{', '}', ':', '[', ']', '=']:
                tokens.append(Token("Carácter Especial", char, fila, columna))
            elif char == ';':
                tokens.append(Token("Punto y Coma", char, fila, columna))
            elif char == ' ':
                continue
            elif char == '\n':
                fila += 1
                columna = 0  
                continue                                        
            else:
                errores_lexicos.append(ErrorLexico(f"Carácter no reconocido: {char}", fila, columna))
    
    
    if palabra:
        if palabra in ['Inicio', 'Encabezado', 'TituloPagina', 'Cuerpo', 'Titulo', 'texto', 'posicion', 'tamaño', 'color', 'Fondo', 'Parrafo', 'fuente', 'Texto', 'Codigo', 'Negrita', 'Subrayado', 'Tachado', 'Cursiva', 'Tabla', 'filas', 'columnas', 'elemento', 'fila', 'columna', 'Salto', 'cantidad']:
            tokens.append(Token("Palabra Reservada", palabra, fila, columna - len(palabra)))
        elif palabra.isdigit():
            tokens.append(Token("Número", palabra, fila, columna - len(palabra)))
        else:
            tokens.append(Token("Cadena", palabra, fila, columna - len(palabra)))
    
    imprimir_tokens_y_errores(tokens, errores_lexicos)
    return tokens, errores_lexicos
    
    

def imprimir_tokens_y_errores(tokens, errores_lexicos):
    # Escribir los errores en un archivo HTML
    with open("errores.html", "w", encoding='utf-8') as f:
        f.write("<html>\n<head>\n<title>Errores Léxicos</title>\n</head>\n<body>\n")
        f.write("<h1>Errores Léxicos</h1>\n")
        f.write("<table border='1'>\n")
        f.write("<tr><th>Caracter Inválido</th><th>Cantidad</th><th>Fila</th><th>Columna</th></tr>\n")
        caracteres_invalidos = {}
        for error in errores_lexicos:
            if error.mensaje not in caracteres_invalidos:
                caracteres_invalidos[error.mensaje] = {"cantidad": 1, "fila": error.fila, "columna": error.columna}
            else:
                caracteres_invalidos[error.mensaje]["cantidad"] += 1
        for caracter, info in caracteres_invalidos.items():
            f.write(f"<tr><td>{caracter}</td><td>{info['cantidad']}</td><td>{info['fila']}</td><td>{info['columna']}</td></tr>\n")
        f.write("</table>\n")
        f.write("</body>\n</html>")

        # Escribir los tokens en un archivo HTML
    with open("tokens.html", "w", encoding='utf-8') as f:
        f.write("<html>\n<head>\n<title>Listado de Tokens</title>\n</head>\n<body>\n")
        f.write("<h1>Listado de Tokens</h1>\n")
        f.write("<table border='1'>\n")
        f.write("<tr><th>Tipo de Token</th><th>Valor</th><th>Línea</th><th>Columna</th></tr>\n")
        for token in tokens:
            f.write(f"<tr><td>{token.tipo}</td><td>{token.valor}</td><td>{token.linea}</td><td>{token.columna}</td></tr>\n")
        f.write("</table>\n")
        f.write("</body>\n</html>")

def analizar_texto(texto):
    tokens = []
    # Patrones para buscar los tokens y sus valores
    patrones = {
        'INICIO': r'Inicio:\s*{',
        'ENCABEZADO': r'Encabezado:\s*{',
        'TITULOPAGINA': r'TituloPagina:\s*\"(.*?)\";',
        'POSICION': r'posicion:\s*\"(.*?)\"',
        'TAMAÑO': r'tamaño:\s*\"(.*?)\"',
        'CUERPO': r'Cuerpo:\s*\[([^]]+)\]',
        'TITULO': r'Titulo:\s*{([^}]+)}',
        'PARRAFO': r'Parrafo:\s*{([^}]+)}',
        'FONDO': r'Fondo:\s*{([^}]+)}',
        'TEXTO': r'Texto:\s*{([^}]+)}',
        'CODIGO': r'Codigo:\s*{([^}]+)}',
        'NEGRITA': r'Negrita:\s*{([^}]+)}',
        'SUBRAYADO': r'Subrayado:\s*{([^}]+)}',
        'TACHADO': r'Tachado:\s*{([^}]+)}',
        'CURSIVA': r'Cursiva:\s*{([^}]+)}',
        'SALTO': r'Salto:\s*{cantidad:\s*\"(\d+)\"\s*};',
        'TABLA': r'Tabla:\s*{([^}]+)}'
    }
    
    # Buscar los patrones en el texto y extraer los tokens y valores
    for token, patron in patrones.items():
        matches = re.findall(patron, texto, re.MULTILINE | re.DOTALL)
        for match in matches:
            tokens.append((token, match))
    
    print("Tokens encontrados:")
    for token in tokens:
        print(token)
    
    return tokens