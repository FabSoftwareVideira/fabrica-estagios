from app import app, db
from app.models import Role, User
from app.seed import seed_command

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Role': Role}


app.cli.add_command(seed_command)

if __name__ == '__main__':
    app.run(debug=False)