# ExDex.cc

ExDex.cc is a demonstration of the EXDEX/AF1 bridge system for managing cryptocurrency
transactions. The project provides a sample frontend that interacts with EXDEX services
for wallet and trading functionality. Only EXDEX-approved smart contracts can be used
with the bridge, and those contracts are pre-written and audited as part of the platform.

This repository contains static web assets only. The backend services and contract code are maintained separately and must be provided when setting up a production instance. Smart contract packages can be obtained from the official ExDEX repository or from your local node.

## Configuration

Secrets such as API keys and wallet seeds **must not** be embedded in the client code.
Create a `website/js/config.js` file (see `config-example.js`) and provide runtime
values like `window.EXDEX_API_URL` through a secure deployment mechanism or environment
variables.

For further background on secure handling of credentials, refer to the **BHE NAS BTC
Breach** repository which documents lessons learned from previous incidents.
