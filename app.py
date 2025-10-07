import streamlit as st
import time
import hashlib
import json

# Blockchain class (same logic as yours)
class Blockchain:
    def __init__(self):
        self.chain = []
        self.current_transactions = []
        # genesis block
        self.create_block(proof=100, previous_hash='1')

    def create_block(self, proof, previous_hash):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time.time(),
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash
        }
        # reset transactions
        self.current_transactions = []
        self.chain.append(block)
        return block

    def add_transaction(self, name, student_id, department):
        self.current_transactions.append({
            'name': name,
            'student_id': student_id,
            'department': department
        })
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

# Instantiate blockchain
blockchain = Blockchain()

def main():
    st.title("Student Blockchain (Streamlit)")

    st.subheader("Add a Student Record / Transaction")
    name = st.text_input("Student Name")
    student_id = st.text_input("Student ID")
    department = st.text_input("Department")

    if st.button("Add & Mine Block"):
        if name.strip() == "" or student_id.strip() == "" or department.strip() == "":
            st.error("Please fill in all fields")
        else:
            blockchain.add_transaction(name, student_id, department)
            last_proof = blockchain.last_block['proof']
            proof = blockchain.proof_of_work(last_proof)
            prev_hash = blockchain.hash(blockchain.last_block)
            blockchain.create_block(proof, prev_hash)
            st.success(f"Block mined! Transaction added in block #{blockchain.last_block['index']}")

    st.markdown("---")
    st.header("Blockchain")
    for block in blockchain.chain:
        st.json(block)

if __name__ == "__main__":
    main()
