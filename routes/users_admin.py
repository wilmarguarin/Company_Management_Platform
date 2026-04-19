from flask import request, redirect, render_template, session, flash
from server import app
from db import get_users_connection, get_data_connection, hash_password

def current_user_is_admin():
    username = session.get('username')
    if not username:
        return False

    conn = get_users_connection()
    user = conn.execute(
        "SELECT role FROM users WHERE username = ?",
        (username,)
    ).fetchone()
    conn.close()

    return user is not None and user['role'] == 'admin'

@app.route('/admin/users')
def admin_users():
    if not current_user_is_admin():
        return render_template('errors/403.html'), 403
    conn_u = get_users_connection()
    users = conn_u.execute("SELECT * FROM users").fetchall()
    conn_u.close()

    conn_d = get_data_connection()
    companies = conn_d.execute("SELECT * FROM companies").fetchall()
    conn_d.close()

    return render_template('admin/admin_users.html', users=users, companies=companies)


@app.route('/admin/users/add', methods=['POST'])
def add_user():
    if not current_user_is_admin():
        return render_template('errors/403.html'), 403
    username = request.form.get('username', '').strip()
    password = request.form.get('password', '').strip()
    role = request.form.get('role', '').strip()
    company_id = request.form.get('company_id', '').strip() if role == 'owner' else None
    if not username or not password or not role:
        flash("Username, password and role are required.", "danger")
        return redirect('/admin/users')
    allowed_roles = {'admin', 'user', 'owner'}
    if role not in allowed_roles:
        flash("Invalid role selected", "danger")
        return redirect('/admin/users')
    if role == 'owner':
        if not company_id or not company_id.isdigit():
            flash("A valid company identifier is required for owner role.", "danger")
            return redirect('/admin/users')
        company_id = int(company_id)
        conn_d = get_data_connection()
        company_exists = conn_d.execute(
            "SELECT id FROM companies WHERE id = ?",
            (company_id,)
        ).fetchone()
        conn_d.close()
        if not company_exists:
            flash("Selected company does not exist.", "danger")
            return redirect('/admin/users')
    conn = get_users_connection()
    if company_id is not None:
        conn.execute(
            "INSERT INTO users (username, password, role, company_id) VALUES (?, ?, ?, ?)",
            (username, hash_password(password), role, company_id)
        )
    else:
        conn.execute(
            "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
            (username, hash_password(password), role))
    conn.commit()
    conn.close()
    flash("User created successfully.", "success")
    return redirect('/admin/users')

@app.route('/admin/users/edit', methods=['POST'])
def edit_user():
    if not current_user_is_admin():
        return render_template('errors/403.html'), 403
    username = request.form.get('username', '').strip()
    new_role = request.form.get('role', '').strip()
    company_id = request.form.get('company_id', '').strip() if new_role == 'owner' else None
    allowed_roles = {'admin', 'user', 'owner'}
    if not username or not new_role:
        flash("Username and role are required.", "danger")
        return redirect('/admin/users')
    if new_role not in allowed_roles:
        flash("Invalid role selected.", "danger")
        return redirect('/admin/users')
    conn = get_users_connection()
    existing_user = conn.execute(
        "SELECT username FROM users WHERE username = ?", (username,)).fetchone()
    if not existing_user:
        conn.close()
        flash("User not found.", "danger")
        return redirect('/admin/users')
    if new_role == 'owner':
        if not company_id or not company_id.isdigit():
            conn.close()
            flash("A valid company identifier is required for owner role.", "danger")
            return redirect('/admin/users')
        company_id = int(company_id)
        conn_d = get_data_connection()
        company_exists = conn_d.execute("SELECT id FROM companies WHERE id = ?",(company_id,)).fetchone()
        conn_d.close()
        if not company_exists:
            conn.close()
            flash("Selected company does not exist.", "danger")
            return redirect('/admin/users')

        conn.execute(
            "UPDATE users SET role = ?, company_id = ? WHERE username = ?",(new_role, company_id, username))
    else:
        conn.execute(
            "UPDATE users SET role = ?, company_id = NULL WHERE username = ?",(new_role, username))

    conn.commit()
    conn.close()
    flash("User updated.", "success")
    return redirect('/admin/users')


@app.route('/admin/users/delete', methods=['POST'])
def delete_user():
    if not current_user_is_admin():
        return render_template('errors/403.html'), 403
    username = request.form.get('username', '').strip()
    if not username:
        flash("Username is required.", "danger")
        return redirect('/admin/users')
    conn = get_users_connection()
    existing_user = conn.execute("SELECT username FROM users WHERE username = ?", (username,)).fetchone()
    if not existing_user:
        conn.close()
        flash("User not found.", "danger")
        return redirect('/admin/users')
    conn.execute(
        "DELETE FROM users WHERE username = ?",(username,))
    conn.commit()
    conn.close()
    flash("User deleted.", "warning")
    return redirect('/admin/users')