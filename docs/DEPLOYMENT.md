# Deployment Guide - Ubuntu Systemd Service

This guide explains how to deploy the Demand Planning MCP Server as a systemd service on Ubuntu.

## Prerequisites

- Ubuntu 20.04 LTS or later
- Python 3.11 or higher
- `sudo` access
- Git installed

---

## Installation Steps

### 1. Clone Repository to Production Location

```bash
# Clone to /opt (standard location for third-party software)
sudo mkdir -p /opt/demand-planning-bot
sudo chown $USER:$USER /opt/demand-planning-bot

cd /opt
git clone https://github.com/CohereJohnny/demand-planning-bot.git
cd demand-planning-bot
```

### 2. Install Dependencies

**Option A: Using uv (Recommended)**
```bash
# Install uv if not already installed
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install dependencies
uv sync
```

**Option B: Using pip with system Python**
```bash
# Create virtual environment with system python3
/usr/bin/python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configure Environment Variables

```bash
# Copy example environment file
cp .env.example .env

# Edit with your API keys
nano .env
```

**Required Configuration:**
```ini
# API Keys (REQUIRED)
EIA_API_KEY=your_eia_api_key_here
NEWS_API_KEY=your_newsapi_key_here

# Server Authentication (RECOMMENDED for production)
SERVER_SECRET=your_secure_random_secret_here

# Optional: Customize server settings
SERVER_PORT=8000
DEBUG_MODE=false
```

**Generate a secure SERVER_SECRET:**
```bash
/usr/bin/python3 -c "import secrets; print(secrets.token_urlsafe(32))"
```

### 4. Create Log Directory

```bash
sudo mkdir -p /opt/demand-planning-bot/logs
sudo chown ubuntu:ubuntu /opt/demand-planning-bot/logs
```

### 5. Install Systemd Service File

```bash
# Copy service file to systemd directory
sudo cp demand-planning-bot.service /etc/systemd/system/

# If using a different user than 'ubuntu', edit the service file
sudo nano /etc/systemd/system/demand-planning-bot.service
# Change User= and Group= to your desired user

# Reload systemd to recognize new service
sudo systemctl daemon-reload
```

### 6. Enable and Start Service

```bash
# Enable service to start on boot
sudo systemctl enable demand-planning-bot

# Start the service
sudo systemctl start demand-planning-bot

# Check status
sudo systemctl status demand-planning-bot
```

Expected output:
```
● demand-planning-bot.service - Demand Planning MCP Server
     Loaded: loaded (/etc/systemd/system/demand-planning-bot.service; enabled)
     Active: active (running) since Wed 2025-10-23 12:00:00 UTC; 5s ago
   Main PID: 12345 (python)
      Tasks: 5 (limit: 4915)
     Memory: 125.2M
        CPU: 1.234s
     CGroup: /system.slice/demand-planning-bot.service
             └─12345 /opt/demand-planning-bot/.venv/bin/python /opt/demand-planning-bot/server.py --transport http --port 8000
```

---

## Service Management

### Common Commands

```bash
# Start service
sudo systemctl start demand-planning-bot

# Stop service
sudo systemctl stop demand-planning-bot

# Restart service
sudo systemctl restart demand-planning-bot

# Reload configuration (if changed)
sudo systemctl reload demand-planning-bot

# Check status
sudo systemctl status demand-planning-bot

# Enable on boot
sudo systemctl enable demand-planning-bot

# Disable on boot
sudo systemctl disable demand-planning-bot
```

### View Logs

```bash
# View recent logs
sudo journalctl -u demand-planning-bot -n 100

# Follow logs in real-time
sudo journalctl -u demand-planning-bot -f

# View logs from today
sudo journalctl -u demand-planning-bot --since today

# View logs with timestamps
sudo journalctl -u demand-planning-bot -o short-iso
```

### Check if Service is Running

```bash
# Quick status check
sudo systemctl is-active demand-planning-bot

