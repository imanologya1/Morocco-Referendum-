# VoteChain Morocco - User Guide

## 🗳️ Welcome to VoteChain Morocco

VoteChain Morocco is a free, secure blockchain-based voting system designed for conducting transparent referendums, elections, and polls with cryptographic guarantees.

## 🎯 Quick Start

### For Voters

1. **Access the Platform**
   - Open the VoteChain Morocco website
   - You'll see the main dashboard with blockchain statistics

2. **Enter Your Voter ID**
   - In the "Your Voter ID" field, enter your email or phone number
   - This is used only for anonymous authentication
   - Your identity is hashed and cannot be traced back to your vote

3. **View Available Polls**
   - Browse active polls displayed on the main page
   - Each poll shows:
     - Title and question
     - Available options
     - Number of votes cast
     - Closing date

4. **Cast Your Vote**
   - Click on your preferred option
   - Your vote is immediately encrypted and added to the blockchain
   - You'll receive a confirmation and a **receipt**

5. **Save Your Receipt**
   - **IMPORTANT**: Save the receipt shown after voting
   - This receipt allows you to verify your vote on the blockchain later
   - Keep it secure and private

### For Poll Creators

1. **Navigate to Create Poll Tab**
   - Click on "Create Poll" at the top of the page

2. **Fill in Poll Details**
   - **Title**: Give your poll a clear, descriptive name
   - **Question**: State the question voters will answer
   - **Options**: Add 2-10 voting choices
     - Click "Add Option" to add more choices
     - Click "×" to remove an option
   - **Duration**: Set how long the poll stays open (in hours)
   - **Language**: Choose Arabic, French, or English

3. **Create the Poll**
   - Click "Create Poll" button
   - You'll receive a unique poll URL
   - Share this URL with voters

4. **Monitor Your Poll**
   - View real-time vote counts
   - Check blockchain statistics
   - See when the poll closes

## 🔐 Security Features

### For Voters

**Your vote is:**
- ✅ **Encrypted** - Vote content is encrypted before storage
- ✅ **Anonymous** - Your identity is hashed and cannot be traced
- ✅ **Immutable** - Once cast, votes cannot be changed or deleted
- ✅ **Verifiable** - Use your receipt to verify your vote on the blockchain
- ✅ **Protected** - One person can only vote once per poll

**What we don't know:**
- ❌ Your actual identity
- ❌ How you voted (until poll closes)
- ❌ Your location or device information

### How Anonymity Works

1. **Voter Token Generation**
   - Your email/phone + poll ID → SHA-256 hash
   - This creates a unique anonymous token
   - Same input always creates same token (prevents double voting)
   - Token cannot be reversed to reveal your identity

2. **Vote Encryption**
   - Your vote choice is encrypted using the poll's public key
   - Encryption uses PBKDF2 key derivation with 100,000 iterations
   - Only the poll creator can decrypt votes after closing

3. **Blockchain Storage**
   - Encrypted vote stored in a block
   - Block is mined with proof-of-work
   - Block is linked to previous blocks (immutable chain)

## 📊 Understanding the Dashboard

### Blockchain Statistics

- **Total Polls**: Number of polls created
- **Total Votes**: All votes across all polls
- **Blockchain Blocks**: Number of blocks in the chain
- **Chain Status**: ✓ Valid or ✗ Invalid

### Poll Information

Each poll card shows:
- **Title**: Poll name
- **Question**: What's being voted on
- **Options**: Voting choices
- **Votes**: Current vote count
- **Closes**: When voting ends
- **Language**: Poll language (AR/FR/EN)

## 🎨 Language Support

VoteChain Morocco supports three languages:

- **العربية (Arabic)** - Primary language for Morocco
- **Français (French)** - Widely used in Morocco
- **English** - International language

Select your preferred language when creating a poll.

## ✅ Best Practices

### For Voters

1. **Use a Real Email/Phone**
   - Ensures you can only vote once
   - Keeps your vote anonymous

2. **Save Your Receipt**
   - Download or copy the receipt text
   - Store it securely
   - Don't share it publicly

3. **Vote Once**
   - You cannot change your vote after submission
   - Think carefully before voting

4. **Verify Your Vote**
   - Use your receipt to verify your vote was recorded
   - Check the blockchain explorer

### For Poll Creators

1. **Clear Questions**
   - Make your question unambiguous
   - Provide clear voting options

2. **Appropriate Duration**
   - Give voters enough time to participate
   - Common durations: 24 hours, 7 days, 30 days

3. **Share Widely**
   - Distribute the poll URL to all eligible voters
   - Use multiple channels (email, social media, etc.)

4. **Monitor Results**
   - Check vote counts regularly
   - Close the poll when time expires

5. **Publish Results**
   - After closing, results are automatically decrypted
   - Share final tallies with participants

