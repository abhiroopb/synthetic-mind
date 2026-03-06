async function submitToken() {
    const token = document.getElementById('token').value.trim();
    const status = document.getElementById('status');

    function showError(msg) {
        status.textContent = '';
        const div = document.createElement('div');
        div.className = 'error';
        div.textContent = msg;
        status.appendChild(div);
    }

    if (!token) {
        showError('Please enter a token');
        return;
    }
    if (!token.startsWith('xoxp-')) {
        showError('Token should start with xoxp-');
        return;
    }

    status.textContent = 'Validating token...';
    document.querySelector('button').disabled = true;

    try {
        const resp = await fetch('/submit', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({token: token})
        });
        const data = await resp.json();

        if (data.ok) {
            document.getElementById('form-container').style.display = 'none';
            document.getElementById('success-container').style.display = 'block';
            document.getElementById('user-info').textContent =
                'Logged in as ' + (data.user?.name || 'Unknown');
            setTimeout(() => window.close(), 2000);
        } else {
            showError('Error: ' + (data.error || 'Unknown error'));
            document.querySelector('button').disabled = false;
        }
    } catch (e) {
        showError('Connection error: ' + e.message);
        document.querySelector('button').disabled = false;
    }
}

document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('token').addEventListener('keypress', (e) => {
        if (e.key === 'Enter') submitToken();
    });
});
