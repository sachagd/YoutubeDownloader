#!/usr/bin/env bash
DIR="$(cd "$(dirname "$0")" && pwd)"
sed -i "s|APP_PATH|$DIR/ytdl-ubuntu|g" "$DIR/native-messaging.json"
mkdir -p "$HOME/.mozilla/native-messaging-hosts"
cp "$DIR/native-messaging.json" "$HOME/.mozilla/native-messaging-hosts/com.sacha.youtubedownloader.json"
echo "Native messaging host registered successfully."
rm -- "$0"