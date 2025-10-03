"""
Blockchain implementation for secure voting system
"""
import hashlib
import json
import time
from typing import List, Dict, Any, Optional
from datetime import datetime


class Block:
    """Represents a single block in the blockchain"""
    
    def __init__(self, index: int, timestamp: float, votes: List[Dict], 
                 previous_hash: str, poll_id: str):
        self.index = index
        self.timestamp = timestamp
        self.votes = votes
        self.previous_hash = previous_hash
        self.poll_id = poll_id
        self.nonce = 0
        self.hash = self.calculate_hash()
    
    def calculate_hash(self) -> str:
        """Calculate SHA-256 hash of the block"""
        block_string = json.dumps({
            "index": self.index,
            "timestamp": self.timestamp,
            "votes": self.votes,
            "previous_hash": self.previous_hash,
            "poll_id": self.poll_id,
            "nonce": self.nonce
        }, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()
    
    def mine_block(self, difficulty: int = 2):
        """Simple proof-of-work mining"""
        target = "0" * difficulty
        while self.hash[:difficulty] != target:
            self.nonce += 1
            self.hash = self.calculate_hash()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert block to dictionary"""
        return {
            "index": self.index,
            "timestamp": self.timestamp,
            "votes": self.votes,
            "previous_hash": self.previous_hash,
            "poll_id": self.poll_id,
            "nonce": self.nonce,
            "hash": self.hash
        }
    
    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'Block':
        """Create block from dictionary"""
        block = Block(
            index=data["index"],
            timestamp=data["timestamp"],
            votes=data["votes"],
            previous_hash=data["previous_hash"],
            poll_id=data["poll_id"]
        )
        block.nonce = data["nonce"]
        block.hash = data["hash"]
        return block


class Blockchain:
    """Blockchain for storing encrypted votes"""
    
    def __init__(self, chain_file: str = "blockchain.json"):
        self.chain_file = chain_file
        self.chain: List[Block] = []
        self.pending_votes: Dict[str, List[Dict]] = {}  # poll_id -> votes
        self.difficulty = 2
        self.load_chain()
    
    def load_chain(self):
        """Load blockchain from file or create genesis block"""
        try:
            with open(self.chain_file, 'r') as f:
                data = json.load(f)
                self.chain = [Block.from_dict(block_data) for block_data in data]
        except (FileNotFoundError, json.JSONDecodeError):
            # Create genesis block
            genesis_block = Block(0, time.time(), [], "0", "genesis")
            genesis_block.mine_block(self.difficulty)
            self.chain = [genesis_block]
            self.save_chain()
    
    def save_chain(self):
        """Save blockchain to file"""
        with open(self.chain_file, 'w') as f:
            json.dump([block.to_dict() for block in self.chain], f, indent=2)
    
    def get_latest_block(self) -> Block:
        """Get the most recent block"""
        return self.chain[-1]
    
    def add_vote(self, poll_id: str, vote_data: Dict):
        """Add a vote to pending votes"""
        if poll_id not in self.pending_votes:
            self.pending_votes[poll_id] = []
        self.pending_votes[poll_id].append(vote_data)
    
    def mine_pending_votes(self, poll_id: str) -> Optional[Block]:
        """Mine pending votes into a new block"""
        if poll_id not in self.pending_votes or not self.pending_votes[poll_id]:
            return None
        
        new_block = Block(
            index=len(self.chain),
            timestamp=time.time(),
            votes=self.pending_votes[poll_id],
            previous_hash=self.get_latest_block().hash,
            poll_id=poll_id
        )
        new_block.mine_block(self.difficulty)
        self.chain.append(new_block)
        self.pending_votes[poll_id] = []
        self.save_chain()
        return new_block
    
    def get_votes_for_poll(self, poll_id: str) -> List[Dict]:
        """Get all votes for a specific poll"""
        votes = []
        for block in self.chain:
            if block.poll_id == poll_id:
                votes.extend(block.votes)
        return votes
    
    def is_chain_valid(self) -> bool:
        """Validate the entire blockchain"""
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]
            
            # Check hash integrity
            if current_block.hash != current_block.calculate_hash():
                return False
            
            # Check chain linkage
            if current_block.previous_hash != previous_block.hash:
                return False
            
            # Check proof-of-work
            if not current_block.hash.startswith("0" * self.difficulty):
                return False
        
        return True
    
    def get_block_by_hash(self, block_hash: str) -> Optional[Block]:
        """Find a block by its hash"""
        for block in self.chain:
            if block.hash == block_hash:
                return block
        return None
    
    def get_chain_stats(self) -> Dict[str, Any]:
        """Get blockchain statistics"""
        total_votes = sum(len(block.votes) for block in self.chain)
        polls = set(block.poll_id for block in self.chain if block.poll_id != "genesis")
        
        return {
            "total_blocks": len(self.chain),
            "total_votes": total_votes,
            "total_polls": len(polls),
            "is_valid": self.is_chain_valid(),
            "latest_block_hash": self.get_latest_block().hash,
            "chain_file": self.chain_file
        }
