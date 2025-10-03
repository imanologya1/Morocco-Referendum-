# VoteChain Morocco - Secure Blockchain Voting System

A free, secure, and transparent blockchain-based voting platform designed for Moroccans to conduct referendums, elections, and polls with cryptographic guarantees.

## 🌟 Features

### Security & Privacy
- **RSA + AES Hybrid Encryption**: All votes are encrypted using industry-standard cryptography
- **Anonymous Voting**: Voter identities are hashed and cannot be traced back to individual votes
- **Blockchain Verification**: Every vote is recorded on an immutable blockchain
- **Digital Signatures**: Each vote is cryptographically signed to prevent tampering
- **One Person, One Vote**: Hash-based voter registry prevents double voting

### User Features
- **Create Polls**: Easy-to-use interface for creating referendums and polls
- **Multiple Options**: Support for 2-10 voting options per poll
- **Multilingual**: Support for Arabic, French, and English
- **Vote Receipts**: Cryptographic receipts allow voters to verify their votes on the blockchain
- **Real-time Stats**: Live blockchain statistics and vote counts
- **Responsive Design**: Works seamlessly on desktop and mobile devices

### Technical Features
- **Simplified Blockchain**: Lightweight blockchain implementation with proof-of-work
- **File-based Storage**: No complex database setup required
- **RESTful API**: Clean API for integration with other systems
- **Batch Mining**: Votes are batched and mined into blocks for efficiency

## 🏗️ Architecture

### Backend Stack
- **Python 3.11** - Core programming language
- **Flask** - Web framework
- **PyCryptodome** - RSA and AES encryption
- **Cryptography** - Additional cryptographic utilities

### Frontend Stack
- **React 18** - Modern UI framework
- **Vite** - Fast build tool
- **Tailwind CSS** - Utility-first styling
- **shadcn/ui** - High-quality UI components
- **Lucide Icons** - Beautiful icon set

### Cryptographic Implementation

#### Vote Encryption Process
1. **Key Generation**: Each poll generates a unique RSA-2048 key pair
2. **Hybrid Encryption**: 
   - Vote content encrypted with AES-256
   - AES key encrypted with RSA public key
3. **Blockchain Storage**: Encrypted vote stored on blockchain
4. **Decryption**: After poll closes, private key used to decrypt and count votes

#### Anonymous Authentication
1. **Voter Token**: SHA-256 hash of (voter_identifier + poll_id)
2. **Registry Check**: Token checked against voter registry
3. **Vote Signing**: Vote signed with token-based signature
4. **Registration**: Token registered to prevent double voting

#### Blockchain Structure
Each block contains:
- Block index and timestamp
- Previous block hash (SHA-256)
- Poll ID
- Array of encrypted votes
- Nonce (proof-of-work)
- Block hash

## 📦 Installation

### Prerequisites
- Python 3.11+
- pip3
- Virtual environment support

### Setup Instructions

1. **Clone or extract the project**
```bash
cd /home/ubuntu/voting_system
```

2. **Activate virtual environment**
```bash
source venv/bin/activate
```

3. **Install dependencies** (already installed)
```bash
pip install -r requirements.txt
```

4. **Run the application**
```bash
python src/main.py
```

5. **Access the application**
Open your browser to: `http://localhost:5000`

## 🚀 Usage Guide

### Creating a Poll

1. Navigate to the **Create Poll** tab
2. Fill in the poll details:
   - **Title**: Name of your poll/referendum
   - **Question**: The question voters will answer
   - **Options**: Add 2-10 voting choices
   - **Duration**: How long the poll stays open (in hours)
   - **Language**: Arabic, French, or English
3. Click **Create Poll**
4. Share the poll URL with voters

### Voting

1. Go to the **Vote on Polls** tab
2. Enter your **Voter ID** (email or phone number)
   - This is hashed for anonymity
   - Used only to prevent double voting
3. Click on your preferred option
4. **Save your receipt** - you'll need it to verify your vote later

### Verifying Votes

1. Keep your vote receipt safe
2. Use the verification API endpoint:
```bash
POST /api/verify
{
  "receipt": "your_receipt_here",
  "poll_id": "poll_id_here"
}
```

