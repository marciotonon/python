function createCustomTitle(container, options) {
    const divtitle = document.createElement('div');
    divtitle.innerHTML = `
      <h1 class="sm:text-3xl text-2xl font-medium title-font text-gray-900 mb-4">${options.title}</h1>
      <p class="text-base leading-relaxed xl:w-2/4 lg:w-3/4 mx-auto text-gray-500s">${options.descricao}</p>
      <div class="flex mt-6 justify-center">
        <div class="w-16 h-1 rounded-full bg-indigo-500 inline-flex"></div>
      </div>
    `;
    container.appendChild(divtitle);
}
// Chame a função para criar e adicionar o componente
createCustomTitle(container, inputOptions);