## 🔍 Verifying Your Vote

### Using Your Receipt

1. **Keep Your Receipt Safe**
   - The receipt contains a unique hash of your vote
   - This hash is stored on the blockchain

2. **Verification Process**
   - Go to the verification endpoint (API)
   - Submit your receipt and poll ID
   - System checks if your vote exists on blockchain

3. **What Verification Proves**
   - ✓ Your vote was recorded
   - ✓ Your vote is on the blockchain
   - ✓ Your vote hasn't been tampered with

### Blockchain Explorer

View all blocks and votes:
- Navigate to `/api/blockchain/blocks`
- See the complete blockchain
- Verify chain integrity

## ⚠️ Important Limitations

### What This System Is

✅ **Suitable for:**
- Community polls and surveys
- Student government elections
- Organization referendums
- Public opinion sampling
- Informal voting
- Decision-making processes

### What This System Is Not

❌ **Not suitable for:**
- Official government elections
- Legally binding referendums
- High-stakes voting requiring government oversight
- Situations requiring government ID verification

### Technical Limitations

- **Centralized Storage**: Blockchain stored on single server
- **Simplified Blockchain**: Not a distributed network
- **Voter Authentication**: Based on email/phone uniqueness
- **Key Management**: Private keys stored on server

## 🆘 Troubleshooting

### "You have already voted"
- You can only vote once per poll
- Your voter ID (email/phone) is already registered
- This prevents double voting

### "Poll is closed"
- The voting period has ended
- Results are being counted
- Check back for final results

### "Invalid vote choice"
- The option you selected doesn't exist
- Refresh the page and try again

### "Missing required fields"
- Make sure you entered your voter ID
- Select a voting option
- All fields must be filled

### Receipt Not Showing
- Check if vote was submitted successfully
- Look for confirmation message
- Contact poll administrator if issue persists

## 📱 Mobile Usage

VoteChain Morocco is fully responsive and works on:
- 📱 Smartphones (iOS, Android)
- 💻 Tablets
- 🖥️ Desktop computers

The interface automatically adapts to your screen size.

## 🌟 Tips for Success

### Creating Effective Polls

1. **Be Specific**: Clear, unambiguous questions get better responses
2. **Limit Options**: 3-5 options work best for most polls
3. **Set Realistic Timeframes**: Give voters adequate time
4. **Promote Widely**: More participants = more representative results

### Participating in Polls

1. **Read Carefully**: Understand the question before voting
2. **Vote Promptly**: Don't wait until the last minute
3. **Keep Records**: Save your receipt for verification
4. **Respect Results**: Accept the outcome of democratic voting

## 📞 Getting Help

### Resources

- **README.md**: Technical documentation
- **DEPLOYMENT.md**: Deployment instructions
- **Architecture Documentation**: System design details

### Common Questions

**Q: Is my vote really anonymous?**
A: Yes! Your identity is hashed using SHA-256 and cannot be traced back to your vote.

**Q: Can I change my vote?**
A: No. Once submitted, votes are immutable on the blockchain.

**Q: How do I know my vote was counted?**
A: Use your receipt to verify your vote on the blockchain.

**Q: What happens when a poll closes?**
A: Votes are decrypted and counted automatically. Results are published immediately.

**Q: Is this system free?**
A: Yes! VoteChain Morocco is completely free to use.

**Q: Can poll creators see how I voted?**
A: Not until the poll closes. Votes are encrypted during the voting period.

## 🎓 Understanding Blockchain Voting

### Why Blockchain?

Traditional voting systems have challenges:
- ❌ Centralized control
- ❌ Potential for manipulation
- ❌ Lack of transparency
- ❌ Difficult to verify

Blockchain voting provides:
- ✅ Decentralized verification
- ✅ Immutable records
- ✅ Complete transparency
- ✅ Easy verification

### How It Works

1. **Vote Submission**: Your vote is encrypted and signed
2. **Blockchain Addition**: Vote added to pending transactions
3. **Block Mining**: Votes are batched and mined into blocks
4. **Chain Verification**: Each block links to the previous one
5. **Result Counting**: After closing, votes are decrypted and tallied

### Trust Through Cryptography

- **Encryption**: Protects vote content
- **Hashing**: Ensures anonymity
- **Digital Signatures**: Prevents tampering
- **Proof-of-Work**: Secures the blockchain

---

## 🇲🇦 Made for Morocco

VoteChain Morocco is designed specifically for Moroccan communities with:
- Multilingual support (Arabic, French, English)
- Free and accessible to all
- Culturally appropriate interface
- Focus on transparency and democracy

**Vote with confidence. Vote with VoteChain Morocco.**

---

*For technical support or questions, please refer to the README.md file or contact your poll administrator.*
