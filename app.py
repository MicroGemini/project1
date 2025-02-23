from flask import Flask, render_template_string

# Initialize the Flask app
app = Flask(__name__)

# Define a simple route
@app.route("/")
def hello_world():
    return render_template_string("""
        <h1>Hello, World App</h1>
        <p>Welcome to your first Flask app! 🎉</p>
        <form action="/greet" method="post">
            <button type="submit">Say Hello</button>
        </form>
    """)

# Define a route for greeting
@app.route("/greet", methods=["POST"])
def greet():
    return render_template_string("""
        <h1>Hello, World! 👋</h1>
        <p>You've just triggered a greeting from Flask!</p>
        <a href="/">Go Back</a>
    """)

# Run the app
if __name__ == "__main__":
    app.run(debug=True)
