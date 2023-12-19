function createCustomInput(container, options) {
    const div = document.createElement('div');
    div.innerHTML = `
        <label for="${options.name}" class="leading-7 text-sm text-gray-600">${options.label}</label>
        <input type="${options.type}" id="full-${options.name}" name="${options.name}" class="w-full bg-gray-100 bg-opacity-50 rounded border border-gray-300 focus:border-indigo-500 focus:bg-transparent focus:ring-2 focus:ring-indigo-200 text-base outline-none text-gray-700 py-1 px-3 leading-8 transition-colors duration-200 ease-in-out">
    `;
    container.appendChild(div);
}
// Chame a função para criar e adicionar o componente
createCustomInput(container, inputOptions);