from reporter_app import create_app, db, cli
from reporter_app.models import User

app, user_datastore = create_app()
cli.register(app, user_datastore)


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User}
