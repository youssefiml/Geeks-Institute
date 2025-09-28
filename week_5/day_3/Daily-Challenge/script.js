const fromSelect = document.getElementById('fromCurrency');
const toSelect = document.getElementById('toCurrency');
const amountInput = document.getElementById('amount');
const convertBtn = document.getElementById('convert');
const switchBtn = document.getElementById('switch');
const resultEl = document.getElementById('result');
const API_KEY = 'a8b81b7144850b36fa80d1e5';
const API_URL = 'https://v6.exchangerate-api.com/v6/';

async function fetchCurrencies() {
  try {
    const response = await fetch(`${API_URL}${API_KEY}/codes`);
    const data = await response.json();
    data.supported_codes.forEach(code => {
      const optionFrom = new Option(`${code[0]} - ${code[1]}`, code[0]);
      const optionTo = new Option(`${code[0]} - ${code[1]}`, code[0]);
      fromSelect.add(optionFrom);
      toSelect.add(optionTo);
    });
    fromSelect.value = 'USD';
    toSelect.value = 'EUR';
  } catch (error) {
    resultEl.textContent = '❌ Error loading currencies';
  }
}

async function convertCurrency() {
  const from = fromSelect.value;
  const to = toSelect.value;
  const amount = parseFloat(amountInput.value);
  if (isNaN(amount) || amount <= 0) {
    resultEl.textContent = '⚠️ Please enter a valid number';
    return;
  }
  try {
    resultEl.innerHTML = `<i class="fas fa-spinner fa-spin"></i> Converting...`;
    const response = await fetch(`${API_URL}${API_KEY}/pair/${from}/${to}/${amount}`);
    const data = await response.json();
    if (data.result === 'success') {
      resultEl.textContent = `💰 ${amount} ${from} = ${data.conversion_result.toFixed(2)} ${to}`;
    } else {
      resultEl.textContent = '❌ Conversion failed';
    }
  } catch (error) {
    resultEl.textContent = '❌ Error fetching conversion';
  }
}

switchBtn.addEventListener('click', () => {
  const temp = fromSelect.value;
  fromSelect.value = toSelect.value;
  toSelect.value = temp;
  convertCurrency();
});

convertBtn.addEventListener('click', convertCurrency);
fetchCurrencies();