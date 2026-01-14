# ExDex.cc - Cryptocurrency Trading Platform

A decentralized exchange platform with advanced security protocols for wallet and trading functionality. Only EXDEX-approved smart contracts can be used with the bridge, and those contracts are pre-written and audited as part of the platform.

## 🚨 SECURITY NOTICE - GitHub Hosting

**⚠️ CRITICAL: This repository currently contains sensitive data and is NOT safe for public hosting on GitHub without security modifications.**

### Current Security Issues:
- Real wallet seed phrases and private keys found in code
- Hardcoded API secrets and authentication tokens  
- Database credentials in configuration files
- Cryptocurrency addresses with real balances

### Can this be hosted on GitHub? 
**YES, but only after security sanitization.** See our [GitHub Hosting Analysis](GITHUB_HOSTING_ANALYSIS.md) for complete details.

## 🛠️ Quick Security Check

Run our security scanner to identify sensitive data:
```bash
./scripts/security-scan.sh
```

## 📁 Repository Structure

This repository contains static web assets only. The backend services and contract code are maintained separately and must be configured before deploying a production instance.

```
ExDex.cc/
├── website/              # Frontend application (can be hosted on GitHub Pages)
├── subdomains/          # Backend service configurations (need secure hosting)
├── scripts/             # Security and deployment tools
├── docs/               # Documentation
└── security/           # Security protocols and analysis
```

## 🔧 Configuration

**IMPORTANT:** Secrets such as API keys and wallet seeds **must not** be embedded in the client code.

### For Development:
1. Copy `website/js/config-example.js` to `website/js/config.js`
2. Use environment variables for all sensitive data
3. Never commit real credentials to version control

### For Production:
1. Use the secure configuration system in `website/js/config-secure.js`
2. Provide runtime values through secure deployment mechanisms
3. Host sensitive backend services on secure infrastructure

## 🔒 Security Protocol Implementation

This platform implements several security layers:

- **RIPTIDE Protocol**: End-to-end encryption across all systems
- **Multi-layer Authentication**: Hardware wallet integration with multi-sig support
- **Behavioral Analysis**: AI-powered anomaly detection
- **Audit Logging**: Complete transaction history and security monitoring

## 📖 Documentation

- [GitHub Hosting Analysis](GITHUB_HOSTING_ANALYSIS.md) - Complete hosting assessment
- [Security Checklist](SECURITY_CHECKLIST.md) - Step-by-step security guide
- [Subdomain Architecture](all%20exdex%20docs/subdomain-architecture.md) - System architecture

## ⚡ Quick Start (Secure Development)

1. **Security First**: Run security scan
   ```bash
   chmod +x scripts/security-scan.sh
   ./scripts/security-scan.sh
   ```

2. **Environment Setup**: Use secure configuration
   ```bash
   cp website/js/config-example.js website/js/config.js
   # Edit config.js with your development settings (no real credentials!)
   ```

3. **Local Development**: Serve static files
   ```bash
   # Use any static file server
   python -m http.server 8000
   # or
   npx serve website/
   ```

## 🚨 Before GitHub Hosting

**Required Steps:**
1. ✅ Run `./scripts/security-scan.sh` and fix all CRITICAL issues
2. ✅ Replace all real wallet data with test/example data  
3. ✅ Use environment variables for all configuration
4. ✅ Remove hardcoded API keys and secrets
5. ✅ Verify no database credentials in code

**Security Verification:**
```bash
# Must pass security scan
./scripts/security-scan.sh
echo $? # Should return 0 for safe hosting
```

## 📚 References

For further background on secure handling of credentials, refer to the **BHE NAS BTC Breach** repository which documents lessons learned from previous incidents.

## 🤝 Contributing

1. All contributions must pass security scanning
2. No sensitive data in pull requests
3. Follow secure coding practices
4. Test in isolated environment first

---

**⚠️ Current Status: REQUIRES SECURITY REVIEW BEFORE PUBLIC HOSTING**
