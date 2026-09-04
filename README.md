# rpg-2.4Reino de Elementaria

Sobre o jogo

Reino de Elementaria é um RPG 2D desenvolvido em Python com Pygame. O jogador começa sua aventura escolhendo um elemento e precisa explorar as ilhas, derrotar monstros, ganhar experiência e moedas, comprar equipamentos e conquistar as masmorras.

O objetivo é avançar pelas ilhas e, no final da aventura, enfrentar o desafio final do reino.

Principais recursos

RPG 2D com gráficos simples feitos em Pygame.

Escolha inicial entre Fogo, Água, Elétrico e Planta.

Sistema de nível e experiência.

Sistema de nível elemental.

Vida e mana que aumentam com a evolução do personagem.

Batalhas contra monstros com elementos diferentes.

Vantagens e desvantagens entre elementos.

Ataques elementais desbloqueados conforme o nível elemental aumenta.

Ataque físico usando punho e, depois, espada.

Sistema de moedas e recompensas aleatórias.

Loja com armas, armaduras e escudo.

Poções de vida e mana.

Médico para recuperar vida e mana na ilha inicial.

Sistema de missões.

Inventário.

Mapa com várias ilhas.

Sistema de salvamento e carregamento.

Masmorras com exatamente 3 monstros por entrada.

Ao derrotar os 3 monstros da masmorra, o jogador recebe um pergaminho e a próxima ilha é liberada.

Portão final para o desafio contra o chefe depois de concluir todas as masmorras.

Elementos

O jogo possui diferentes elementos, cada um com seus próprios ataques:

Elemento

Forte contra

Fraco contra

Fogo

Planta

Água

Água

Fogo

Elétrico

Elétrico

Água

Planta

Planta

Elétrico

Fogo

Sombrio

Fogo, Água, Elétrico e Planta

Nenhum definido

Terra

Veneno

Voador

Voador

Terra

Gelo

Gelo

Voador

Fogo

Fantasma

Água, Fogo, Planta e Elétrico

Veneno

Veneno

Fantasma

Terra

Durante uma batalha, usar um elemento forte contra o elemento do inimigo aumenta o dano. Usar um elemento fraco reduz o dano.

Progressão

O jogador começa com:

100 de vida.

100 de mana.

Punhos para ataques físicos.

100 moedas.

Nível 1.

Ao ganhar experiência, o personagem pode subir de nível. Ao evoluir, sua vida máxima e sua mana máxima aumentam.

O nível elemental também aumenta separadamente e libera ataques elementais mais fortes.

Loja

A loja possui os seguintes equipamentos:

Item

Preço

Armadura de Ferro

250 moedas

Armadura de Escamas

350 moedas

Cajado Arcano

150 moedas

Espada de Ferro

200 moedas

Escudo Elemental

300 moedas

Também é possível comprar:

Poção de Regeneração — 15 moedas.

Poção de Mana — 20 moedas.

Masmorra

A masmorra foi projetada para ter somente 3 monstros.

O funcionamento é:

O jogador entra na masmorra.

Enfrenta o primeiro monstro.

Enfrenta o segundo monstro.

Enfrenta o terceiro monstro.

Depois de derrotar o terceiro, a masmorra é concluída.

O jogador recebe o pergaminho correspondente à ilha.

A próxima ilha é desbloqueada.

O jogador retorna ao mundo e pode viajar para a nova ilha.

A masmorra não inicia um novo grupo depois dos 3 monstros.

Enquanto estiver na masmorra, a saída fica bloqueada. Se o jogador morrer, a masmorra termina junto com a partida atual.

Ilhas

O jogo possui 10 ilhas:

Ilha Inicial — Planta

Ilha Vulcânica — Fogo

Ilha Aquática — Água

Ilha Eletrônica — Elétrico

Ilha Sombria — Sombrio

Ilha de Terra — Terra

Ilha Voadora — Voador

Ilha de Gelo — Gelo

Ilha Fantasmagórica — Fantasma

Ilha Venenosa — Veneno

As ilhas são liberadas progressivamente conforme as masmorras são concluídas.

Controles

Mundo

W / A / S / D ou Setas — movimentar o personagem.

M — abrir o mapa das ilhas.

I — abrir o inventário.

E — interagir com locais do mundo.

F — entrar na masmorra.

B — abrir o portão do chefe.

F5 — salvar o jogo.

Batalha

1 — ataque elemental 1.

2 — ataque elemental 2.

3 — ataque elemental 3.

4 — ataque físico com punho ou espada.

H — usar poção de vida.

P — usar poção de mana.

ESC — sair da batalha normal.

Masmorra

ENTER — enfrentar o próximo monstro.

ESC — bloqueado dentro da masmorra.

M / I / B / F — bloqueados dentro da masmorra.

Menus

1 — Novo jogo / selecionar opção correspondente.

2 — Carregar jogo.

3 — Sair.

Como executar

Requisitos

É necessário ter Python instalado e a biblioteca Pygame.

Instale o Pygame com:

pip install pygame

Depois execute o arquivo principal:

python Reino_de_Elementaria_masmorra_3_monstros.py

Em alguns computadores, pode ser necessário usar python3 no lugar de python.

Salvamento

O jogo utiliza um arquivo chamado elementaria_save.json para guardar o progresso.

O salvamento é feito usando a tecla F5.

Estrutura básica

O projeto utiliza principalmente:

Python — linguagem de programação.

Pygame — criação da janela, gráficos, eventos e funcionamento do jogo.

JSON — armazenamento do progresso salvo.

Random — geração aleatória de monstros, níveis, dano, experiência e recompensas.

Objetivo do jogador

Explore o Reino de Elementaria, evolua seu personagem, consiga equipamentos melhores, conclua cada masmorra com seus 3 monstros, obtenha os pergaminhos, desbloqueie todas as ilhas e chegue ao desafio final.

Autor

Projeto desenvolvido como um jogo RPG em Python.
