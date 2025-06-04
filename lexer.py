import ply.lex as lex
import json
import io
import sys

class LexerAnalyzer:
    def __init__(self):
        self.errores = 0
        self.tokens_identificados = []
        self.lexer = None
        self._build_lexer()
    
    def _build_lexer(self):
        """Construye el lexer con todas las definiciones de tokens"""
        
        # Definición de tokens
        self.tokens = ('LLAVE_IZQ','COMA','LLAVE_DER','CORCHETE_IZQ','CORCHETE_DER','DOS_PUNTOS','LISTA_EQUIPOS','VERSION','EQUIPO','EQUIPOS', 'LINK',
                      'NOMB_EQUIPO','IDENTIDAD','DIRECCION','ASIGNATURA','CARRERA','UNIVERSIDAD','ALIANZA','INTEGRANTES','CALLE','CIUDAD','PAIS',
                      'NOMBRE','EDAD','CARGO','FOTO','EMAIL','DIREMAIL','HABILIDADES','SALARIO','ACTIVO','PROYECTOS','PROYECTO','DATE',
                      'P_NOMBRE','P_ESTADO','P_RESUMEN','P_VIDEO','P_CONCLUSION','TAREAS','FECHA_INI','FIRMA','FECHA_FIN','URL','ROL','P_PROGRESO','ERROR','STRING','BOOL','FLOAT','INTEGER','GUION')
        
        # Reglas de tokens simples
        self.t_ignore = ' \t'
        self.t_COMA = r'\,'
        self.t_DOS_PUNTOS = r'\:'
        self.t_CORCHETE_IZQ = r'\['
        self.t_CORCHETE_DER = r'\]'
        self.t_LLAVE_IZQ = r'\{'
        self.t_LLAVE_DER = r'\}'
        self.t_INTEGER = r'\d+'
        self.t_FLOAT = r'[+-]?(\d+\.\d\d)'
        
        # Crear el lexer
        self.lexer = lex.lex(module=self)
    
    # Funciones de tokens (copiadas de tu código original)
    def t_EQUIPOS(self, t):
        r'"equipos"'
        return t

    def t_EQUIPO(self, t):
        r'"equipo"'
        return t

    def t_NOMB_EQUIPO(self, t):
        r'"nombre_equipo"'
        return t

    def t_IDENTIDAD(self, t):
        r'"identidad_equipo"'
        return t

    def t_LINK(self, t):
        r'"link"'
        return t

    def t_ASIGNATURA(self, t):
        r'"asignatura"'
        return t

    def t_CARRERA(self, t):
        r'"carrera"'
        return t

    def t_UNIVERSIDAD(self, t):
        r'"universidad_regional"'
        return t

    def t_DIRECCION(self, t):
        r'"dirección"'
        return t

    def t_CALLE(self, t):
        r'"calle"'
        return t

    def t_CIUDAD(self, t):
        r'"ciudad"'
        return t

    def t_PAIS(self, t):
        r'"país"'
        return t

    def t_ALIANZA(self, t):
        r'"alianza_equipo"'
        return t

    def t_INTEGRANTES(self, t):
        r'"integrantes"'
        return t

    def t_NOMBRE(self, t):
        r'"nombre"'
        t.value = t.value[1:-1]
        return t

    def t_EDAD(self, t):
        r'"edad"'
        return t

    def t_CARGO(self, t):
        r'"cargo"'
        return t

    def t_FOTO(self, t):
        r'"foto"'
        return t

    def t_EMAIL(self, t):
        r'"email"'
        return t

    def t_DIREMAIL(self, t):
        r'"[a-z0-9!#$%&\'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&\'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?"'
        return t

    def t_HABILIDADES(self, t):
        r'"habilidades"'
        return t

    def t_SALARIO(self, t):
        r'"salario"'
        return t

    def t_ACTIVO(self, t):
        r'"activo"'
        return t

    def t_PROYECTOS(self, t):
        r'"proyectos"'
        return t

    def t_P_ESTADO(self, t):
        r'"estado"'
        t.value = t.value[1:-1]
        return t

    def t_P_PROGRESO(self, t):
        r'"(To\sDo|In\sProgress|Cancelled|Done|On\sHold)"'
        t.value = t.value[1:-1]
        return t

    def t_P_RESUMEN(self, t):
        r'"resumen"'
        return t

    def t_FECHA_INI(self, t):
        r'"fecha_inicio"'
        t.value = t.value[1:-1]
        return t

    def t_FECHA_FIN(self, t):
        r'"fecha_fin"'
        t.value = t.value[1:-1]
        return t

    def t_TAREAS(self, t):
        r'"tareas"'
        return t

    def t_P_VIDEO(self, t):
        r'"video"'
        return t

    def t_P_CONCLUSION(self, t):
        r'"conclusión"'
        return t

    def t_VERSION(self, t):
        r'"versión"'
        return t

    def t_FIRMA(self, t):
        r'"firma_digital"'
        return t

    def t_ROL(self, t):
        r'"(Product\sAnalyst|Project\sManager|UX\sDesigner|Marketing|Developer|Devops|DB\sAdmin)"'
        return t

    def t_DATE(self, t):
        r'"(19[0-9][0-9]|20[0-9][0-9])\-(0?[1-9]|1[012])\-([12][0-9]|3[01]|0?[1-9])"'
        t.value = t.value[1:-1]
        return t

    def t_URL(self, t):
        r'"https?://[^\s"]+"'
        return t

    def t_BOOL(self, t):
        r'(true|false)'
        return t

    def t_STRING(self, t):
        r'"(?:[^"\\]|\\.)*"'
        t.value = bytes(t.value[1:-1], "utf-8").decode("unicode_escape")
        return t

    def t_error(self, t):
        self.errores += 1
        error_msg = f"Caracter ilegal: '{t.value}'(Código: {ord(t.value[0])})"
        print(error_msg)
        t.lexer.skip(1)

    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)

    def analyze_symbol(self, symbol):
        """
        Analiza un símbolo individual y devuelve su token
        """
        self.errores = 0
        self.tokens_identificados = []
        
        try:
            self.lexer.input(symbol)
            token_found = None
            
            for tok in self.lexer:
                if tok is not None:
                    token_found = tok
                    self.tokens_identificados.append(f"{tok.type}: {tok.value}")
            
            if token_found:
                return {
                    'token': token_found.type,
                    'value': token_found.value,
                    'success': True,
                    'errors': self.errores
                }
            else:
                return {
                    'token': 'NO_TOKEN_FOUND',
                    'value': symbol,
                    'success': False,
                    'errors': self.errores
                }
                
        except Exception as e:
            return {
                'token': 'ERROR',
                'value': symbol,
                'success': False,
                'errors': self.errores + 1,
                'error_message': str(e)
            }

    def analyze_text(self, text):
        """
        Analiza un texto completo y devuelve todos los tokens encontrados
        """
        self.errores = 0
        self.tokens_identificados = []
        found_tokens = []
        
        try:
            self.lexer.input(text)
            
            for tok in self.lexer:
                if tok is not None:
                    token_info = {
                        'type': tok.type,
                        'value': tok.value,
                        'line': tok.lineno,
                        'position': tok.lexpos
                    }
                    found_tokens.append(token_info)
                    self.tokens_identificados.append(f"{tok.type}: {tok.value}")
            
            return {
                'tokens': found_tokens,
                'total_tokens': len(found_tokens),
                'errors': self.errores,
                'success': self.errores == 0,
                'tokens_list': self.tokens_identificados
            }
            
        except Exception as e:
            return {
                'tokens': [],
                'total_tokens': 0,
                'errors': self.errores + 1,
                'success': False,
                'error_message': str(e)
            }

    def analyze_json_file(self, json_content):
        """
        Analiza un archivo JSON (ya parseado) y devuelve los tokens
        """
        try:
            # Convertir el JSON a texto formateado
            text = json.dumps(json_content, indent=2, ensure_ascii=False)
            
            # Analizar el texto
            result = self.analyze_text(text)
            
            # Agregar información específica del JSON
            result['json_info'] = {
                'is_valid_json': True,
                'json_type': type(json_content).__name__,
                'json_size': len(text)
            }
            
            return result
            
        except Exception as e:
            return {
                'tokens': [],
                'total_tokens': 0,
                'errors': 1,
                'success': False,
                'error_message': f"Error procesando JSON: {str(e)}",
                'json_info': {
                    'is_valid_json': False,
                    'json_type': 'unknown',
                    'json_size': 0
                }
            }

    def get_token_info(self, symbol):
        """
        Método simplificado para obtener solo el tipo de token
        """
        result = self.analyze_symbol(symbol)
        return result.get('token', 'UNKNOWN')

    def reset(self):
        """
        Reinicia el estado del lexer
        """
        self.errores = 0
        self.tokens_identificados = []
        self.lexer.lineno = 1

# Función para mantener compatibilidad con el código original
def create_lexer():
    """
    Crea una instancia del lexer
    """
    return LexerAnalyzer()

# Para uso directo del módulo (opcional)
if __name__ == "__main__":
    # Código original del menú (comentado para uso con Flask)
    """
    # Tu código original del menú aquí si quieres mantenerlo
    lexer_analyzer = LexerAnalyzer()
    
    # Ejemplo de uso:
    result = lexer_analyzer.analyze_symbol('"equipos"')
    print(f"Token: {result['token']}")
    """
    print("Lexer adaptado para Flask. Importa la clase LexerAnalyzer para usarla.")