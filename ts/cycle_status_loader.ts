interface Window {
    cycles: {display_name: string, id: string}[];
}

async function load_cycle_statuses(): Promise<void> {    
    window.cycles.forEach(cycle => {
        fetch(`cycle/${cycle.id}?display_name=${cycle.display_name}`)
        .then(res => res.text())
        .then(html => {
            const fragment = document.createRange().createContextualFragment(html);
            document.getElementById(cycle.id)!.replaceWith(fragment);
        })
    });
}

window.addEventListener("DOMContentLoaded", load_cycle_statuses);