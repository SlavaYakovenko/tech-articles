# Optimizing Ollama for Claude Code on macOS

![Architecture of Claude Code, Ollama, and Gemma 4 symbiosis](./images/claude-ollama-gemma.png)

This guide provides comprehensive instructions on how to configure Ollama on macOS to achieve maximum performance when used as a backend for Claude Code and other AI agents.

## The Problem

When using Claude Code with models via Ollama, users often encounter performance bottlenecks.
## The Solution

To transform Ollama from a simple application into a high-performance background engine, we need to move beyond the UI and implement a low-level configuration using a macOS `LaunchAgent`. This ensures the service starts automatically with the correct environment variables.

### Step 1: System Cleanup

Before applying the new configuration, you must disable standard launch mechanisms to avoid "Address already in use" conflicts.

1. **Disable Background Items**: Go to `System Settings` -> `General` -> `Login Items` and toggle off Ollama in the Background Items section.
2. **Terminate Active Processes**:
   ```bash
   # Kill all running Ollama instances
   killall Ollama 2>/dev/null; killall ollama 2>/dev/null
   ```
3. **Verify Port Availability**:
   ```bash
   # Ensure port 11434 is free
   lsof -i :11434
   ```
   If a process is still listed, terminate it using `kill -9 [PID]`.

### Step 2: Creating the LaunchAgent Configuration

Using a `LaunchAgent` is the most reliable method for 2026, as it maintains access to `/Applications` and your local model library.

Create the configuration file using the following command:

```bash
# Create the plist file to manage Ollama as a system service
# ~/Library/LaunchAgents/ai.ollama.plist
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd"\>
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>ai.ollama</string>
    <key>ProgramArguments</key>
    <array>
        <string>/Applications/Ollama.app/Contents/Resources/ollama</string>
        <string>serve</string>
    </array>
    <key>EnvironmentVariables</key>
    <dict>
        <key>OLLAMA_KEEP_ALIVE</key>
        <string>-1</string>
        <key>OLLAMA_NUM_PARALLEL</key>
        <string>4</string>
        <key>OLLAMA_CONTEXT_LENGTH</key>
        <string>65536</string>
    </dict>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
    <key>StandardOutPath</key>
    <string>/tmp/ollama.stdout.log</string>
    <key>StandardErrorPath</key>
    <string>/tmp/ollama.stderr.log</string>
</dict>
</plist>
EOF
```

### Step 3: Service Activation

Apply the correct permissions and register the agent with the system:

```bash
# Set permissions and load the agent
chmod 644 ~/Library/LaunchAgents/ai.ollama.plist
launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/ai.ollama.plist
```

### Step 4: Verification and Tuning

Verify that the service is running and the parameters are active.

**Status Check**:
```bash
# Check if the service is registered and has a PID
launchctl list | grep ai.ollama
```

**Configuration Check**:
```bash
# Verify environment variables are applied to the running process
ps -ww -E -p $(pgrep -f "ollama serve") | grep OLLAMA
```

## Benefits/Results

By applying these settings, you achieve a significant boost in development velocity:

| Parameter | Value | Benefit |
| :--- | :--- | :--- |
| `OLLAMA_KEEP_ALIVE` | `-1` | Models stay in GPU memory; responses are instantaneous. |
| `OLLAMA_NUM_PARALLEL` | `4` | Allows Claude Code to scan files and maintain chat simultaneously. |
| `OLLAMA_CONTEXT_LENGTH` | `65536` | Increases the "memory" for handling long source files. |

## Conclusion

Your Ollama instance is now optimized to serve as a high-performance backend for Claude Code and Gemma 4. This setup removes the UI-imposed limitations and ensures a seamless, low-latency AI development experience.

---

## Quick Reference

### Essential Commands

```bash
# Reload configuration after editing the .plist file
launchctl bootout gui/$(id -u) ~/Library/LaunchAgents/ai.ollama.plist
launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/ai.ollama.plist

# Check logs for debugging
tail -f /tmp/ollama.stdout.log
```

### Useful Links
- [Ollama Official Documentation](https://ollama.com/docs)
- [Claude Code Guide](https://claude.ai/code)
