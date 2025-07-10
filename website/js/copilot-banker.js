// Copilot Banker: AI-powered assistant using Cortana voice
const API_URL = window.EXDEX_API_URL || 'http://127.0.0.1:8000';

const chatLog = document.getElementById('samantha-chat-log');
const chatForm = document.getElementById('samantha-chat-form');
const chatInput = document.getElementById('samantha-input');
const micBtn = document.getElementById('samantha-mic');
const walletCreateBtn = document.getElementById('samantha-wallet-create');
const walletRecoverBtn = document.getElementById('samantha-wallet-recover');
const walletSendBtn = document.getElementById('samantha-wallet-send');

function appendMessage(author, msg) {
    const el = document.createElement('div');
    const authorEl = document.createElement('strong');
    authorEl.style.color = author === 'Copilot Banker' ? '#3e4bff' : '#fff';
    authorEl.textContent = `${author}:`;
    const msgEl = document.createElement('span');
    msgEl.textContent = msg;
    el.appendChild(authorEl);
    el.appendChild(document.createTextNode(' ')); // Add a space between author and message
    el.appendChild(msgEl);
    el.style.marginBottom = '7px';
    chatLog.appendChild(el);
    chatLog.scrollTop = chatLog.scrollHeight;
}

// Chat submit
chatForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const msg = chatInput.value.trim();
    if (!msg) return;
    appendMessage('You', msg);
    chatInput.value = '';
    appendMessage('Copilot Banker', '<em>Thinking...</em>');
    const resp = await fetch(`${API_URL}/ai/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: msg })
    });
    const data = await resp.json();
    const lastChild = chatLog.lastChild;
    lastChild.textContent = ''; // Clear existing content
    const authorEl = document.createElement('strong');
    authorEl.style.color = '#3e4bff';
    authorEl.textContent = 'Copilot Banker:';
    const responseEl = document.createElement('span');
    responseEl.textContent = data.response;
    lastChild.appendChild(authorEl);
    lastChild.appendChild(document.createTextNode(' ')); // Add a space between author and response
    lastChild.appendChild(responseEl);
    // Optionally, play TTS
    playTTS(data.response);
});

// Microphone (speech-to-text)
micBtn.addEventListener('click', async () => {
    if (!navigator.mediaDevices || !window.MediaRecorder) {
        alert('Microphone not supported in this browser.');
        return;
    }
    micBtn.disabled = true;
    micBtn.querySelector('img').style.filter = 'invert(0.2)';
    appendMessage('You', '<em>Listening...</em>');

    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    const recorder = new MediaRecorder(stream);
    let chunks = [];
    recorder.ondataavailable = e => chunks.push(e.data);
    recorder.onstop = async () => {
        const blob = new Blob(chunks, { type: 'audio/wav' });
        const formData = new FormData();
        formData.append('file', blob, 'audio.wav');
        const resp = await fetch(`${API_URL}/ai/speech-to-text`, { method: 'POST', body: formData });
        const data = await resp.json();
        chatLog.lastChild.innerHTML = `<strong style="color:#fff;">You:</strong> <span>${data.transcript}</span>`;
        chatInput.value = data.transcript;
        micBtn.disabled = false;
        micBtn.querySelector('img').style.filter = 'invert(0.8)';
    };
    recorder.start();
    setTimeout(() => recorder.stop(), 5000); // 5 seconds max
});

// Play TTS
async function playTTS(text) {
    const resp = await fetch(`${API_URL}/ai/text-to-speech`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text })
    });
    if (resp.ok) {
        const audioBlob = await resp.blob();
        const audioUrl = URL.createObjectURL(audioBlob);
        const audio = new Audio(audioUrl);
        audio.play();
    }
}

// Wallet controls
walletCreateBtn.addEventListener('click', async () => {
    const blockchain = prompt('Create wallet for which blockchain? (btc/eth)');
    if (!blockchain) return;
    appendMessage('Copilot Banker', '<em>Creating wallet...</em>');
    const resp = await fetch(`${API_URL}/wallet/create`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ blockchain })
    });
    const data = await resp.json();
    appendMessage('Copilot Banker', `Address: ${data.address}\nMnemonic: ${data.mnemonic}`);
});

walletRecoverBtn.addEventListener('click', async () => {
    const blockchain = prompt('Recover wallet for which blockchain? (btc/eth)');
    const mnemonic = prompt('Enter your mnemonic phrase:');
    if (!blockchain || !mnemonic) return;
    appendMessage('Copilot Banker', '<em>Recovering wallet...</em>');
    const resp = await fetch(`${API_URL}/wallet/recover`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ blockchain, mnemonic })
    });
    const data = await resp.json();
    appendMessage('Copilot Banker', `Recovered Address: <code>${data.address}</code>`);
});

walletSendBtn.addEventListener('click', async () => {
    const blockchain = prompt('Send from which blockchain? (btc/eth)');
    const from_address = prompt('From address:');
    const to_address = prompt('To address:');
    const amount = prompt('Amount:');
    const private_key = prompt('Private key:');
    if (!blockchain || !from_address || !to_address || !amount || !private_key) return;
    appendMessage('Copilot Banker', '<em>Sending transaction...</em>');
    const resp = await fetch(`${API_URL}/wallet/send`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ blockchain, from_address, to_address, amount: parseFloat(amount), private_key })
    });
    const data = await resp.json();
    appendMessage('Copilot Banker', `Transaction ID: ${data.txid} Status: ${data.status}`);
});
