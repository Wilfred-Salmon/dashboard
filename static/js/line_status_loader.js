function load_lines() {
    return fetch('lines')
        .then(res => res.json());
}

async function load_statuses() {
    const status_container = document.getElementById('line-statuses');

    load_lines().then(lines => {
        const placeholders = lines.map(() => {
            const placeholder = document.createElement('div');
            placeholder.classList.add('line-status-loader');
            status_container.appendChild(placeholder);
            return placeholder;
        })

        lines.forEach((line, index) => {
            fetch(`line_status/${line.id}?display_name=${line.display_name}`)
            .then(res => res.text())
            .then(html => {
                const fragment = document.createRange().createContextualFragment(html);
                placeholders[index].replaceWith(fragment);
            })
        })
    });
}

window.addEventListener("DOMContentLoaded", load_statuses);