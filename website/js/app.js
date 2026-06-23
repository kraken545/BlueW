/* BlueWave Dashboard - Live Price Tracker */

const DEXSCREENER_API = 'https://api.dexscreener.com/latest/dex/tokens/';

let tokenAddress = localStorage.getItem('bluewave_token_address') || '';
let updateInterval = null;

function formatPrice(num) {
  if (!num || isNaN(num)) return '$0.000000';
  if (num < 0.0001) return '$' + num.toFixed(10);
  if (num < 1) return '$' + num.toFixed(6);
  return '$' + num.toLocaleString(undefined, {minimumFractionDigits:2,maximumFractionDigits:2});
}

function formatLarge(num) {
  if (!num || isNaN(num)) return '—';
  if (num >= 1e9) return '$' + (num / 1e9).toFixed(2) + 'B';
  if (num >= 1e6) return '$' + (num / 1e6).toFixed(2) + 'M';
  if (num >= 1e3) return '$' + (num / 1e3).toFixed(2) + 'K';
  return '$' + num.toFixed(2);
}

async function fetchPrice() {
  if (!tokenAddress) {
    document.getElementById('price').textContent = '—';
    document.getElementById('change').textContent = 'Set token address';
    document.getElementById('mcap').textContent = '—';
    document.getElementById('liquidity').textContent = '—';
    document.getElementById('volume').textContent = '—';
    document.getElementById('hero-price').textContent = '$0.000000';
    document.getElementById('hero-change').textContent = 'Awaiting token';
    return;
  }

  try {
    const resp = await fetch(DEXSCREENER_API + tokenAddress);
    const data = await resp.json();
    const pair = data.pairs?.[0];

    if (pair) {
      const price = parseFloat(pair.priceUsd) || 0;
      const change = parseFloat(pair.priceChange?.h24) || 0;
      const mcap = parseFloat(pair.fdv) || 0;
      const liq = parseFloat(pair.liquidity?.usd) || 0;
      const vol = parseFloat(pair.volume?.h24) || 0;

      document.getElementById('price').textContent = formatPrice(price);
      document.getElementById('change').textContent = change >= 0 ? `+${change.toFixed(2)}%` : `${change.toFixed(2)}%`;
      document.getElementById('change').style.color = change >= 0 ? '#00B87A' : '#FF3B3B';
      document.getElementById('mcap').textContent = formatLarge(mcap);
      document.getElementById('liquidity').textContent = formatLarge(liq);
      document.getElementById('volume').textContent = formatLarge(vol);

      document.getElementById('hero-price').textContent = formatPrice(price);
      document.getElementById('hero-change').textContent = change >= 0 ? `+${change.toFixed(2)}% (24h)` : `${change.toFixed(2)}% (24h)`;
    } else {
      document.getElementById('price').textContent = 'Token not found';
      document.getElementById('hero-price').textContent = 'No pairs yet';
      document.getElementById('hero-change').textContent = 'Awaiting listing';
    }
  } catch (err) {
    console.error('Price fetch error:', err);
    document.getElementById('price').textContent = 'API error';
    document.getElementById('hero-price').textContent = 'Retrying...';
  }
}

function saveTokenAddress() {
  const input = document.getElementById('token-address-input');
  if (input.value.trim()) {
    tokenAddress = input.value.trim();
    localStorage.setItem('bluewave_token_address', tokenAddress);
    document.getElementById('token-config').close();
    fetchPrice();
  }
}

function loadSavedToken() {
  const saved = localStorage.getItem('bluewave_token_address');
  if (saved) {
    tokenAddress = saved;
    document.getElementById('token-address-input').value = saved;
  }
}

// Mobile nav toggle
document.querySelector('.nav__toggle')?.addEventListener('click', () => {
  const links = document.querySelector('.nav__links');
  links.style.display = links.style.display === 'flex' ? 'none' : 'flex';
  if (links.style.display === 'flex') {
    links.style.flexDirection = 'column';
    links.style.position = 'absolute';
    links.style.top = 'var(--nav-h)';
    links.style.left = '0';
    links.style.right = '0';
    links.style.background = 'rgba(255,255,255,0.98)';
    links.style.padding = '16px 24px';
    links.style.gap = '16px';
    links.style.borderBottom = '1px solid rgba(0,119,182,0.08)';
  }
});

// Init
loadSavedToken();
fetchPrice();
if (updateInterval) clearInterval(updateInterval);
updateInterval = setInterval(fetchPrice, 30000);
