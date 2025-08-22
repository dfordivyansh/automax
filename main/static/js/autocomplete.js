document.addEventListener('DOMContentLoaded', () => {
    const input = document.getElementById('search-box');
    const box = document.getElementById('suggestions-box');
    let debounce;

    input.addEventListener('input', () => {
        clearTimeout(debounce);
        const query = input.value;
        if (query.length < 2) return;

        debounce = setTimeout(() => {
            fetch(`/autocomplete/?query=${encodeURIComponent(query)}`)
                .then(res => res.json())
                .then(data => {
                    box.innerHTML = '';
                    if (!data.suggestions.length) {
                        box.classList.add('d-none');
                        return;
                    }

                    data.suggestions.forEach(s => {
                        const div = document.createElement('div');
                        div.className = 'list-group-item list-group-item-action';
                        div.textContent = s;
                        div.onclick = () => {
                            input.value = s;
                            box.classList.add('d-none');
                        };
                        box.appendChild(div);
                    });

                    box.classList.remove('d-none');
                });
        }, 300);
    });

    document.addEventListener('click', (e) => {
        if (!box.contains(e.target) && e.target !== input) {
            box.classList.add('d-none');
        }
    });
});
