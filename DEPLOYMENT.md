# VoteChain Morocco - Deployment Guide

## 🚀 Quick Start

The VoteChain Morocco voting system is ready to use! You can run it locally or deploy it to any hosting platform.

## 📋 Local Deployment

### Prerequisites
- Python 3.11+
- pip3
- Virtual environment

### Steps

1. **Navigate to project directory**
```bash
cd /home/ubuntu/voting_system
```

2. **Activate virtual environment**
```bash
source venv/bin/activate
```

3. **Run the application**
```bash
python src/main.py
```

4. **Access the application**
Open your browser to: `http://localhost:5000`

The application will start on port 5000 with:
- ✅ Blockchain voting system
- ✅ Cryptographic vote encryption
- ✅ Anonymous voter authentication
- ✅ Real-time blockchain statistics
- ✅ Multilingual interface (Arabic, French, English)

## 🌐 Production Deployment

### Recommended Platforms

#### 1. **Railway.app** (Recommended - Free Tier Available)
```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Initialize project
cd /home/ubuntu/voting_system
railway init

# Deploy
railway up
```

#### 2. **Render.com** (Free Tier Available)
1. Create account at render.com
2. Connect GitHub repository
3. Create new Web Service
4. Set build command: `pip install -r requirements.txt`
5. Set start command: `python src/main.py`

#### 3. **PythonAnywhere** (Free Tier Available)
1. Upload project files
2. Create virtual environment
3. Install requirements
4. Configure WSGI file
5. Reload web app

#### 4. **Heroku** (Paid)
```bash
# Install Heroku CLI
# Create Procfile
echo "web: python src/main.py" > Procfile

# Deploy
heroku create votechain-morocco
git push heroku main
```

### Environment Configuration

For production deployment, set these environment variables:

```bash
FLASK_ENV=production
FLASK_DEBUG=0
SECRET_KEY=your-secret-key-here
PORT=5000
```

### Production Checklist

- [ ] Set `FLASK_ENV=production`
- [ ] Disable debug mode
- [ ] Use strong SECRET_KEY
- [ ] Enable HTTPS/SSL
- [ ] Set up regular backups for `blockchain.json` and `polls.json`
- [ ] Configure rate limiting
- [ ] Set up monitoring and logging
- [ ] Test all features in production environment

## 🔧 Configuration

### Port Configuration
Default port is 5000. To change:
```python
# In src/main.py
app.run(host='0.0.0.0', port=YOUR_PORT, debug=False)
```

### Database Files
The system uses file-based storage:
- `blockchain.json` - Blockchain data
- `polls.json` - Poll information

**Important**: Back up these files regularly!

### CORS Configuration
CORS is enabled by default for API access. To restrict:
```python
# In src/main.py
CORS(app, origins=['https://yourdomain.com'])
```

## 📦 Dependencies

All dependencies are in `requirements.txt`:
- Flask - Web framework
- Flask-CORS - Cross-origin resource sharing
- Flask-SQLAlchemy - Database ORM
- Pure Python cryptography (no compiled dependencies)

## 🔒 Security Notes

### What's Included
✅ Vote encryption using PBKDF2 key derivation  
✅ SHA-256 hashing for anonymity  
✅ Blockchain immutability  
✅ Digital signatures  
✅ Double-voting prevention  

### Production Security
For production use, consider:
1. **HTTPS**: Always use SSL/TLS certificates
2. **Rate Limiting**: Implement request throttling
3. **CAPTCHA**: Add to vote submission
4. **Firewall**: Restrict access to admin endpoints
5. **Monitoring**: Log all voting activity
6. **Backups**: Automated blockchain backups

## 🐛 Troubleshooting

### Port Already in Use
```bash
# Find process using port 5000
lsof -i :5000
# Kill process
kill -9 PID
```

### Module Not Found
```bash
# Reinstall dependencies
pip install -r requirements.txt
```

### Permission Denied
```bash
# Make sure you have write permissions
chmod 755 /home/ubuntu/voting_system
```

### Blockchain Corruption
```bash
# Backup current blockchain
cp blockchain.json blockchain.backup.json
# Reset blockchain (WARNING: loses all data)
echo '[{"index":0,"timestamp":0,"votes":[],"previous_hash":"0","poll_id":"genesis","nonce":0,"hash":"genesis"}]' > blockchain.json
```

## 📊 Monitoring

### Check Blockchain Status
```bash
curl http://localhost:5000/api/blockchain/stats
```

### View All Polls
```bash
curl http://localhost:5000/api/polls
```

### Check Active Polls
```bash
curl http://localhost:5000/api/polls?active=true
```

## 🔄 Updates

To update the application:
1. Pull latest changes
2. Activate virtual environment
3. Update dependencies: `pip install -r requirements.txt`
4. Restart application

## 💾 Backup Strategy

### Automated Backup Script
```bash
#!/bin/bash
# backup.sh
DATE=$(date +%Y%m%d_%H%M%S)
cp blockchain.json backups/blockchain_$DATE.json
cp polls.json backups/polls_$DATE.json
echo "Backup completed: $DATE"
```

Run daily:
```bash
chmod +x backup.sh
crontab -e
# Add: 0 2 * * * /path/to/backup.sh
```

## 🌍 Scaling

For high-traffic scenarios:
1. Use a production WSGI server (Gunicorn, uWSGI)
2. Set up load balancing
3. Implement caching (Redis)
4. Use a proper database (PostgreSQL)
5. Distribute blockchain across nodes

## 📞 Support

For issues or questions:
- Check README.md for detailed documentation
- Review architecture documentation
- Test locally before deploying to production

---

**VoteChain Morocco** - Secure, Free, and Transparent Voting for Everyone
