from app import create_app

unify_app = create_app()

if __name__ == '__main__':
    unify_app.run(host='0.0.0.0', port=5000, debug=True)