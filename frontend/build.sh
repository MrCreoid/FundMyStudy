# Replace the entire file with this
echo '#!/bin/bash
set -e  # Exit on any error
cd "$(dirname "$0")" || exit 1  # Ensure we're in frontend folder
echo "Installing dependencies..."
npm install
echo "Building application..."
npm run build
echo "Build complete!"' > frontend/build.sh

# Make executable
chmod +x frontend/build.sh