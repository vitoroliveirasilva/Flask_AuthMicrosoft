function menushow() {
    // Seleciona o elemento com a classe 'mobile-menu'
    let menumobile = document.querySelector('.mobile-menu');
    
    // Verifica se o elemento tem a classe 'open'
    if (menumobile.classList.contains('open')) {
        // Se tiver a classe 'open', remove a classe para fechar o menu
        menumobile.classList.remove('open');
        
        // Altera o ícone para o ícone de menu aberto
        document.querySelector('.icon').src = "../static/assets/icons/open_menu_black.svg";
    } else {
        // Se não tiver a classe 'open', adiciona a classe para abrir o menu
        menumobile.classList.add('open');
        
        // Altera o ícone para o ícone de menu fechado
        document.querySelector('.icon').src = "../static/assets/icons/close_menu_black.svg";
    }
}
