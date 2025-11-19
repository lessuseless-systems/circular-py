#!/usr/bin/env bash
set -euo pipefail

# Helper script to start the Nix daemon if it isn't running.
# Intended for dev/CI environments (containers) where systemd is not active.

SOCKET="/nix/var/nix/daemon-socket/socket"
DAEMON_BIN="/nix/var/nix/profiles/default/bin/nix-daemon"

function die() {
  echo "ERROR: $*" >&2
  exit 1
}

echo "Checking Nix daemon socket: ${SOCKET}"
if [ -S "$SOCKET" ]; then
  echo "Socket exists: $SOCKET"
else
  echo "Socket does not exist: $SOCKET (daemon may not be running)"
fi

if pgrep -f 'nix-daemon' > /dev/null 2>&1; then
  echo "nix-daemon appears to be running (pgrep matched)"
  exit 0
fi

if [ ! -x "$DAEMON_BIN" ]; then
  die "nix-daemon binary not found at '$DAEMON_BIN'. Is Nix installed?"
fi

echo "Attempting to start nix-daemon as root..."
if sudo "$DAEMON_BIN" >/dev/null 2>&1 & then
  sleep 1
  if pgrep -f 'nix-daemon' >/dev/null 2>&1; then
    echo "nix-daemon started successfully"
    exit 0
  fi
fi

die "Failed to start nix-daemon. Try running 'sudo $DAEMON_BIN &' manually or enable it via systemd if present."