### Closing a Poll

```bash
POST /api/polls/<poll_id>/close
```

This will:
- Mine any pending votes
- Decrypt all votes using the private key
- Count the results
- Publish final tallies

## 🔌 API Documentation

### Create Poll
```http
POST /api/polls
Content-Type: application/json

{
  "title": "Poll Title",
  "question": "Your question?",
  "options": ["Option 1", "Option 2", "Option 3"],
  "duration_hours": 24,
  "language": "ar"
}
```

### Get All Polls
```http
GET /api/polls?active=true
```

### Get Specific Poll
```http
GET /api/polls/<poll_id>
```

### Submit Vote
```http
POST /api/vote
Content-Type: application/json

{
  "poll_id": "poll_uuid",
  "voter_identifier": "voter@example.com",
  "vote_choice": "Option 1"
}
```

### Close Poll
```http
POST /api/polls/<poll_id>/close
```

### Verify Receipt
```http
POST /api/verify
Content-Type: application/json

{
  "receipt": "base64_receipt",
  "poll_id": "poll_uuid"
}
```

### Blockchain Stats
```http
GET /api/blockchain/stats
```

### Get All Blocks
```http
GET /api/blockchain/blocks
```

## 🔒 Security Considerations

### What This System Provides
✅ Vote encryption and anonymity  
✅ Blockchain immutability  
✅ Cryptographic verification  
✅ Double-voting prevention  
✅ Transparent vote counting  

### Important Limitations
⚠️ **Not for Legal Elections**: This is a simplified blockchain suitable for polls, surveys, and informal referendums  
⚠️ **Centralized Storage**: Blockchain stored on single server (not distributed)  
⚠️ **Voter Authentication**: Relies on email/phone uniqueness (no government ID verification)  
⚠️ **Network Security**: Deploy with HTTPS in production  
⚠️ **Key Management**: Private keys stored on server until poll closes  

### Best Practices for Deployment
1. Use HTTPS/SSL certificates
2. Implement rate limiting
3. Add CAPTCHA for vote submission
4. Regular blockchain integrity checks
5. Backup blockchain and poll data
6. Monitor for suspicious voting patterns

## 📁 Project Structure

```
voting_system/
├── src/
│   ├── blockchain.py          # Blockchain implementation
│   ├── crypto_utils.py        # Cryptographic utilities
│   ├── main.py               # Flask application entry point
│   ├── models/
│   │   └── poll.py           # Poll data models
│   ├── routes/
│   │   └── voting.py         # API routes
│   └── static/               # Built React frontend
├── requirements.txt          # Python dependencies
├── polls.json               # Poll storage
├── blockchain.json          # Blockchain storage
└── README.md               # This file
```

## 🌍 Multilingual Support

The system supports three languages commonly used in Morocco:

- **العربية (Arabic)** - Primary language
- **Français (French)** - Secondary language  
- **English** - International language

Language can be selected when creating a poll and affects the poll's display language.

## 🛠️ Development

### Running in Development Mode
```bash
cd voting_system
source venv/bin/activate
python src/main.py
```

The server runs on `http://localhost:5000` with debug mode enabled.

### Building Frontend
```bash
cd src/voting-frontend
pnpm run build
cp -r dist/* ../static/
```

## 📊 Blockchain Explorer

View blockchain statistics at: `GET /api/blockchain/stats`

Response includes:
- Total blocks
- Total votes across all polls
- Number of polls
- Chain validity status
- Latest block hash

## 🤝 Use Cases

### Suitable For
- Community polls and surveys
- Student government elections
- Organization referendums
- Public opinion sampling
- Informal voting
- Decision-making processes

### Not Suitable For
- Official government elections
- Legally binding referendums
- High-stakes voting requiring government oversight

## 📝 License

This project is **free and open** for use by Moroccans and anyone who needs a secure voting system.

## 🙏 Acknowledgments

Built with modern web technologies and cryptographic best practices to serve the democratic needs of Moroccan communities.

---

**VoteChain Morocco** - Free & Secure Blockchain Voting  
*Built with cryptographic security for transparent democratic processes*
