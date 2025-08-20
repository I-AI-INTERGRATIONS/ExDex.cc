#!/bin/bash

# Security Scanner for ExDex.cc Repository
# Identifies potentially sensitive data that should not be committed to GitHub

echo "🔍 ExDex.cc Security Scanner"
echo "================================"
echo ""

# Colors for output
RED='\033[0;31m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color

# Counters
CRITICAL_ISSUES=0
HIGH_ISSUES=0
MEDIUM_ISSUES=0

# Function to report issues
report_issue() {
    local severity=$1
    local message=$2
    local file=$3
    local line=$4
    
    case $severity in
        "CRITICAL")
            echo -e "${RED}🔴 CRITICAL: $message${NC}"
            CRITICAL_ISSUES=$((CRITICAL_ISSUES + 1))
            ;;
        "HIGH")
            echo -e "${YELLOW}🟡 HIGH: $message${NC}"
            HIGH_ISSUES=$((HIGH_ISSUES + 1))
            ;;
        "MEDIUM")
            echo -e "${GREEN}🟢 MEDIUM: $message${NC}"
            MEDIUM_ISSUES=$((MEDIUM_ISSUES + 1))
            ;;
    esac
    
    if [ ! -z "$file" ]; then
        echo "   📁 File: $file"
    fi
    if [ ! -z "$line" ]; then
        echo "   📍 Line: $line"
    fi
    echo ""
}

echo "Scanning for sensitive data patterns..."
echo ""

# 1. Check for wallet seed phrases (12-24 word phrases)
echo "1. Checking for wallet seed phrases..."
SEED_RESULTS=$(grep -rn "seed.*:" --include="*.js" --include="*.json" --include="*.sh" . 2>/dev/null)
if [ ! -z "$SEED_RESULTS" ]; then
    while IFS= read -r line; do
        # Check if it contains what looks like a real seed phrase
        if echo "$line" | grep -q "abandon\|width\|helmet\|frame\|swing\|border\|happy"; then
            file=$(echo "$line" | cut -d: -f1)
            line_num=$(echo "$line" | cut -d: -f2)
            report_issue "CRITICAL" "Potential real wallet seed phrase found" "$file" "$line_num"
        elif echo "$line" | grep -qE "seed.*['\"][a-z ]{50,}['\"]"; then
            file=$(echo "$line" | cut -d: -f1)
            line_num=$(echo "$line" | cut -d: -f2)
            report_issue "HIGH" "Potential wallet seed phrase found" "$file" "$line_num"
        fi
    done <<< "$SEED_RESULTS"
fi

# 2. Check for private keys
echo "2. Checking for private keys..."
PRIVATE_KEY_RESULTS=$(grep -rn "private.*key\|privateKey" --include="*.js" --include="*.json" --include="*.sh" . 2>/dev/null)
if [ ! -z "$PRIVATE_KEY_RESULTS" ]; then
    while IFS= read -r line; do
        if echo "$line" | grep -qE "(private.*key|privateKey).*['\"][a-fA-F0-9]{64}['\"]"; then
            file=$(echo "$line" | cut -d: -f1)
            line_num=$(echo "$line" | cut -d: -f2)
            report_issue "CRITICAL" "Potential real private key found" "$file" "$line_num"
        elif echo "$line" | grep -qE "(private.*key|privateKey).*:"; then
            file=$(echo "$line" | cut -d: -f1)
            line_num=$(echo "$line" | cut -d: -f2)
            report_issue "HIGH" "Private key reference found" "$file" "$line_num"
        fi
    done <<< "$PRIVATE_KEY_RESULTS"
fi

# 3. Check for hardcoded secrets/passwords
echo "3. Checking for hardcoded secrets..."
SECRET_PATTERNS=("password.*:" "secret.*:" "api.*key" "token.*:" "AIRFORCE_ONE" "auth.*:")
for pattern in "${SECRET_PATTERNS[@]}"; do
    SECRET_RESULTS=$(grep -rn "$pattern" --include="*.js" --include="*.json" --include="*.sh" . 2>/dev/null)
    if [ ! -z "$SECRET_RESULTS" ]; then
        while IFS= read -r line; do
            file=$(echo "$line" | cut -d: -f1)
            line_num=$(echo "$line" | cut -d: -f2)
            report_issue "HIGH" "Hardcoded secret pattern found: $pattern" "$file" "$line_num"
        done <<< "$SECRET_RESULTS"
    fi
done

