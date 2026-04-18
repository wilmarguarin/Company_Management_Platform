from flask import request, redirect, render_template, session, flash
from server import app
from db import get_data_connection

@app.route('/admin/companies')
def admin_list_companies():
    if session.get('role') != 'admin':
        return render_template('errors/403.html'), 403

    conn = get_data_connection()
    companies = conn.execute("SELECT * FROM companies").fetchall()
    conn.close()
    return render_template('admin/admin_companies.html', companies=companies)

@app.route('/admin/companies/add', methods=['GET', 'POST'])
def admin_add_company():
    if session.get('role') != 'admin':
        return render_template('errors/403.html'), 403

    if request.method == 'POST':
        company_name = request.form.get('company_name', '').strip()
        description = request.form.get('description', '').strip()
        owner = request.form.get('owner', '').strip()

        if not company_name or not description or not owner:
            flash("All fields are required.", "danger")
            return redirect('/admin/companies')

        conn = get_data_connection()
        conn.execute(
            "INSERT INTO companies (name, description, owner) VALUES (?, ?, ?)",
            (company_name, description, owner)
        )
        conn.commit()
        conn.close()

        flash("Company created successfully.", "success")
        return redirect('/admin/companies')

    return render_template('admin/admin_companies.html')

@app.route('/admin/companies/delete', methods=['POST'])
def delete_company():
    if session.get('role') != 'admin':
        return render_template('errors/403.html'), 403

    company = request.form.get('company', '').strip()

    try:
        company_id = int(company)
        if company_id <= 0:
            raise ValueError()
    except ValueError:
        flash("Invalid company identifier.", "danger")
        return redirect('/admin/companies')

    conn = get_data_connection()
    conn.execute("DELETE FROM comments WHERE company_id = ?", (company_id,))
    conn.execute("DELETE FROM companies WHERE id = ?", (company_id,))
    conn.commit()
    conn.close()

    flash("Company deleted.", "warning")
    return redirect('/admin/companies')