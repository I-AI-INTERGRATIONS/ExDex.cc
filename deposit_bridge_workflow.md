# Deposit & Bridge Workflow

```mermaid
sequenceDiagram
    participant User
    participant KnoxWallet
    participant BridgeA
    participant Relayer
    participant LightClient
    participant BridgeB
    participant BHE_Network

    User->>KnoxWallet: 1. Initiate Deposit
    KnoxWallet->>BridgeA: 2. Lock Assets
    BridgeA-->>KnoxWallet: 3. Confirmation Receipt
    
    loop Every X blocks or time interval
        Relayer->>BridgeA: 4. Monitor for new deposits
        BridgeA-->>Relayer: 5. Deposit event data
        Relayer->>LightClient: 6. Submit Merkle Proof
        LightClient-->>Relayer: 7. Validation Result
        Relayer->>BridgeB: 8. Submit Cross-chain Message
    end
    
    BridgeB->>BHE_Network: 9. Verify Message Proof
    BHE_Network-->>BridgeB: 10. Validation Confirmation
    BridgeB->>KnoxWallet: 11. Mint Wrapped Assets
    KnoxWallet-->>User: 12. Deposit Complete
```

## Workflow Steps

1. **User Initiation**: User initiates a deposit from their KnoxWallet
2. **Asset Locking**: Assets are locked in BridgeA's smart contract
3. **Receipt Generation**: User receives a deposit confirmation receipt
4. **Event Monitoring**: Relayer monitors BridgeA for deposit events
5. **Proof Submission**: Relayer submits Merkle proof to Light Client
6. **Cross-chain Message**: Validated message is sent to BridgeB
7. **Verification**: BridgeB verifies the message against BHE Network
8. **Asset Minting**: Wrapped assets are minted on BHE Network
9. **Completion**: User receives wrapped assets in their KnoxWallet

## Security Considerations
- All cross-chain messages are cryptographically verified
- Multiple confirmations required before finalizing transactions
- Economic incentives ensure relayers act honestly
- Light client verification ensures data integrity
