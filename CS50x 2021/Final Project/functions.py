from cs50 import SQL

# Calling the database to set the query

db = SQL("sqlite:///problem.db")

# Set function rules


def get_coms_count(problem):
    coms = db.execute("SELECT COUNT(*) AS com_count FROM comments WHERE post_id=:post_id", post_id=problem["id"])
    problem["comments"] = coms[0]['com_count']


# Adjust the number of pages based on the number of problems

def get_pages_count(problems_count):
    if problems_count > 10:
        if problems_count % 10 == 0:
            count = int(problems_count / 10)
        else:
            count = int(problems_count // 10 + 1)
    else:
        count = 1
    return count