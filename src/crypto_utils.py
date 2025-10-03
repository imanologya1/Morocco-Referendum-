"""
Cryptographic utilities for secure voting (Pure Python implementation)
"""
import hashlib
import json
import base64
import secrets
from typing import Tuple, Dict, Any


class VoteCrypto:
    """Handles encryption and signing for votes using pure Python"""
    
    @staticmethod
    def generate_poll_keypair() -> Tuple[str, str]:
        """Generate a secret key pair for a poll (using secure random)"""
        # Generate a 256-bit secret key
        secret_key = secrets.token_hex(32)
        # Public key is derived hash
        public_key = hashlib.sha256(secret_key.encode()).hexdigest()
        return secret_key, public_key
    
    @staticmethod
    def encrypt_vote(vote_choice: str, public_key: str) -> str:
        """
        Encrypt a vote using XOR cipher with key derivation
        Note: This is a simplified encryption for deployment compatibility
        """
        # Derive encryption key from public key
        key_material = hashlib.sha256(public_key.encode()).digest()
        
        # Generate random salt
        salt = secrets.token_bytes(16)
        
        # Derive actual encryption key
        derived_key = hashlib.pbkdf2_hmac('sha256', key_material, salt, 100000)
        
        # XOR encryption
        vote_bytes = vote_choice.encode('utf-8')
        encrypted_bytes = bytes(a ^ b for a, b in zip(vote_bytes, (derived_key * (len(vote_bytes) // len(derived_key) + 1))[:len(vote_bytes)]))
        
        encrypted_data = {
            'salt': base64.b64encode(salt).decode('utf-8'),
            'ciphertext': base64.b64encode(encrypted_bytes).decode('utf-8'),
            'length': len(vote_bytes)
        }
        
        return json.dumps(encrypted_data)
    
    @staticmethod
    def decrypt_vote(encrypted_vote: str, private_key: str) -> str:
        """Decrypt a vote using the private key"""
        try:
            encrypted_data = json.loads(encrypted_vote)
            
            # Decode from base64
            salt = base64.b64decode(encrypted_data['salt'])
            ciphertext = base64.b64decode(encrypted_data['ciphertext'])
            length = encrypted_data['length']
            
            # Derive public key from private key
            public_key = hashlib.sha256(private_key.encode()).hexdigest()
            
            # Derive decryption key
            key_material = hashlib.sha256(public_key.encode()).digest()
            derived_key = hashlib.pbkdf2_hmac('sha256', key_material, salt, 100000)
            
            # XOR decryption
            decrypted_bytes = bytes(a ^ b for a, b in zip(ciphertext, (derived_key * (len(ciphertext) // len(derived_key) + 1))[:len(ciphertext)]))
            
            return decrypted_bytes[:length].decode('utf-8')
        except Exception as e:
            raise ValueError(f"Decryption failed: {str(e)}")
    
    @staticmethod
    def generate_voter_token(voter_identifier: str, poll_id: str) -> str:
        """Generate anonymous voter token (hash-based)"""
        combined = f"{voter_identifier}:{poll_id}".encode('utf-8')
        return hashlib.sha256(combined).hexdigest()
    
    @staticmethod
    def sign_vote(vote_data: Dict[str, Any], voter_token: str) -> str:
        """Create a signature for the vote"""
        # Use voter token as seed for deterministic signing
        vote_string = json.dumps(vote_data, sort_keys=True)
        combined = f"{vote_string}:{voter_token}".encode('utf-8')
        return hashlib.sha256(combined).hexdigest()
    
    @staticmethod
    def verify_vote_signature(vote_data: Dict[str, Any], voter_token: str, signature: str) -> bool:
        """Verify vote signature"""
        expected_signature = VoteCrypto.sign_vote(vote_data, voter_token)
        return expected_signature == signature
    
    @staticmethod
    def generate_receipt(vote_data: Dict[str, Any]) -> str:
        """Generate a verification receipt for the voter"""
        receipt_data = {
            'poll_id': vote_data.get('poll_id'),
            'timestamp': vote_data.get('timestamp'),
            'vote_hash': hashlib.sha256(
                json.dumps(vote_data, sort_keys=True).encode('utf-8')
            ).hexdigest()
        }
        return base64.b64encode(json.dumps(receipt_data).encode('utf-8')).decode('utf-8')
    
    @staticmethod
    def verify_receipt(receipt: str, blockchain_votes: list) -> bool:
        """Verify a receipt against blockchain"""
        try:
            receipt_data = json.loads(base64.b64decode(receipt).decode('utf-8'))
            vote_hash = receipt_data['vote_hash']
            
            # Check if vote exists in blockchain
            for vote in blockchain_votes:
                vote_check_hash = hashlib.sha256(
                    json.dumps(vote, sort_keys=True).encode('utf-8')
                ).hexdigest()
                if vote_check_hash == vote_hash:
                    return True
            return False
        except Exception:
            return False


class VoterRegistry:
    """Manages voter tokens to prevent double voting"""
    
    def __init__(self):
        self.used_tokens: Dict[str, set] = {}  # poll_id -> set of tokens
    
    def has_voted(self, poll_id: str, voter_token: str) -> bool:
        """Check if a voter has already voted"""
        if poll_id not in self.used_tokens:
            return False
        return voter_token in self.used_tokens[poll_id]
    
    def register_vote(self, poll_id: str, voter_token: str):
        """Register that a voter has voted"""
        if poll_id not in self.used_tokens:
            self.used_tokens[poll_id] = set()
        self.used_tokens[poll_id].add(voter_token)
    
    def get_vote_count(self, poll_id: str) -> int:
        """Get number of votes for a poll"""
        if poll_id not in self.used_tokens:
            return 0
        return len(self.used_tokens[poll_id])
    
    def clear_poll(self, poll_id: str):
        """Clear voter registry for a poll (after closing)"""
        if poll_id in self.used_tokens:
            del self.used_tokens[poll_id]
