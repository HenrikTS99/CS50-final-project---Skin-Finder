// Script for all-skins-overview.html. For filtering and displaying search results.

// When search-bar is typed in, call filterList function.
document.querySelector("#search").addEventListener("input", filterList);

// Returns all skins that match the filter. If skin is decorated weapon, also include weapon name in search.
function filterSkins(skins, filter) {
    return skins.filter(skin => {
        if (skin.hasOwnProperty('name')) {
            return skin.name.toLowerCase().includes(filter);
        } else if (skin.hasOwnProperty('skin')) {
            return skin.skin.toLowerCase().includes(filter) || 
            skin.weapon.toLowerCase().includes(filter);
        }
    });
}

function filterList(){
    const searchInput = document.querySelector("#search");
    const filter = searchInput.value.toLowerCase();

    const filteredSkins = filterSkins(skins, filter);
    displayResults(filteredSkins);
}

// Create html of all the skins that fit the filteredSkins list.
function displayResults(filteredSkins) {
    skinsSection.innerHTML = '';

    const section = document.createElement('section');
    section.className = `ItemGrid ${sizeClass}`;
    section.id = 'resultsContainer';

    filteredSkins.forEach(skin => {
        const div = document.createElement('div');
        div.className = `grid-item ${sizeClass} ${skin.grade}`;

        const a = document.createElement('a');
        if (skin.hasOwnProperty('name')) {
            a.href = `/warpaint/${skin.name}`;
        } else if (skin.hasOwnProperty('skin')) {
            a.href = `/decorated_weapons/${skin.skin}/${skin.weapon}`;
        }
        a.style.textDecoration = 'none';

        const img = document.createElement('img');
        img.src = skin.image_url;
        img.width = 120;
        img.height = 120;

        const desc = document.createElement('div');
        desc.className = `desc item-grade ${skin.grade}`;
        if (skin.hasOwnProperty('name')) {
            desc.textContent = `${skin.name}`;
        } else if (skin.hasOwnProperty('skin')) {
            desc.textContent = `${skin.skin} ${skin.weapon}`;
        }

        a.appendChild(img);
        a.appendChild(desc);
        div.appendChild(a);
        section.appendChild(div);
        
    });
    skinsSection.appendChild(section);
}