# 4. Check for database connection strings
echo "4. Checking for database credentials..."
DB_RESULTS=$(grep -rn "mongodb://\|postgres://\|mysql://\|redis://" --include="*.js" --include="*.json" --include="*.sh" . 2>/dev/null)
if [ ! -z "$DB_RESULTS" ]; then
    while IFS= read -r line; do
        if echo "$line" | grep -qE "(mongodb|postgres|mysql|redis)://[^/]*:[^@]*@"; then
            file=$(echo "$line" | cut -d: -f1)
            line_num=$(echo "$line" | cut -d: -f2)
            report_issue "CRITICAL" "Database connection with credentials found" "$file" "$line_num"
        else
            file=$(echo "$line" | cut -d: -f1)
            line_num=$(echo "$line" | cut -d: -f2)
            report_issue "MEDIUM" "Database connection string found" "$file" "$line_num"
        fi
    done <<< "$DB_RESULTS"
fi

# 5. Check for cryptocurrency addresses with balances
echo "5. Checking for cryptocurrency addresses..."
CRYPTO_RESULTS=$(grep -rn "balance.*BTC\|balance.*ETH" --include="*.js" --include="*.json" . 2>/dev/null)
if [ ! -z "$CRYPTO_RESULTS" ]; then
    while IFS= read -r line; do
        if echo "$line" | grep -qE "balance.*[0-9]+\.[0-9]+.*(BTC|ETH)"; then
            file=$(echo "$line" | cut -d: -f1)
            line_num=$(echo "$line" | cut -d: -f2)
            report_issue "HIGH" "Cryptocurrency address with balance found" "$file" "$line_num"
        fi
    done <<< "$CRYPTO_RESULTS"
fi

# 6. Check for real Ethereum addresses
echo "6. Checking for Ethereum addresses..."
ETH_RESULTS=$(grep -rn "0x[a-fA-F0-9]{40}" --include="*.js" --include="*.json" . 2>/dev/null)
if [ ! -z "$ETH_RESULTS" ]; then
    while IFS= read -r line; do
        # Skip common example addresses
        if ! echo "$line" | grep -qE "(example|demo|test|0x0000|0x1111)"; then
            file=$(echo "$line" | cut -d: -f1)
            line_num=$(echo "$line" | cut -d: -f2)
            report_issue "MEDIUM" "Ethereum address found (verify if real)" "$file" "$line_num"
        fi
    done <<< "$ETH_RESULTS"
fi

# 7. Check for environment variable usage (good practice)
echo "7. Checking for proper environment variable usage..."
ENV_USAGE=$(grep -rn "process\.env\." --include="*.js" . 2>/dev/null | wc -l)
if [ "$ENV_USAGE" -gt 0 ]; then
    echo -e "${GREEN}✅ Found $ENV_USAGE uses of environment variables (good practice)${NC}"
else
    report_issue "MEDIUM" "No environment variable usage found - consider using env vars for configuration"
fi

echo ""
echo "================================"
echo "🔍 Security Scan Results"
echo "================================"
echo -e "${RED}🔴 Critical Issues: $CRITICAL_ISSUES${NC}"
echo -e "${YELLOW}🟡 High Priority Issues: $HIGH_ISSUES${NC}"
echo -e "${GREEN}🟢 Medium Priority Issues: $MEDIUM_ISSUES${NC}"
echo ""

# Overall assessment
TOTAL_ISSUES=$((CRITICAL_ISSUES + HIGH_ISSUES + MEDIUM_ISSUES))

if [ $CRITICAL_ISSUES -gt 0 ]; then
    echo -e "${RED}❌ SECURITY ASSESSMENT: CRITICAL ISSUES FOUND${NC}"
    echo "❗ Repository is NOT safe for public hosting on GitHub"
    echo "🚨 Immediate action required to remove sensitive data"
    exit 1
elif [ $HIGH_ISSUES -gt 5 ]; then
    echo -e "${YELLOW}⚠️  SECURITY ASSESSMENT: HIGH RISK${NC}"
    echo "⚠️  Repository requires significant security improvements before GitHub hosting"
    exit 2
elif [ $TOTAL_ISSUES -gt 0 ]; then
    echo -e "${YELLOW}⚠️  SECURITY ASSESSMENT: MEDIUM RISK${NC}"
    echo "🔧 Some security improvements recommended before hosting"
    exit 3
else
    echo -e "${GREEN}✅ SECURITY ASSESSMENT: LOOKS GOOD${NC}"
    echo "🎉 Repository appears safe for GitHub hosting"
    exit 0
fi