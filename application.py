from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)


def init_db():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS reviews (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            rating INTEGER,
            comment TEXT
        )
    """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS earnings_table (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            earnings REAL,
            month TEXT
        )
    """
    )

    # Insert some sample earnings data for testing
    cursor.execute(
        "INSERT INTO earnings_table (earnings, month) VALUES (1000.0, 'January')"
    )
    cursor.execute(
        "INSERT INTO earnings_table (earnings, month) VALUES (1500.0, 'February')"
    )

    conn.commit()
    conn.close()


init_db()


def calculate_earnings_statistics():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT SUM(earnings) FROM earnings_table")
    total_earnings = cursor.fetchone()[0]

    cursor.execute("SELECT AVG(earnings) FROM earnings_table")
    average_earnings = cursor.fetchone()[0]

    conn.close()
    return total_earnings, average_earnings


@app.route("/")
def index():
    total_earnings, average_earnings = calculate_earnings_statistics()
    return render_template(
        "index.html", total_earnings=total_earnings, average_earnings=average_earnings
    )


@app.route("/reviews")
def reviews():
    # Display reviews here (you can fetch data from the database)
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM reviews")
    reviews = cursor.fetchall()
    conn.close()
    return render_template("reviews.html", reviews=reviews)


@app.route("/add_review", methods=["POST"])
def add_review():
    if request.method == "POST":
        name = request.form["name"]
        rating = request.form["rating"]
        comment = request.form["comment"]

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO reviews (name, rating, comment) VALUES (?, ?, ?)",
            (name, rating, comment),
        )
        conn.commit()
        conn.close()

    return redirect(url_for("reviews"))


# Delete a review
@app.route("/delete_review/<int:review_id>", methods=["POST"])
def delete_review(review_id):
    if request.method == "POST":
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM reviews WHERE id = ?", (review_id,))
        conn.commit()
        conn.close()

    return redirect(url_for("reviews"))


if __name__ == "__main__":
    app.run(debug=True)