# Detailed status
sudo systemctl status demand-planning-bot

# Test HTTP endpoint (if configured)
curl http://localhost:8000/health
```

---

## Troubleshooting

### Service Won't Start

1. **Check service status for errors:**
   ```bash
   sudo systemctl status demand-planning-bot
   ```

2. **View detailed logs:**
   ```bash
   sudo journalctl -u demand-planning-bot -n 50 --no-pager
   ```

3. **Common issues:**
   - Missing API keys in `.env`
   - Incorrect file permissions
   - Python virtual environment not activated
   - Port already in use

### Permission Issues

```bash
# Fix ownership
sudo chown -R ubuntu:ubuntu /opt/demand-planning-bot

# Fix permissions
sudo chmod 644 /opt/demand-planning-bot/.env
sudo chmod 755 /opt/demand-planning-bot/server.py
```

### Port Already in Use

```bash
# Check what's using port 8000
sudo lsof -i :8000

# Kill process if needed (replace PID)
sudo kill -9 <PID>

# Or change port in service file
sudo nano /etc/systemd/system/demand-planning-bot.service
# Change --port 8000 to --port 8001
sudo systemctl daemon-reload
sudo systemctl restart demand-planning-bot
```

### Service Keeps Restarting

```bash
# Check restart count
systemctl show demand-planning-bot | grep NRestarts

# Disable restart temporarily for debugging
sudo systemctl edit demand-planning-bot
# Add: [Service]
#      Restart=no

# Test manually
cd /opt/demand-planning-bot
source .venv/bin/activate
python3 server.py --transport http --port 8000
```

---

## Security Hardening

### 1. Use Non-Root User

The service file already runs as user `ubuntu`. Never run as `root`.

### 2. Set Strong SERVER_SECRET

```bash
# Generate strong secret (32+ characters)
/usr/bin/python3 -c "import secrets; print(secrets.token_urlsafe(32))"

# Add to .env
echo "SERVER_SECRET=<generated-secret>" >> /opt/demand-planning-bot/.env
```

### 3. Firewall Configuration

```bash
# Allow only specific IPs to access the service
sudo ufw allow from 192.168.1.0/24 to any port 8000

# Or use nginx as reverse proxy
sudo apt install nginx
# Configure nginx to proxy to localhost:8000
```

### 4. File Permissions

```bash
# Secure .env file (contains secrets)
chmod 600 /opt/demand-planning-bot/.env

# Ensure only ubuntu user can read
sudo chown ubuntu:ubuntu /opt/demand-planning-bot/.env
```

### 5. Enable HTTPS (Recommended)

Use nginx or Apache as reverse proxy with SSL:

```bash
# Install certbot for Let's Encrypt SSL
sudo apt install certbot python3-certbot-nginx

# Configure nginx reverse proxy
sudo nano /etc/nginx/sites-available/demand-planning-bot

# Get SSL certificate
sudo certbot --nginx -d yourdomain.com
```

---

## Updates and Maintenance

### Update Application

```bash
# Stop service
sudo systemctl stop demand-planning-bot

# Pull latest code
cd /opt/demand-planning-bot
git pull origin main

# Update dependencies
uv sync
# or: source .venv/bin/activate && pip install -r requirements.txt

# Restart service
sudo systemctl start demand-planning-bot

# Verify
sudo systemctl status demand-planning-bot
```

### Backup Configuration

```bash
# Backup .env file
sudo cp /opt/demand-planning-bot/.env /opt/demand-planning-bot/.env.backup

# Backup entire directory
sudo tar -czf /backup/demand-planning-bot-$(date +%Y%m%d).tar.gz /opt/demand-planning-bot
```

### Monitor Resource Usage

```bash
# Check memory usage
systemctl show demand-planning-bot | grep Memory

# Check CPU usage
top -p $(pgrep -f demand-planning-bot)

# View all resource limits
systemctl show demand-planning-bot
```

---

## Advanced Configuration

### Change Transport Mode

Edit service file to use stdio instead of HTTP:

```bash
sudo nano /etc/systemd/system/demand-planning-bot.service

