#!/bin/bash

# Nginx Redirect Loop Fix Script
# This script helps diagnose and fix ERR_TOO_MANY_REDIRECTS errors

echo "=== Nginx Redirect Loop Troubleshooting Script ==="
echo "This script will help you fix ERR_TOO_MANY_REDIRECTS errors"
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_info() {
    echo -e "[INFO] $1"
}

# Check if running as root
if [[ $EUID -ne 0 ]]; then
   print_error "This script should be run as root (use sudo)"
   exit 1
fi

# Step 1: Check nginx status
echo "=== Step 1: Checking nginx status ==="
if systemctl is-active --quiet nginx; then
    print_success "Nginx is running"
else
    print_error "Nginx is not running"
    echo "Starting nginx..."
    systemctl start nginx
fi

# Step 2: Find nginx configuration files
echo ""
echo "=== Step 2: Locating nginx configuration files ==="
NGINX_CONF="/etc/nginx/nginx.conf"
SITES_AVAILABLE="/etc/nginx/sites-available"
SITES_ENABLED="/etc/nginx/sites-enabled"

if [ -f "$NGINX_CONF" ]; then
    print_success "Found main nginx config: $NGINX_CONF"
else
    print_error "Main nginx config not found at $NGINX_CONF"
fi

# Step 3: Check for common redirect loop causes
echo ""
echo "=== Step 3: Checking for redirect loop causes ==="

# Check for multiple redirect rules
echo "Checking for multiple redirect rules..."
REDIRECT_COUNT=$(grep -r "return 301\|return 302\|rewrite.*redirect\|rewrite.*permanent" $SITES_AVAILABLE $SITES_ENABLED 2>/dev/null | wc -l)
if [ "$REDIRECT_COUNT" -gt 2 ]; then
    print_warning "Found $REDIRECT_COUNT redirect rules. This might cause loops."
    echo "Redirect rules found:"
    grep -r "return 301\|return 302\|rewrite.*redirect\|rewrite.*permanent" $SITES_AVAILABLE $SITES_ENABLED 2>/dev/null
fi

# Check for SSL redirect issues
echo ""
echo "Checking for SSL redirect issues..."
SSL_REDIRECTS=$(grep -r "if.*\$scheme.*http" $SITES_AVAILABLE $SITES_ENABLED 2>/dev/null | wc -l)
if [ "$SSL_REDIRECTS" -gt 0 ]; then
    print_warning "Found potentially problematic SSL redirect rules:"
    grep -r "if.*\$scheme.*http" $SITES_AVAILABLE $SITES_ENABLED 2>/dev/null
fi

# Step 4: Test nginx configuration
echo ""
echo "=== Step 4: Testing nginx configuration ==="
if nginx -t; then
    print_success "Nginx configuration syntax is valid"
else
    print_error "Nginx configuration has syntax errors"
    echo "Please fix the syntax errors before proceeding"
    exit 1
fi

# Step 5: Check for duplicate server blocks
echo ""
echo "=== Step 5: Checking for duplicate server blocks ==="
DOMAIN="webmail-authx01.redirrectx1.store"
DUPLICATE_SERVERS=$(grep -r "server_name.*$DOMAIN" $SITES_AVAILABLE $SITES_ENABLED 2>/dev/null | wc -l)
if [ "$DUPLICATE_SERVERS" -gt 2 ]; then
    print_warning "Found multiple server blocks for $DOMAIN:"
    grep -r "server_name.*$DOMAIN" $SITES_AVAILABLE $SITES_ENABLED 2>/dev/null
fi

# Step 6: Provide solution
echo ""
echo "=== Step 6: Recommended Solution ==="
print_info "To fix redirect loops, follow these steps:"
echo ""
echo "1. Backup your current configuration:"
echo "   sudo cp /etc/nginx/sites-available/default /etc/nginx/sites-available/default.backup"
echo ""
echo "2. Edit your site configuration (usually in /etc/nginx/sites-available/):"
echo "   sudo nano /etc/nginx/sites-available/your-site"
echo ""
echo "3. Ensure you have ONLY ONE redirect from HTTP to HTTPS:"
echo "   - Remove any duplicate redirect rules"
echo "   - Use 'return 301 https://\$server_name\$request_uri;' for HTTP to HTTPS redirect"
echo ""
echo "4. For your webmail application, ensure proper proxy configuration:"
echo "   - If using cPanel, proxy to the correct cPanel port (usually 2083 or 2087)"
echo "   - Set proper proxy headers to prevent loops"
echo ""
echo "5. Test and reload nginx:"
echo "   sudo nginx -t && sudo systemctl reload nginx"
echo ""

# Step 7: Common fixes
echo "=== Step 7: Common Fixes for Webmail Redirect Loops ==="
echo ""
print_info "Common causes and fixes:"
echo ""
echo "1. Multiple HTTPS redirects:"
echo "   - Problem: Both nginx and the application are redirecting to HTTPS"
echo "   - Fix: Remove application-level HTTPS redirects, let nginx handle it"
echo ""
echo "2. Incorrect proxy configuration:"
echo "   - Problem: Proxy headers not set correctly"
echo "   - Fix: Add these headers to your proxy configuration:"
echo "     proxy_set_header Host \$host;"
echo "     proxy_set_header X-Real-IP \$remote_addr;"
echo "     proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;"
echo "     proxy_set_header X-Forwarded-Proto \$scheme;"
echo ""
echo "3. cPanel webmail specific:"
echo "   - Problem: cPanel expects specific configuration"
echo "   - Fix: Use the sample configuration provided in nginx_fix.conf"
echo ""

# Step 8: Test the specific URL
echo "=== Step 8: Testing your specific URL ==="
URL="https://webmail-authx01.redirrectx1.store/cpsess/prompt?fromPWA=1&pwd=abc123&_x_zm_rtaid=random123&_x_zm_rhtaid=lol@yahoo.com"
print_info "Testing redirect chain for your URL..."
echo "curl -I -L -k \"$URL\" 2>/dev/null | grep -E '^HTTP|^Location'"

# Final recommendations
echo ""
echo "=== Final Recommendations ==="
print_warning "IMPORTANT: For your specific webmail setup:"
echo ""
echo "1. If this is a cPanel webmail interface:"
echo "   - Make sure you're proxying to the correct cPanel port"
echo "   - Use the configuration from nginx_fix.conf as a template"
echo ""
echo "2. Check your SSL certificate:"
echo "   - Ensure SSL certificate is valid and properly configured"
echo "   - Use 'sudo certbot certificates' if using Let's Encrypt"
echo ""
echo "3. Clear browser cache and cookies:"
echo "   - Clear all cookies for webmail-authx01.redirrectx1.store"
echo "   - Try accessing in private/incognito mode"
echo ""
echo "4. Monitor nginx logs:"
echo "   - tail -f /var/log/nginx/error.log"
echo "   - tail -f /var/log/nginx/access.log"
echo ""

print_success "Troubleshooting script completed!"
print_info "Review the output above and apply the recommended fixes."
print_info "Use the sample configuration in nginx_fix.conf as a reference."