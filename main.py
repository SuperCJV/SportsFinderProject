from website import create_app

#create the application
app = create_app()

if __name__ == '__main__':
    app.run(debug=True)