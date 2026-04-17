from db import get_users_connection, hash_password
from flask import request, redirect, render_template, session, flash
from server import app
from urllib.parse import urlparse #urlparse para analizar URLs 


#Función para validar que la URL de redirección es segura, solo permitiendo rutas internar e.g '/dashboard'
def is_safe_redirect(target):
    parsed = urlparse(target) #parsear la url, separar esquema, dominio, ruta, etc..
    return not parsed.netloc and target.startswith('/') #parsed.netloc vacío significa que NO hay dominio, y con target.startswith('/') garantiza que la ruta comienza en la raíz del sitio.  Si ambas condiciones se cumplen, la redirección es segura.

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'username' in session:
        return redirect('/dashboard')
    next_url = request.args.get('next', '/dashboard')
    if not is_safe_redirect(next_url): #si la URL no es segura (contiene un dominio externo), se forza la redireccion a ruta interna
        next_url = '/dashboard'

    if request.method == 'POST':
        username = request.form.get('username').strip() #get() para obtener el valor de username desde el formulario evitando errores si no se envia, y strip() elimina espacios en blanco al inicio y al final
        password = request.form.get('password','') #get() para obtener el valor de password desde el formulario evitamdo errores si no se envia
        if  not username or not password: #validamos que ambos campos sean obligatorios
            flash("Username and password are required.","danger") #mostrar mensaje indicando la ausencia de un campo
            return render_template('auth/login.html', next_url=next_url) #se renderiza el login manteniendo redireccion segura
        
        conn = get_users_connection()
        #user = conn.execute("SELECT * FROM users WHERE username = '"+ username +"' AND password = '"+hash_password(password)+"'").fetchone()
        """Se modifica para realizar consulta parametrizada.
        Mitigacion: 3.1 Injection en el proceso de login y 3.3 3.3	Ausencia de validación de campos y sanitización
        """
        user = conn.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, hash_password(password))).fetchone()
        conn.close()
        
        if user:
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['role'] = user['role']
            session['company_id'] = user['company_id']
            session.permanent = True
            return redirect(next_url)
        else:
            flash("Invalid username or password", "danger")
            return render_template('auth/login.html', next_url=next_url)
    return render_template('auth/login.html', next_url=next_url)


@app.route('/logout')
def logout():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect('/login')
