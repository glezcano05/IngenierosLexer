from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import json
import os
from werkzeug.utils import secure_filename

# Importa tu lexer adaptado
from lexer import LexerAnalyzer

app = Flask(__name__)
CORS(app)  # Para permitir requests desde el frontend

# Configuración para subida de archivos
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'json'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB máximo

# Crear carpeta de uploads si no existe
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Instancia de tu lexer
lexer_analyzer = LexerAnalyzer()

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    """Servir la página principal"""
    return render_template('index.html')

@app.route('/api/analyze', methods=['POST'])
def analyze_symbol():
    """Analizar un símbolo individual"""
    try:
        data = request.get_json()
        symbol = data.get('symbol', '').strip()
        
        if not symbol:
            return jsonify({
                'success': False,
                'error': 'El símbolo no puede estar vacío'
            }), 400
        
        # Usar tu lexer real
        result = lexer_analyzer.analyze_symbol(symbol)
        
        if result['success']:
            return jsonify({
                'success': True,
                'symbol': symbol,
                'token': result['token'],
                'value': result['value'],
                'errors': result['errors'],
                'message': f'Símbolo "{symbol}" analizado correctamente'
            })
        else:
            return jsonify({
                'success': False,
                'symbol': symbol,
                'token': result.get('token', 'UNKNOWN'),
                'errors': result['errors'],
                'error': result.get('error_message', 'No se pudo identificar el token')
            })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Error al analizar el símbolo: {str(e)}'
        }), 500

@app.route('/api/process-file', methods=['POST'])
def process_file():
    """Procesar archivo JSON"""
    try:
        # Verificar si se envió un archivo
        if 'file' not in request.files:
            return jsonify({
                'success': False,
                'error': 'No se encontró ningún archivo'
            }), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({
                'success': False,
                'error': 'No se seleccionó ningún archivo'
            }), 400
        
        if file and allowed_file(file.filename):
            # Guardar archivo de forma segura
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            # Leer y procesar el archivo JSON
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    json_content = json.load(f)
                
                # Usar tu lexer real para procesar el JSON
                result = lexer_analyzer.analyze_json_file(json_content)
                
                # Limpiar archivo temporal
                os.remove(filepath)
                
                if result['success']:
                    return jsonify({
                        'success': True,
                        'filename': filename,
                        'result': {
                            'tokens_found': result['total_tokens'],
                            'errors_found': result['errors'],
                            'file_size': result['json_info']['json_size'],
                            'structure_type': result['json_info']['json_type'],
                            'is_valid_json': result['json_info']['is_valid_json'],
                            'message': f'Archivo {filename} procesado exitosamente',
                            'tokens_detail': result['tokens'][:10]  # Primeros 10 tokens como ejemplo
                        }
                    })
                else:
                    return jsonify({
                        'success': False,
                        'error': result.get('error_message', 'Error procesando el archivo'),
                        'errors_found': result['errors']
                    }), 400
                
            except json.JSONDecodeError:
                return jsonify({
                    'success': False,
                    'error': 'El archivo no es un JSON válido'
                }), 400
                
        else:
            return jsonify({
                'success': False,
                'error': 'Tipo de archivo no permitido. Solo se permiten archivos .json'
            }), 400
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Error al procesar el archivo: {str(e)}'
        }), 500

# Función para agregar más información sobre los tokens (opcional)
@app.route('/api/analyze-text', methods=['POST'])
def analyze_text():
    """Analizar texto completo (endpoint adicional)"""
    try:
        data = request.get_json()
        text = data.get('text', '').strip()
        
        if not text:
            return jsonify({
                'success': False,
                'error': 'El texto no puede estar vacío'
            }), 400
        
        result = lexer_analyzer.analyze_text(text)
        
        return jsonify({
            'success': result['success'],
            'tokens': result['tokens'],
            'total_tokens': result['total_tokens'],
            'errors': result['errors'],
            'tokens_list': result['tokens_list']
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Error al analizar el texto: {str(e)}'
        }), 500

if __name__ == '__main__':
    print("🚀 Iniciando servidor del Lexer...")
    print("📱 Interfaz web disponible en: http://localhost:5000")
    print("🔧 API endpoints:")
    print("   - POST /api/analyze (análisis de símbolos)")
    print("   - POST /api/process-file (procesamiento de archivos)")
    app.run(debug=True, host='0.0.0.0', port=5000)