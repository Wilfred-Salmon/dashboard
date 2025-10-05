interface Window {
    lines: {id: string, display_name: string}[];
}

async function load_statuses(): Promise<void> {    
    window.lines.forEach(line => {
        fetch(`line_status/${line.id}?display_name=${line.display_name}`)
        .then(res => res.text())
        .then(html => {
            const fragment = document.createRange().createContextualFragment(html);
            document.getElementById(line.id)!.replaceWith(fragment);
        })
    });
}

window.addEventListener("DOMContentLoaded", load_statuses);