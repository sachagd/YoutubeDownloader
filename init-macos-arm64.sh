#!/usr/bin/env bash
DIR="$(cd "$(dirname "$0")" && pwd)"
mkdir -p "$HOME/Library/Application Support/Mozilla/NativeMessagingHosts"
cp "$DIR/native-messaging.json" "$HOME/Library/Application Support/Mozilla/NativeMessagingHosts/com.sacha.youtubedownloader.json"
echo "Native messaging host registered successfully."
chmod +x ytdl_macos_arm64
rm -- "$0"