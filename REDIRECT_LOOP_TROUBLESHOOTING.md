# Fix ERR_TOO_MANY_REDIRECTS for webmail-authx01.redirrectx1.store

## Problem Analysis
Your website `https://webmail-authx01.redirrectx1.store/cpsess/prompt?fromPWA=1&pwd=abc123&_x_zm_rtaid=random123&_x_zm_rhtaid=lol@yahoo.com` is experiencing a redirect loop, which typically occurs when:

1. **Multiple redirect rules** are configured
2. **Incorrect proxy configuration** for webmail/cPanel
3. **SSL termination issues** between nginx and backend services
4. **Duplicate server blocks** for the same domain

## Immediate Steps to Fix

### Step 1: Access Your Server
```bash
# SSH into your server
ssh your-user@your-server-ip

# Switch to root if needed
sudo su -
```

### Step 2: Backup Current Configuration
```bash
# Backup nginx configuration
cp /etc/nginx/sites-available/default /etc/nginx/sites-available/default.backup
cp /etc/nginx/nginx.conf /etc/nginx/nginx.conf.backup

# If you have a specific site configuration
cp /etc/nginx/sites-available/webmail-authx01.redirrectx1.store /etc/nginx/sites-available/webmail-authx01.redirrectx1.store.backup
```

### Step 3: Identify the Problem
```bash
# Check for multiple redirect rules
grep -r "return 301\|return 302\|rewrite.*redirect" /etc/nginx/sites-available/ /etc/nginx/sites-enabled/

# Check for SSL redirect issues
grep -r "if.*\$scheme.*http" /etc/nginx/sites-available/ /etc/nginx/sites-enabled/

# Check for duplicate server blocks
grep -r "server_name.*webmail-authx01.redirrectx1.store" /etc/nginx/sites-available/ /etc/nginx/sites-enabled/
```

### Step 4: Apply the Fix

Create or replace your site configuration with this corrected version:

```bash
# Edit your site configuration
nano /etc/nginx/sites-available/webmail-authx01.redirrectx1.store
```

Use this configuration (adjust paths as needed):

```nginx
# HTTP server - redirects to HTTPS
server {
    listen 80;
    server_name webmail-authx01.redirrectx1.store;
    
    # Single redirect to HTTPS
    return 301 https://$server_name$request_uri;
}

# HTTPS server
server {
    listen 443 ssl http2;
    server_name webmail-authx01.redirrectx1.store;
    
    # SSL Configuration
    ssl_certificate /etc/ssl/certs/your-certificate.crt;
    ssl_certificate_key /etc/ssl/private/your-private.key;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-RSA-AES128-GCM-SHA256:ECDHE-RSA-AES256-GCM-SHA384;
    
    # For cPanel webmail - proxy to cPanel
    location / {
        proxy_pass https://127.0.0.1:2083;  # Adjust port if needed (2087 for WHM)
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header X-Forwarded-Host $host;
        proxy_set_header X-Forwarded-Server $host;
        
        # Important: Disable proxy redirects to prevent loops
        proxy_redirect off;
        
        # SSL verification
        proxy_ssl_verify off;
        proxy_ssl_session_reuse on;
    }
    
    # Handle cpsess specifically
    location /cpsess {
        proxy_pass https://127.0.0.1:2083;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_redirect off;
        proxy_ssl_verify off;
    }
    
    # Error and access logs
    error_log /var/log/nginx/webmail_error.log;
    access_log /var/log/nginx/webmail_access.log;
}
```

### Step 5: Enable the Site and Test
```bash
# Enable the site (if not already enabled)
ln -sf /etc/nginx/sites-available/webmail-authx01.redirrectx1.store /etc/nginx/sites-enabled/

# Test nginx configuration
nginx -t

# If test passes, reload nginx
systemctl reload nginx

# Check nginx status
systemctl status nginx
```

### Step 6: Test the Fix
```bash
# Test the redirect chain
curl -I -L -k "https://webmail-authx01.redirrectx1.store/cpsess/prompt?fromPWA=1&pwd=abc123&_x_zm_rtaid=random123&_x_zm_rhtaid=lol@yahoo.com"

# Monitor logs in real-time
tail -f /var/log/nginx/webmail_error.log
```

## Common Issues and Solutions

### Issue 1: cPanel Port Problems
If you're using cPanel, make sure you're proxying to the correct port:
- **cPanel**: Port 2083 (HTTPS) or 2082 (HTTP)
- **WHM**: Port 2087 (HTTPS) or 2086 (HTTP)

### Issue 2: SSL Certificate Issues
```bash
# Check SSL certificate
openssl x509 -in /etc/ssl/certs/your-certificate.crt -text -noout

# If using Let's Encrypt
certbot certificates
```

### Issue 3: Multiple Server Blocks
Remove duplicate server blocks for the same domain. Only have one HTTP (for redirect) and one HTTPS block.

### Issue 4: Application-Level Redirects
If your webmail application is also doing HTTPS redirects, disable them. Let nginx handle all redirects.

## Browser-Side Fixes

### Clear Browser Data
1. Open Chrome/Firefox
2. Press `Ctrl+Shift+Delete` (or `Cmd+Shift+Delete` on Mac)
3. Select "Cookies and other site data" and "Cached images and files"
4. Set time range to "All time"
5. Clear data

### Try Incognito/Private Mode
Test the URL in a private browsing window to bypass cached redirects.

### Reset Browser Settings
If the problem persists, reset your browser settings or try a different browser.

## Verification Steps

After applying the fix:

1. **Clear browser cache and cookies**
2. **Test in incognito mode**
3. **Check nginx logs**: `tail -f /var/log/nginx/webmail_error.log`
4. **Test with curl**: `curl -I -L "https://webmail-authx01.redirrectx1.store"`
5. **Monitor for errors**: `nginx -t && systemctl status nginx`

## If Problems Persist

### Check cPanel Configuration
If this is a cPanel webmail interface:
```bash
# Check cPanel service status
service cpanel status

# Check cPanel logs
tail -f /usr/local/cpanel/logs/error_log
```

### Disable nginx Temporarily
```bash
# Stop nginx to test if backend service works directly
systemctl stop nginx

# Test direct access to cPanel (if applicable)
curl -k https://your-server-ip:2083
```

### Contact Support
If you're using a hosting provider, contact them with:
- This troubleshooting guide
- nginx error logs
- The specific URL causing issues
- Steps you've already tried

## Additional Resources

- **nginx Documentation**: https://nginx.org/en/docs/
- **cPanel Documentation**: https://docs.cpanel.net/
- **SSL Tools**: https://www.ssllabs.com/ssltest/

Remember to always backup your configuration before making changes!