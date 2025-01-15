## GitHub Copilot Chat

- Extension Version: 0.22.4 (prod)
- VS Code: vscode/1.95.2
- OS: Mac

## Network

User Settings:
```json
  "github.copilot.advanced": {
    "debug.useElectronFetcher": true,
    "debug.useNodeFetcher": false
  }
```

Connecting to https://api.github.com:
- DNS ipv4 Lookup: 20.26.156.210 (22 ms)
- DNS ipv6 Lookup: ::ffff:20.26.156.210 (18 ms)
- Electron Fetcher (configured): HTTP 200 (175 ms)
- Node Fetcher: HTTP 200 (69 ms)
- Helix Fetcher: HTTP 200 (330 ms)

Connecting to https://api.individual.githubcopilot.com/_ping:
- DNS ipv4 Lookup: 140.82.113.22 (19 ms)
- DNS ipv6 Lookup: ::ffff:140.82.113.22 (5 ms)
- Electron Fetcher (configured): HTTP 200 (93 ms)
- Node Fetcher: HTTP 200 (292 ms)
- Helix Fetcher: HTTP 200 (295 ms)

## Documentation

In corporate networks: [Troubleshooting firewall settings for GitHub Copilot](https://docs.github.com/en/copilot/troubleshooting-github-copilot/troubleshooting-firewall-settings-for-github-copilot).