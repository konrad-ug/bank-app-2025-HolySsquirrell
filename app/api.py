from flask import Flask, request, jsonify
from src.accountPersonal import AccountPersonal
from src.accountRegistry import AccountRegistry

app = Flask(__name__)
registry = AccountRegistry()

@app.route("/api/accounts", methods=['POST'])
def create_account():
    data = request.get_json()
    pesel = str(data["pesel"])
    
    if registry.search_account(pesel):
        return jsonify({"error": "Account with this PESEL already exists"}), 409

    account = AccountPersonal( data["name"], data["surname"], pesel)
    
    registry.add_account(account)
    return jsonify({"message": "Account created"}), 201

@app.route("/api/accounts", methods=['GET'])
def get_all_accounts():
    print("Get all accounts request received")
    accounts = registry.return_all_accs()
    accounts_data = [{"name": acc.first_name,"surname": acc.last_name,"pesel": acc.pesel, "balance":acc.balance} for acc in accounts]
    return jsonify(accounts_data), 200

@app.route("/api/accounts/count", methods=['GET'])
def get_account_count():
    print("Get count request received")
    accounts = registry.return_all_accs()
    count = len(accounts)
    return jsonify({"count": count}), 200

@app.route("/api/accounts/<pesel>", methods=['GET'])
def get_account_by_pesel(pesel):
    account = registry.search_account(pesel)

    if not account:
        return jsonify({"error": "Account not found"}), 404

    return jsonify({
        "name": account.first_name,
        "surname": account.last_name,
        "pesel": account.pesel,
        "balance": account.balance
    }), 200

@app.route("/api/accounts/<pesel>", methods=['PATCH'])
@app.route("/api/accounts/<pesel>", methods=['PATCH'])
def update_account(pesel):
    data = request.get_json()
    account = registry.search_account(pesel)

    if not account:
        return jsonify({"error": "Account not found"}), 404

    if "name" in data:
        account.first_name = data["name"]

    if "surname" in data:
        account.last_name = data["surname"]

    if "balance" in data:  
        account.balance = float(data["balance"])

    return jsonify({"message": "Account updated"}), 200


@app.route("/api/accounts/<pesel>", methods=['DELETE'])
def delete_account(pesel):
    account = registry.search_account(pesel)

    if not account:
        return jsonify({"error": "Account not found"}), 404

    registry.accounts.remove(account)
    return jsonify({"message": "Account deleted"}), 200

@app.route("/api/accounts/<pesel>/transfer", methods=['POST'])
def transfer(pesel):
    data = request.get_json()
    amount = data.get("amount")
    transfer_type = data.get("type")

    account = registry.search_account(pesel)
    if not account:
        return jsonify({"error": "Account not found"}), 404

    if transfer_type not in ["incoming", "outgoing", "express"]:
        return jsonify({"error": "Unknown transfer type"}), 400

    if transfer_type == "incoming":
        account.balance += amount
        account.history.append(amount)
        return jsonify({"message": "Zlecenie przyjęto do realizacji"}), 200
    
    elif transfer_type == "outgoing":
        if account.balance >= amount:
            account.balance -= amount
            account.history.append(-amount)
            return jsonify({"message": "Zlecenie przyjęto do realizacji"}), 200
        else:
            return jsonify({"error": "Insufficient funds"}), 422
    elif transfer_type == "express":
        account.balance += amount
        account.history.append(amount)
        return jsonify({"message": "Zlecenie przyjęto do realizacji"}), 200

@app.route("/api/transfers", methods=["POST"])
def transfer_between_accounts():
    data = request.get_json()

    sender_pesel = data["from"]
    receiver_pesel = data["to"]
    amount = float(data["amount"])

    sender = registry.search_account(sender_pesel)
    receiver = registry.search_account(receiver_pesel)

    if not sender or not receiver:
        return jsonify({"error": "Account not found"}), 404

    if sender.balance < amount:
        return jsonify({"error": "Insufficient funds"}), 400

    sender.balance -= amount
    receiver.balance += amount

    sender.history.append(-amount)
    receiver.history.append(amount)

    return jsonify({"message": "Transfer completed"}), 200


if __name__ == "__main__":
    app.run(debug=True)


