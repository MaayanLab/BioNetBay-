# benchmark.py

from flask_bcrypt import generate_password_hash

# Change the number of rounds (second argument) until it takes between
# 0.25 and 0.5 seconds to run.
generate_password_hash('password1', 12)
