#!/usr/bin/env bash
DIR="$(cd "$(dirname "$0")" && pwd)"
sed -i '' "s|APP_PATH|$DIR/ytdl-macos-arm64|g" "$DIR/native-messaging.json"
mkdir -p "$HOME/Library/Application Support/Mozilla/NativeMessagingHosts"
cp "$DIR/native-messaging.json" "$HOME/Library/Application Support/Mozilla/NativeMessagingHosts/com.sacha.youtubedownloader.json"
echo "Native messaging host registered successfully."
chmod +x ytdl-macos-arm64
xattr -d com.apple.quarantine "$DIR/ytdl-macos-arm64"
xattr -dr com.apple.quarantine "$DIR/_internal"