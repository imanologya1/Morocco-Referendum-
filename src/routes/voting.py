"""
Voting API routes
"""
from flask import Blueprint, request, jsonify
from datetime import datetime
import time

from src.models.poll import Poll, PollStore
from src.blockchain import Blockchain
from src.crypto_utils import VoteCrypto, VoterRegistry

voting_bp = Blueprint('voting', __name__, url_prefix='/api')

# Initialize components
poll_store = PollStore('polls.json')
blockchain = Blockchain('blockchain.json')
voter_registry = VoterRegistry()
crypto = VoteCrypto()


@voting_bp.route('/polls', methods=['POST'])
def create_poll():
    """Create a new poll"""
    try:
        data = request.json
        
        # Validate input
        if not data.get('title') or not data.get('question'):
            return jsonify({'error': 'Title and question are required'}), 400
        
        options = data.get('options', [])
        if len(options) < 2 or len(options) > 10:
            return jsonify({'error': 'Must have 2-10 options'}), 400
        
        # Generate encryption keys for this poll
        private_key, public_key = crypto.generate_poll_keypair()
        
        # Create poll
        poll = Poll(
            title=data['title'],
            question=data['question'],
            options=options,
            creator=data.get('creator', 'anonymous'),
            duration_hours=data.get('duration_hours', 24),
            language=data.get('language', 'en'),
            public_key=public_key,
            private_key=private_key
        )
        
        poll_store.create_poll(poll)
        
        return jsonify({
            'success': True,
            'poll': poll.to_public_dict(),
            'poll_url': f'/poll/{poll.poll_id}'
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@voting_bp.route('/polls', methods=['GET'])
def get_polls():
    """Get all polls or active polls"""
    try:
        active_only = request.args.get('active', 'false').lower() == 'true'
        
        if active_only:
            polls = poll_store.get_active_polls()
        else:
            polls = poll_store.get_all_polls()
        
        return jsonify({
            'success': True,
            'polls': [poll.to_public_dict() for poll in polls]
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@voting_bp.route('/polls/<poll_id>', methods=['GET'])
def get_poll(poll_id):
    """Get a specific poll"""
    try:
        poll = poll_store.get_poll(poll_id)
        
        if not poll:
            return jsonify({'error': 'Poll not found'}), 404
        
        # Include results if poll is closed
        poll_data = poll.to_public_dict()
        if poll.status == 'closed' and poll.results:
            poll_data['results'] = poll.results
        
        # Add vote count
        poll_data['vote_count'] = voter_registry.get_vote_count(poll_id)
        
        return jsonify({
            'success': True,
            'poll': poll_data
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@voting_bp.route('/vote', methods=['POST'])
def submit_vote():
    """Submit a vote"""
    try:
        data = request.json
        
        poll_id = data.get('poll_id')
        voter_identifier = data.get('voter_identifier')  # email, phone, or unique ID
        vote_choice = data.get('vote_choice')
        
        if not all([poll_id, voter_identifier, vote_choice]):
            return jsonify({'error': 'Missing required fields'}), 400
        
        # Get poll
        poll = poll_store.get_poll(poll_id)
        if not poll:
            return jsonify({'error': 'Poll not found'}), 404
        
        # Check if poll is active
        if not poll.is_active():
            return jsonify({'error': 'Poll is closed'}), 400
        
        # Validate vote choice
        if vote_choice not in poll.options:
            return jsonify({'error': 'Invalid vote choice'}), 400
        
        # Generate voter token
        voter_token = crypto.generate_voter_token(voter_identifier, poll_id)
        
        # Check if already voted
        if voter_registry.has_voted(poll_id, voter_token):
            return jsonify({'error': 'You have already voted in this poll'}), 400
        
        # Encrypt vote
        encrypted_vote = crypto.encrypt_vote(vote_choice, poll.public_key)
        
        # Create vote data
        vote_data = {
            'poll_id': poll_id,
            'encrypted_vote': encrypted_vote,
            'timestamp': time.time(),
            'voter_token_hash': voter_token[:16]  # Partial hash for verification
        }
        
        # Sign vote
        signature = crypto.sign_vote(vote_data, voter_token)
        vote_data['signature'] = signature
        
        # Add to blockchain
        blockchain.add_vote(poll_id, vote_data)
        
        # Mine block every 10 votes or immediately for testing
        if len(blockchain.pending_votes.get(poll_id, [])) >= 10:
            blockchain.mine_pending_votes(poll_id)
        
        # Register voter
        voter_registry.register_vote(poll_id, voter_token)
        
        # Generate receipt
        receipt = crypto.generate_receipt(vote_data)
        
        return jsonify({
            'success': True,
            'message': 'Vote submitted successfully',
            'receipt': receipt,
            'vote_hash': vote_data['signature'][:16]
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@voting_bp.route('/polls/<poll_id>/close', methods=['POST'])
def close_poll(poll_id):
    """Close a poll and count votes"""
    try:
        poll = poll_store.get_poll(poll_id)
        
        if not poll:
            return jsonify({'error': 'Poll not found'}), 404
        
        if poll.status == 'closed':
            return jsonify({'error': 'Poll already closed'}), 400
        
        # Mine any pending votes
        if poll_id in blockchain.pending_votes and blockchain.pending_votes[poll_id]:
            blockchain.mine_pending_votes(poll_id)
        
        # Get all encrypted votes
        encrypted_votes = blockchain.get_votes_for_poll(poll_id)
        
        # Decrypt and count votes
        results = {option: 0 for option in poll.options}
        
        for vote_data in encrypted_votes:
            try:
                decrypted_vote = crypto.decrypt_vote(
                    vote_data['encrypted_vote'],
                    poll.private_key
                )
                if decrypted_vote in results:
                    results[decrypted_vote] += 1
            except Exception as e:
                print(f"Error decrypting vote: {e}")
                continue
        
        # Update poll
        poll.close()
        poll.set_results(results)
        poll_store.update_poll(poll)
        
        return jsonify({
            'success': True,
            'message': 'Poll closed successfully',
            'results': results,
            'total_votes': sum(results.values())
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@voting_bp.route('/verify', methods=['POST'])
def verify_receipt():
    """Verify a vote receipt"""
    try:
        data = request.json
        receipt = data.get('receipt')
        poll_id = data.get('poll_id')
        
        if not receipt or not poll_id:
            return jsonify({'error': 'Receipt and poll_id required'}), 400
        
        # Get votes from blockchain
        votes = blockchain.get_votes_for_poll(poll_id)
        
        # Verify receipt
        is_valid = crypto.verify_receipt(receipt, votes)
        
        return jsonify({
            'success': True,
            'valid': is_valid,
            'message': 'Vote verified on blockchain' if is_valid else 'Vote not found'
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@voting_bp.route('/blockchain/stats', methods=['GET'])
def blockchain_stats():
    """Get blockchain statistics"""
    try:
        stats = blockchain.get_chain_stats()
        return jsonify({
            'success': True,
            'stats': stats
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@voting_bp.route('/blockchain/blocks', methods=['GET'])
def get_blocks():
    """Get all blocks"""
    try:
        blocks = [block.to_dict() for block in blockchain.chain]
        return jsonify({
            'success': True,
            'blocks': blocks
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
