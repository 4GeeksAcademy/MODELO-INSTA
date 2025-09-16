import os
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from models import db, User

def setup_admin(app):
    """
    Configura la interfaz de administración de Flask-Admin.
    """
    app.secret_key = os.environ.get('FLASK_APP_KEY', 'sample key')
    app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'

    admin = Admin(app, name='4Geeks Admin', template_mode='bootstrap3')

    # Agrega modelos al panel de administración
    admin.add_view(ModelView(User, db.session))

    # Para agregar más modelos, duplicar la línea anterior
    # admin.add_view(ModelView(YourModelName, db.session))
