from typing import Dict, List
import main


if __name__ == "__main__":
    config = main.load_config()
    blockchain = main.load_chain(config["blockchain_file"])
    transactions: List[Dict] = []

    main.start_server(
        config["host"],
        config["port"],
        blockchain,
        config["difficulty"],
        transactions,
        config["blockchain_file"],
    )

    # create a transaction
    print("[TEST] Make transaction")
    main.make_transaction(
        "george_linux",
        "george_windows",
        10,
        transactions,
        config["peers_file"],
        config["port"],
    )

    print("[TEST] Mine block")
    main.mine_block(
        transactions,
        blockchain,
        config["node_id"],
        config["reward"],
        config["difficulty"],
        config["blockchain_file"],
        config["peers_file"],
        config["port"],
    )
