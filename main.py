from pprint import pp
import hashlib, json, socket, threading, time, os
from datetime import datetime
from typing import Dict, List

from block import (
    Block,
    create_block,
    create_block_from_dict,
    create_genesis_block,
    hash_block,
)


def load_chain(fpath: str) -> List[Block]:
    """
    Verifica se existe blockchain local.
    Se existir, carrega arquivo.
    Se não existir, cria um bloco genesis.

    TODO: deveria solicitar blockchain dos demais pares da rede antes de criar um bloco genesis?
    """
    if os.path.exists(fpath):
        with open(fpath) as f:
            return json.load(f)
    return [create_genesis_block()]


def save_chain(fpath: str, chain: list[Block]):
    blockchain_serializable = []
    for b in chain:
        blockchain_serializable.append(b.as_dict())

    with open(fpath, "w") as f:
        json.dump(blockchain_serializable, f, indent=2)


def valid_chain(chain):
    for i in range(1, len(chain)):
        if chain[i]["prev_hash"] != chain[i - 1]["hash"]:
            return False
    return True


def list_peers(fpath: str):
    if not os.path.exists(fpath):
        print("[!] No peers file founded!")
        return []
    with open(fpath) as f:
        return [line.strip() for line in f if line.strip()]


def broadcast_block(block: Block, peers_fpath: str, port: int):
    print("Broadcasting transaction...")
    for peer in list_peers(peers_fpath):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((peer, port))
            s.send(json.dumps({"type": "block", "data": block.as_dict()}).encode())
            s.close()
        except Exception:
            pass


def handle_client(
    conn: socket.socket,
    addr: str,
    blockchain: List[Block],
    difficulty: int,
    transactions: List[Dict],
    blockchain_fpath: str,
):
    try:
        data = conn.recv(4096).decode()
        msg = json.loads(data)
        if msg["type"] == "block":
            block = create_block_from_dict(msg["data"])
            expected_hash = hash_block(block)
            if (
                block.prev_hash == blockchain[-1].hash
                and block.hash.startswith("0" * difficulty)
                and block.hash == expected_hash
            ):
                blockchain.append(block)
                save_chain(blockchain_fpath, blockchain)
                print(f"[✓] New valid block added from {addr}")
            else:
                print(f"[!] Invalid block received from {addr}")
        elif msg["type"] == "tx":
            tx = msg["data"]
            if tx not in transactions:
                transactions.append(tx)
                print(f"[+] Transaction received from {addr}")
    except:
        pass
    conn.close()


def start_server(
    host: str,
    port: int,
    blockchain: List[Block],
    difficulty: int,
    transactions: List[Dict],
    blockchain_fpath: str,
):
    def server_thread():
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((host, port))
        server.listen()
        print(f"[SERVER] Listening on {host}:{port}")
        while True:
            conn, addr = server.accept()
            threading.Thread(
                target=handle_client,
                args=(
                    conn,
                    addr,
                    blockchain,
                    difficulty,
                    transactions,
                    blockchain_fpath,
                ),
            ).start()

    threading.Thread(target=server_thread, daemon=True).start()


def mine_block(
    transactions: List,
    blockchain: List[Block],
    node_id: str,
    reward: int,
    difficulty: int,
    blockchain_fpath: str,
    peers_fpath: str,
    port: int,
):
    if not transactions:
        print("[!] No transactions to mine.")
        return

    new_block = create_block(
        transactions,
        blockchain[-1].hash,
        miner=node_id,
        index=len(blockchain),
        reward=reward,
        difficulty=difficulty,
    )
    blockchain.append(new_block)
    transactions.clear()
    save_chain(blockchain_fpath, blockchain)
    broadcast_block(new_block, peers_fpath, port)
    print(f"[✓] Block {new_block.index} mined and broadcasted.")


def print_chain(blockchain: List[Block]):
    for b in blockchain:
        print(f"Index: {b.index}, Hash: {b.hash[:10]}..., Tx: {len(b.transactions)}")


def broadcast_transaction(tx: Dict, peers_fpath: str, port: int):
    for peer in list_peers(peers_fpath):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(5)
            s.connect((peer, port))
            s.send(json.dumps({"type": "tx", "data": tx}).encode())
            s.close()
        except Exception as e:
            print(
                f"[BROADCAST_TX] Exception during comunication with {peer}. Exception: {e}"
            )


def get_balance(node_id: str, blockchain: List[Block]) -> float:
    balance = 0
    for block in blockchain:
        for tx in block.transactions:
            if tx["to"] == node_id:
                balance += float(tx["amount"])
            if tx["from"] == node_id:
                balance -= float(tx["amount"])
    return balance


def load_config(fpath: str = "configs/node_config.json") -> Dict:
    print("Loading config...")
    with open(fpath, "r") as f:
        data = json.load(f)
        print("Config loaded:")
        pp(data)
        return data


def make_transaction(sender, recipient, amount, transactions, peers_file, port):
    tx = {"from": sender, "to": recipient, "amount": amount}
    transactions.append(tx)
    broadcast_transaction(tx, peers_file, port)
    print("[+] Transaction added.")


if __name__ == "__main__":
    config = load_config()
    blockchain = load_chain(config["blockchain_file"])
    transactions: List[Dict] = []

    start_server(
        config["host"],
        config["port"],
        blockchain,
        config["difficulty"],
        transactions,
        config["blockchain_file"],
    )

    print("=== SimpleCoin CLI ===")
    while True:
        print("\n1. Add transaction")
        print("2. Mine block")
        print("3. View blockchain")
        print("4. Get balance")
        print("5. Exit")
        choice = input("> ").strip()

        if choice == "1":
            sender = input("Sender: ")
            recipient = input("Recipient: ")
            amount = input("Amount: ")
            make_transaction(
                sender,
                recipient,
                amount,
                transactions,
                config["peers_file"],
                config["port"],
            )

        elif choice == "2":
            mine_block(
                transactions,
                blockchain,
                config["node_id"],
                config["reward"],
                config["difficulty"],
                config["blockchain_file"],
                config["peers_file"],
                config["port"],
            )

        elif choice == "3":
            print_chain(blockchain)

        elif choice == "4":
            node_id = input("Node ID: ")
            balance = get_balance(node_id, blockchain)
            print(f"[i] The balance of {node_id} is {balance}.")

        else:
            print("[!] Invalid choice.")
