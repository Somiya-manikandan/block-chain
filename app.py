from flask import Flask, request, render_template_string
import time
import hashlib
import json

app = Flask(__name__)   # __name__, not _name_

# -------------------------
# Blockchain Class
# -------------------------
class Blockchain:
    def __init__(self):   # double underscores
        self.chain = []
        self.current_transactions = []
        # create the genesis block
        self.create_block(proof=100, previous_hash='1')

    def create_block(self, proof, previous_hash):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time.time(),
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash
        }
        # reset current transactions
        self.current_transactions = []
        self.chain.append(block)
        return block

    def add_transaction(self, name, student_id, department):
        self.current_transactions.append({
            'name': name,
            'student_id': student_id,
            'department': department
        })
        # return index of the block where it will be added
        return self.last_block['index'] + 1

    @staticmethod
    def hash(block):
        encoded = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(encoded).hexdigest()

    @property
    def last_block(self):
        return self.chain[-1]

    def proof_of_work(self, last_proof):
        proof = 0
        while not self.valid_proof(last_proof, proof):
            proof += 1
        return proof

    @staticmethod
    def valid_proof(last_proof, proof):
        guess = f"{last_proof}{proof}".encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"


# Initialize the blockchain
blockchain = Blockchain()

# -------------------------
# HTML Template (inline)
# -------------------------
template = '''
<!DOCTYPE html>
<html>
<head>
    <title>Student Blockchain</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 40px;
            background: #f4f4f4;
        }
        h1, h2 {
            color: #333;
        }
        form {
            background: white;
            padding: 20px;
            max-width: 400px;
            margin-bottom: 30px;
            border-radius: 8px;
        }
        input, button {
            padding: 10px;
            margin: 5px 0;
            width: 100%;
            box-sizing: border-box;
        }
        button {
            background: #4CAF50;
            color: white;
            border: none;
        }
        .block {
            background: white;
            padding: 15px;
            margin-bottom: 15px;
            border-left: 5px solid #4CAF50;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            max-width: 800px;
        }
        pre {
            white-space: pre-wrap;
            word-wrap: break-word;
        }
    </style>
</head>
<body>

    <h1>Student Blockchain</h1>

    <form action="/add_transaction" method="post">
        <input type="text" name="name" placeholder="Student Name" required>
        <input type="text" name="student_id" placeholder="Student ID" required>
        <input type="text" name="department" placeholder="Department" required>
        <button type="submit">Add Student</button>
    </form>

    <h2>Blockchain</h2>
    {% for block in chain %}
        <div class="block">
            <pre>{{ block | tojson(indent=2) }}</pre>
        </div>
    {% endfor %}

</body>
</html>
'''

# -------------------------
# Flask Routes
# -------------------------

@app.route('/')
def index():
    return render_template_string(template, chain=blockchain.chain)

@app.route('/add_transaction', methods=['POST'])
def add_transaction():
    name = request.form['name']
    student_id = request.form['student_id']
    department = request.form['department']

    blockchain.add_transaction(name, student_id, department)

    # Mine one block
    last_proof = blockchain.last_block['proof']
    proof = blockchain.proof_of_work(last_proof)
    previous_hash = blockchain.hash(blockchain.last_block)
    blockchain.create_block(proof, previous_hash)

    return render_template_string(template, chain=blockchain.chain)

# -------------------------
# Run the App
# -------------------------
if __name__ == "__main__":
    app.run(debug=True)
