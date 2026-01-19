<div align="center">
    <img src="resources/github_back.png" alt="Terminal Background">
</div>

<div align="justify">
<picture>
    <source media="(prefers-color-scheme: dark)" srcset="./output.gif">
    <source media="(prefers-color-scheme: light)" srcset="./output.gif">
    <img alt="ZOVOS" src="output.gif">
</picture>
</div>

```text
gr00ss@arch ~> systemctl --user status github-profile
● github-profile.service - GitHub Profile Service
     Loaded: loaded (/home/gr00ss/.config/systemd/user/github-profile.service; enabled; preset: enabled)
     Active: active (running) since Tue 2026-01-20 14:23:17 MSK; 3h 42min ago
 Invocation: 0x7f8a9c2e3b4d5f6a7b8c9d0e1f2a3b4c
   Main PID: 1337 (gr00ss)
      Tasks: 8 (limit: 8873)
     Memory: 256M (peak: 512M)
        CPU: 1.25h
     CGroup: /user.slice/user-1000.slice/user@1000.service/app.slice/github-profile.service
             └─1337 /usr/bin/github-profile -config /home/gr00ss/.config/github/config.json

Jan 20 14:23:17 arch github-profile[1337]: GitHub Profile Engine v3.14.15 (Gr00ss Edition)
Jan 20 14:23:17 arch github-profile[1337]: Initializing profile: https://github.com/Gr00ss  
Jan 20 14:23:18 arch github-profile[1337]: Loading user configuration from /home/gr00ss/.config/github/config.json
Jan 20 14:23:19 arch github-profile[1337]: ✓ Skills matrix loaded: C, C++, Python, JavaScript, Bash
Jan 20 14:23:20 arch github-profile[1337]: ✓ Project repositories indexed: 12 active projects
Jan 20 14:23:21 arch github-profile[1337]: ✓ SSH keys verified: ed25519-key-20260120@gr00ss.system
Jan 20 14:23:22 arch github-profile[1337]: [INFO] Profile optimization: terminal theme applied
Jan 20 14:23:23 arch github-profile[1337]: ✓ Profile status: ONLINE and READY
Jan 20 14:23:24 arch github-profile[1337]: [WARNING] Memory usage high: 256M - consider optimizing README.md
Jan 20 14:23:25 arch github-profile[1337]: [SUCCESS] Profile service started successfully

Profile Configuration:
├── User: Gr00ss
├── Location: /home/gr00ss/github/Gr00ss
├── Shell: /bin/bash
├── Theme: linux-terminal (dark mode)
├── Color Scheme: 
│   ├── Border: dark-red (#8B0000)
│   ├── Header: red (#FF0000)
│   ├── Text: light-red (#FF6347)
│   ├── Normal: white (#FFFFFF)
│   └── Commands: orange (#FFA500)
└── Status: ACTIVE

Recent Activity Log:
Jan 20 15:10:22 arch github-profile[1337]: [COMMIT] Pushed update to README.md
Jan 20 15:45:18 arch github-profile[1337]: [MERGE] Merged feature/terminal-theme branch
Jan 20 16:20:33 arch github-profile[1337]: [BUILD] Successfully built profile assets
Jan 20 17:05:47 arch github-profile[1337]: [ONLINE] Profile accessed by 12 unique visitors
Jan 20 17:58:12 arch github-profile[1337]: [UPDATE] System statistics refreshed

System Statistics:
├── Uptime: 5 years, 3 months, 14 days
├── Repositories: 12 public, 8 private
├── Contributions: 1,842 this year
├── Languages: C(45%), Python(25%), JavaScript(15%), Bash(10%), Other(5%)
└── Network: ONLINE @ 1 Gbps

Service Control:
│ systemctl --user start github-profile    # Start profile service
│ systemctl --user stop github-profile     # Stop profile service
│ systemctl --user restart github-profile  # Restart profile service
│ systemctl --user status github-profile   # Check profile status
└── journalctl --user -u github-profile -f # View live logs

gr00ss@arch ~> [SYSTEM READY] [STATUS: ONLINE]