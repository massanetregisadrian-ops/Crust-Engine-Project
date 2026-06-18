# Crust Engine

Crust Engine is a custom Minecraft Java Edition launcher built with Python.

## Features

- Install and launch Minecraft Java Edition (vanilla and modded)
- Sign in with a Microsoft account (premium login) using the standard
  Xbox Live / XSTS / Minecraft Services OAuth flow, via
  [minecraft-launcher-lib](https://github.com/JakobDev/minecraft-launcher-lib)
- Offline/skin mode for testing without signing in

## Status

This project is currently in active development as a personal/independent
launcher project.

## How login works

Login is handled entirely through Microsoft's official OAuth 2.0
authorization code flow with PKCE. The user signs in with their own
Microsoft account in their browser; the launcher never sees or stores
their password, only the resulting OAuth tokens needed to launch the
game locally on their own machine.