# Change ExecStart line:
# ExecStart=/opt/demand-planning-bot/.venv/bin/python3 /opt/demand-planning-bot/server.py --transport stdio

sudo systemctl daemon-reload
sudo systemctl restart demand-planning-bot
```

### Run Multiple Instances

Create multiple service files for different ports:

```bash
# Copy service file
sudo cp /etc/systemd/system/demand-planning-bot.service \
        /etc/systemd/system/demand-planning-bot-8001.service

# Edit to use different port
sudo nano /etc/systemd/system/demand-planning-bot-8001.service
# Change --port 8000 to --port 8001

# Enable and start
sudo systemctl enable demand-planning-bot-8001
sudo systemctl start demand-planning-bot-8001
```

### Custom Logging

Add custom log file location:

```bash
sudo nano /etc/systemd/system/demand-planning-bot.service

# Add to [Service] section:
# StandardOutput=append:/var/log/demand-planning-bot/stdout.log
# StandardError=append:/var/log/demand-planning-bot/stderr.log

# Create log directory
sudo mkdir -p /var/log/demand-planning-bot
sudo chown ubuntu:ubuntu /var/log/demand-planning-bot

sudo systemctl daemon-reload
sudo systemctl restart demand-planning-bot
```

---

## Monitoring and Alerts

### Setup Health Check Script

```bash
# Create health check script
cat > /opt/demand-planning-bot/healthcheck.sh << 'EOF'
#!/bin/bash
RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/health)
if [ "$RESPONSE" -ne 200 ]; then
    echo "Health check failed: HTTP $RESPONSE"
    sudo systemctl restart demand-planning-bot
    # Send alert email
    echo "Demand Planning Bot was restarted at $(date)" | mail -s "Alert: Service Restart" admin@example.com
fi
EOF

chmod +x /opt/demand-planning-bot/healthcheck.sh

# Add to crontab (every 5 minutes)
(crontab -l 2>/dev/null; echo "*/5 * * * * /opt/demand-planning-bot/healthcheck.sh") | crontab -
```

### Integrate with Monitoring Tools

**Prometheus Metrics** (if implementing):
- Add metrics endpoint to server
- Configure Prometheus scraper
- Set up Grafana dashboard

**Systemd Journal Integration:**
```bash
# Forward logs to syslog
sudo nano /etc/systemd/journald.conf
# Set: ForwardToSyslog=yes
sudo systemctl restart systemd-journald
```

---

## Uninstall

To completely remove the service:

```bash
# Stop and disable service
sudo systemctl stop demand-planning-bot
sudo systemctl disable demand-planning-bot

# Remove service file
sudo rm /etc/systemd/system/demand-planning-bot.service

# Reload systemd
sudo systemctl daemon-reload

# Optionally remove application
sudo rm -rf /opt/demand-planning-bot
```

---

## Quick Reference

| Task | Command |
|------|---------|
| Start service | `sudo systemctl start demand-planning-bot` |
| Stop service | `sudo systemctl stop demand-planning-bot` |
| Restart service | `sudo systemctl restart demand-planning-bot` |
| Check status | `sudo systemctl status demand-planning-bot` |
| View logs | `sudo journalctl -u demand-planning-bot -f` |
| Enable on boot | `sudo systemctl enable demand-planning-bot` |
| Disable on boot | `sudo systemctl disable demand-planning-bot` |
| Reload config | `sudo systemctl daemon-reload` |

---

**For Production Use:**
1. ✅ Use HTTP transport (not stdio)
2. ✅ Set strong SERVER_SECRET
3. ✅ Configure firewall rules
4. ✅ Use reverse proxy with SSL
5. ✅ Monitor logs regularly
6. ✅ Set up automated backups
7. ✅ Configure health checks

**Support:** For issues, check logs with `sudo journalctl -u demand-planning-bot -f`

