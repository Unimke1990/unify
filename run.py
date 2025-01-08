from app import create_app

unify_app = create_app()

if __name__ == '__main__':
    unify_app.run(host='127.0.0.1', port=5000, debug=True)