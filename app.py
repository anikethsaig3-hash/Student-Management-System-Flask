from app import create_app

# Create the WSGI application object for servers that expect 'app'
app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
