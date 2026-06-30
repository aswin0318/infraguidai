#!/bin/bash
set -euo pipefail

# Write environment file for the systemd service
mkdir -p /etc/infraguidai
cat > /etc/infraguidai/env << 'ENVEOF'
AWS_SECRET_NAME=${secret_name}
AWS_REGION=${aws_region}
APP_ENV=${app_env}
LOG_LEVEL=INFO
FRONTEND_ORIGIN=${frontend_origin}
ENVEOF

# Ensure correct permissions
chmod 600 /etc/infraguidai/env

# Reload systemd, enable and start the service
systemctl daemon-reload
systemctl enable infraguidai
systemctl restart infraguidai
